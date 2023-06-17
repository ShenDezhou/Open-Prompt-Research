import copy
import time
import utils as U

from agents import ActionAgent
from agents import CriticAgent
from agents import CurriculumAgent
from agents import SkillManager
from env import VoyagerEnv


# parse model
import getopt
import sys

openai_model = "gpt-3.5-turbo-0613"
argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "m:", ["model ="])
except:
    print("Error Message ")

for name, value in options:
    if name in ['-m', '--model']:
        openai_model = value
print("USING:"+openai_model)
recorder = U.EventRecorder()
llm_recorder = U.EventRecorder()

resume = True # if resume the skills
# Agents BEGIN.
action_agent=ActionAgent(model_name=openai_model, resume=resume)
critic_agent=CriticAgent(model_name=openai_model, llm_recorder=llm_recorder)
curriculum_agent = CurriculumAgent(
    model_name=openai_model,
    core_inventory_items=r".*_log|.*_planks|stick|crafting_table|furnace"
        r"|cobblestone|dirt|coal|.*_pickaxe|.*_sword|.*_axe",
    llm_recorder=llm_recorder,
    resume=resume
)
skill_manager = SkillManager(model_name=openai_model, llm_recorder=llm_recorder, resume=resume)
env=VoyagerEnv(mc_port=25565)
# Agents END.


#CONSTANT
env_wait_ticks=20

max_iterations=1
action_agent_task_max_retries=4
reset_env=True
reset_placed_if_failed=False

#global var
action_agent_rollout_num_iter = -1
messages = []
conversations = []
last_events = []


def reset(task, context="", reset_env=True):
    global action_agent_rollout_num_iter, messages, conversations, llm_recorder
    action_agent_rollout_num_iter = 0
    task = task
    context = context
    if reset_env:
        env.reset(
            options={
                "mode": "soft",
                "wait_ticks": env_wait_ticks,
            }
        )
    difficulty = (
        "easy" if len(curriculum_agent.completed_tasks) > 15 else "peaceful"
    )
    # step to peek an observation
    events = env.step(
        "bot.chat(`/time set ${getNextTime()}`);\n"
        + f"bot.chat(`/difficulty {difficulty}`);"
    )
    skills = skill_manager.retrieve_skills(query=context)
    print(
        f"\033[33mRender Action Agent system message with {len(skills)} control_primitives\033[0m"
    )
    system_message = action_agent.render_system_message(skills=skills)
    human_message = action_agent.render_human_message(
        events=events, code="", task=task, context=context, critique=""
    )
    messages = [system_message, human_message]
    print(
        f"\033[32m****Action Agent human message****\n{human_message.content}\033[0m"
    )
    assert len(messages) == 2
    conversations = []
    llm_recorder.record([system_message.content, human_message.content], "llm-action")
    return messages

def step():
    global action_agent_rollout_num_iter, messages, conversations, last_events, llm_recorder, recorder, skill_manager
    if action_agent_rollout_num_iter < 0:
        raise ValueError("Agent must be reset before stepping")
    ai_message = action_agent.llm(messages)
    print(f"\033[34m****Action Agent ai message****\n{ai_message.content}\033[0m")
    conversations.append(
        (messages[0].content, messages[1].content, ai_message.content)
    )
    llm_recorder.record([messages[0].content, messages[1].content, ai_message.content], "llm-action")
    parsed_result = action_agent.process_ai_message(message=ai_message)
    success = False
    if isinstance(parsed_result, dict):
        code = parsed_result["program_code"] + "\n" + parsed_result["exec_code"]
        events = env.step(
            code,
            programs=skill_manager.programs,
        )
        recorder.record(events, task)
        action_agent.update_chest_memory(events[-1][1]["nearbyChests"])
        success, critique = critic_agent.check_task_success(
            events=events,
            task=task,
            context=context,
            chest_observation=action_agent.render_chest_observation(),
            max_retries=5,
        )
        if reset_placed_if_failed and not success:
            # revert all the placing event in the last step
            blocks = []
            positions = []
            for event_type, event in events:
                if event_type == "onSave" and event["onSave"].endswith("_placed"):
                    block = event["onSave"].split("_placed")[0]
                    position = event["status"]["position"]
                    blocks.append(block)
                    positions.append(position)
            new_events = env.step(
                f"await givePlacedItemBack(bot, {U.json_dumps(blocks)}, {U.json_dumps(positions)})",
                programs=skill_manager.programs,
            )
            llm_recorder.record(new_events, "env-events")
            events[-1][1]["inventory"] = new_events[-1][1]["inventory"]
            events[-1][1]["voxels"] = new_events[-1][1]["voxels"]
        new_skills = skill_manager.retrieve_skills(
            query=context
                  + "\n\n"
                  + action_agent.summarize_chatlog(events)
        )
        system_message = action_agent.render_system_message(skills=new_skills)
        human_message = action_agent.render_human_message(
            events=events,
            code=parsed_result["program_code"],
            task=task,
            context=context,
            critique=critique,
        )
        last_events = copy.deepcopy(events)
        messages = [system_message, human_message]
    else:
        assert isinstance(parsed_result, str)
        recorder.record([], task)
        print(f"\033[34m{parsed_result} Trying again!\033[0m")
    assert len(messages) == 2
    action_agent_rollout_num_iter += 1
    done = (
            action_agent_rollout_num_iter >= action_agent_task_max_retries
            or success
    )
    info = {
        "success": success,
        "conversations": conversations,
    }
    if success:
        assert (
                "program_code" in parsed_result and "program_name" in parsed_result
        ), "program and program_name must be returned when success"
        info["program_code"] = parsed_result["program_code"]
        info["program_name"] = parsed_result["program_name"]
    else:
        print(
            f"\033[32m****Action Agent human message****\n{messages[-1].content}\033[0m"
        )
    return messages, 0, done, info

def rollout(task, context, reset_env=True):
    reset(task=task, context=context, reset_env=reset_env)
    while True:
        messages, reward, done, info = step()
        if done:
            break
    return messages, reward, done, info


if __name__ == "__main__":
    if resume:
        # keep the inventory
        env.reset(
            options={
                "mode": "soft",
                "wait_ticks": env_wait_ticks,
            }
        )
    else:
        # clear the inventory
        env.reset(
            options={
                "mode": "hard",
                "wait_ticks": env_wait_ticks,
            }
        )
        resume = True
    last_events = env.step("")
    
    while True:
        if recorder.iteration > max_iterations:
            print("Iteration limit reached")
            break
        task, context = curriculum_agent.propose_next_task(
            events=last_events,
            chest_observation=action_agent.render_chest_observation(),
            max_retries=5,
        )
        llm_recorder.record([task, context], "llm-curri")
        print(
            f"\033[35mStarting task {task} for at most {action_agent_task_max_retries} times\033[0m"
        )
        try:
            messages, reward, done, info = rollout(
                task=task,
                context=context,
                reset_env=reset_env,
            )
        except Exception as e:
            time.sleep(3)  # wait for mineflayer to exit
            info = {
                "success": False,
            }
            # reset inventory here
            last_events = env.reset(
                options={
                    "mode": "hard",
                    "wait_ticks": env_wait_ticks,
                    "inventory": last_events[-1][1]["inventory"],
                    "equipment": last_events[-1][1]["status"]["equipment"],
                    "position": last_events[-1][1]["status"]["position"],
                }
            )
            # use red color background to print the error
            print("Your last round rollout terminated due to error:")
            print(f"\033[41m{e}\033[0m")
        if (
                task == "Place and deposit useless items into a chest"
                or task.startswith("Deposit useless items into the chest at")
        ):
            continue
        if info["success"]:
            print(f"\033[35mCompleted task {task}.\033[0m")
            skill_manager.add_skill(
                program_name=info["program_name"],
                program_code=info["program_code"],
            )
            curriculum_agent.completed_tasks.append(task)
        else:
            curriculum_agent.failed_tasks.append(task)
            print(
                f"\033[35mFailed to complete task {task}. Skipping to next task.\033[0m"
            )
        # clean up tasks and dump to disk
        curriculum_agent.clean_up_tasks()
        print(
            f"\033[35mCompleted tasks: {', '.join(curriculum_agent.completed_tasks)}\033[0m"
        )
        print(
            f"\033[35mFailed tasks: {', '.join(curriculum_agent.failed_tasks)}\033[0m"
        )