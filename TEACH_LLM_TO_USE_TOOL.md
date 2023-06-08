# 教LLM使用工具

本项目使用了[javascript](https://pypi.org/project/javascript/)包。该项目目标时允许Nodejs与Python交互。

AI项目使用了大量的python代码作为开发语言，而javascript的重要性也是不言而喻的，整个互联网都是运行在其上的。

一个可工作的版本要求Node.js=14并且Python=3.8。

## LLM代码生成自我验证

在输入任务目标后，LLM生成代码，通过node环境验证生成代码可编译/运行性。

````python
babel = require("@babel/core")
babel_generator = require("@babel/generator").default

code_pattern = re.compile(r"```(?:javascript|js)(.*?)```", re.DOTALL)
code = "\n".join(code_pattern.findall(message.content))
parsed = babel.parse(code)
functions = []
assert len(list(parsed.program.body)) > 0, "No functions found"
for i, node in enumerate(parsed.program.body):
    if node.type != "FunctionDeclaration":
        continue
    node_type = (
        "AsyncFunctionDeclaration"
        if node["async"]
        else "FunctionDeclaration"
    )
    functions.append(
        {
            "name": node.id.name,
            "type": node_type,
            "body": babel_generator(node).code,
            "params": list(node["params"]),
        }
    )
# find the last async function
main_function = None
for function in reversed(functions):
    if function["type"] == "AsyncFunctionDeclaration":
        main_function = function
        break
assert (
    main_function is not None
), "No async function found. Your main function must be async."
assert (
    len(main_function["params"]) == 1
    and main_function["params"][0].name == "bot"
), f"Main function {main_function['name']} must take a single argument named 'bot'"
program_code = "\n\n".join(function["body"] for function in functions)
exec_code = f"await {main_function['name']}(bot);"
return {
    "program_code": program_code,
    "program_name": main_function["name"],
    "exec_code": exec_code,
}
````

上述代码在LLM的生成文本中提取javascript代码，并用nodejs中的babel库验证生成代码的可运行性。

## 开放学习过程

Voyager的开放学习是用`代码生成`替代`模型训练`的一个过程。

```python
self.last_events = self.env.step("")
while True:
    if self.recorder.iteration > self.max_iterations:
        print("Iteration limit reached")
        break
    task, context = self.curriculum_agent.propose_next_task(
        events=self.last_events,
        chest_observation=self.action_agent.render_chest_observation(),
        max_retries=5,
    )
    print(
        f"\033[35mStarting task {task} for at most {self.action_agent_task_max_retries} times\033[0m"
    )
    try:
        messages, reward, done, info = self.rollout(
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
        self.last_events = self.env.reset(
            options={
                "mode": "hard",
                "wait_ticks": self.env_wait_ticks,
                "inventory": self.last_events[-1][1]["inventory"],
                "equipment": self.last_events[-1][1]["status"]["equipment"],
                "position": self.last_events[-1][1]["status"]["position"],
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
        self.skill_manager.add_skill(
            program_name=info["program_name"],
            program_code=info["program_code"],
        )
        self.curriculum_agent.completed_tasks.append(task)
    else:
        self.curriculum_agent.failed_tasks.append(task)
        print(
            f"\033[35mFailed to complete task {task}. Skipping to next task.\033[0m"
        )
    # clean up tasks and dump to disk
    self.curriculum_agent.clean_up_tasks()
    print(
        f"\033[35mCompleted tasks: {', '.join(self.curriculum_agent.completed_tasks)}\033[0m"
    )
    print(
        f"\033[35mFailed tasks: {', '.join(self.curriculum_agent.failed_tasks)}\033[0m"
    )
```

开放学习过程是一个训练过程，检查当前步数是否到达最大步数。  

> 重置环境，根据是否`resume`来确定是软重置还是硬重置
> 最近事件保存环境单步执行结果

每步训练：  

* 课程智能体：给出下一个任务、环境
* 执行[单步探索]并返回任务执行情况：成功状态、生成代码名称与详细编码
* 任务执行异常：失败状态、重置环境、保存最近事件
* 如任务名称是需要`待忽略`任务，则进入下一步
* 执行结果为成功：技能智能体增加新技能(技能名称、详细代码）
* 课程智能体更新成功、失败队列
* 课程智能体清理当前任务，当前步数完成，进入下一步。

Voyager的学习过程就是智能体探索过程。

## 单步探索

```python
ai_message = self.action_agent.llm(self.messages)
print(f"\033[34m****Action Agent ai message****\n{ai_message.content}\033[0m")
self.conversations.append(
    (self.messages[0].content, self.messages[1].content, ai_message.content)
)
parsed_result = self.action_agent.process_ai_message(message=ai_message)
...
code = parsed_result["program_code"] + "\n" + parsed_result["exec_code"]
events = self.env.step(
    code,
    programs=self.skill_manager.programs,
)
self.recorder.record(events, self.task)
self.action_agent.update_chest_memory(events[-1][1]["nearbyChests"])
success, critique = self.critic_agent.check_task_success(
    events=events,
    task=self.task,
    context=self.context,
    chest_observation=self.action_agent.render_chest_observation(),
    max_retries=5,
)
...
new_skills = self.skill_manager.retrieve_skills(
    query=self.context
    + "\n\n"
    + self.action_agent.summarize_chatlog(events)
)
system_message = self.action_agent.render_system_message(skills=new_skills)
human_message = self.action_agent.render_human_message(
    events=events,
    code=parsed_result["program_code"],
    task=self.task,
    context=self.context,
    critique=critique,
)
self.last_events = copy.deepcopy(events)
self.messages = [system_message, human_message]
```

单步探索结合了环境智能体、动作智能体、评论家智能体、技能智能体等功能模块的联合处理。