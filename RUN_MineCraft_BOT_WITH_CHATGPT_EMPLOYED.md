# ChatGPT playing Minecraft.

这个项目受Voyager启发，使用ChatGPT驱动Minecraft中BOT进行开放世界探索。

项目前提：
* [Minecraft server](https://github.com/ShenDezhou/MineCraft-Server)
* [Node_server(Mineflayer-powered)](https://github.com/ShenDezhou/Open-Node-Research)

按照上述项目说明启动mcserver后，将Node server代码放置到与本项目同级目录下，可以执行该项目的`learn.py`，开始探索。

运行项目前需要在`~/.bash_profile`中配置OPENAI_KEY。


## 日志分析
在Events下面记录了Node服务器返回的日志，也记录了LLM的交互日志。

### MC Bot的Node状态

本项目运行是在所有的Agent都使用的ChatGPT模型，并未与原Voyager项目中CurriculumAgent、ActionAgent设置为GPT-4保持一致。读者根据预算可自行尝试。

从Node日志看出，该Bot还在自我验证阶段，即利用`javascript`库在验证代码的完整性、可运行性，通过bridger调用的是node中的babel的core、generator两个库。

```javascript
2023-06-13 21:07:42,222 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:07:43,223 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:07:46,230 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:07:46,230 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:07:46,245 - mineflayer - INFO - {
2023-06-13 21:07:46,245 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:07:46,245 - mineflayer - INFO - port: 25565,
2023-06-13 21:07:46,245 - mineflayer - INFO - reset: 'hard',
2023-06-13 21:07:46,245 - mineflayer - INFO - inventory: {},
2023-06-13 21:07:46,245 - mineflayer - INFO - equipment: [],
2023-06-13 21:07:46,245 - mineflayer - INFO - spread: false,
2023-06-13 21:07:46,245 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:07:46,245 - mineflayer - INFO - position: null
2023-06-13 21:07:46,245 - mineflayer - INFO - }
2023-06-13 21:07:47,316 - mineflayer - INFO - { code: '', programs: '' }
2023-06-13 21:07:50,381 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:07:51,398 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:07:54,407 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:07:54,407 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:07:54,421 - mineflayer - INFO - {
2023-06-13 21:07:54,422 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:07:54,422 - mineflayer - INFO - port: 25565,
2023-06-13 21:07:54,422 - mineflayer - INFO - reset: 'soft',
2023-06-13 21:07:54,422 - mineflayer - INFO - inventory: {},
2023-06-13 21:07:54,422 - mineflayer - INFO - equipment: [],
2023-06-13 21:07:54,422 - mineflayer - INFO - spread: false,
2023-06-13 21:07:54,422 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:07:54,422 - mineflayer - INFO - position: null
2023-06-13 21:07:54,422 - mineflayer - INFO - }
2023-06-13 21:07:55,639 - mineflayer - INFO - {
2023-06-13 21:07:55,639 - mineflayer - INFO - code: 'bot.chat(`/time set ${getNextTime()}`);\nbot.chat(`/difficulty peaceful`);',
2023-06-13 21:07:55,639 - mineflayer - INFO - programs: ''
2023-06-13 21:07:55,639 - mineflayer - INFO - }
2023-06-13 21:08:34,945 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:08:35,962 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:08:38,970 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:08:38,970 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:08:38,991 - mineflayer - INFO - {
2023-06-13 21:08:38,991 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:08:38,991 - mineflayer - INFO - port: 25565,
2023-06-13 21:08:38,991 - mineflayer - INFO - reset: 'hard',
2023-06-13 21:08:38,991 - mineflayer - INFO - inventory: {},
2023-06-13 21:08:38,991 - mineflayer - INFO - equipment: [ null, null, null, null, null, null ],
2023-06-13 21:08:38,991 - mineflayer - INFO - spread: false,
2023-06-13 21:08:38,991 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:08:38,991 - mineflayer - INFO - position: { x: 34.7, y: 67, z: -50.35393393610496 }
2023-06-13 21:08:38,991 - mineflayer - INFO - }
2023-06-13 21:08:40,188 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:08:41,202 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:08:44,210 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:08:44,210 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:08:44,224 - mineflayer - INFO - {
2023-06-13 21:08:44,225 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:08:44,225 - mineflayer - INFO - port: 25565,
2023-06-13 21:08:44,225 - mineflayer - INFO - reset: 'soft',
2023-06-13 21:08:44,225 - mineflayer - INFO - inventory: {},
2023-06-13 21:08:44,225 - mineflayer - INFO - equipment: [],
2023-06-13 21:08:44,225 - mineflayer - INFO - spread: false,
2023-06-13 21:08:44,225 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:08:44,225 - mineflayer - INFO - position: null
2023-06-13 21:08:44,225 - mineflayer - INFO - }
2023-06-13 21:08:45,342 - mineflayer - INFO - {
2023-06-13 21:08:45,342 - mineflayer - INFO - code: 'bot.chat(`/time set ${getNextTime()}`);\nbot.chat(`/difficulty peaceful`);',
2023-06-13 21:08:45,342 - mineflayer - INFO - programs: ''
2023-06-13 21:08:45,342 - mineflayer - INFO - }
2023-06-13 21:09:16,660 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:09:17,674 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:09:20,682 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:09:20,683 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:09:20,697 - mineflayer - INFO - {
2023-06-13 21:09:20,697 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:09:20,698 - mineflayer - INFO - port: 25565,
2023-06-13 21:09:20,698 - mineflayer - INFO - reset: 'hard',
2023-06-13 21:09:20,698 - mineflayer - INFO - inventory: {},
2023-06-13 21:09:20,698 - mineflayer - INFO - equipment: [ null, null, null, null, null, null ],
2023-06-13 21:09:20,698 - mineflayer - INFO - spread: false,
2023-06-13 21:09:20,698 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:09:20,698 - mineflayer - INFO - position: { x: 34.7, y: 66, z: -50.35393393610496 }
2023-06-13 21:09:20,698 - mineflayer - INFO - }
2023-06-13 21:09:21,910 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:09:22,928 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:09:25,936 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:09:25,936 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:09:25,951 - mineflayer - INFO - {
2023-06-13 21:09:25,951 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:09:25,951 - mineflayer - INFO - port: 25565,
2023-06-13 21:09:25,951 - mineflayer - INFO - reset: 'soft',
2023-06-13 21:09:25,951 - mineflayer - INFO - inventory: {},
2023-06-13 21:09:25,951 - mineflayer - INFO - equipment: [],
2023-06-13 21:09:25,951 - mineflayer - INFO - spread: false,
2023-06-13 21:09:25,951 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:09:25,952 - mineflayer - INFO - position: null
2023-06-13 21:09:25,952 - mineflayer - INFO - }
2023-06-13 21:09:27,108 - mineflayer - INFO - {
2023-06-13 21:09:27,108 - mineflayer - INFO - code: 'bot.chat(`/time set ${getNextTime()}`);\nbot.chat(`/difficulty peaceful`);',
2023-06-13 21:09:27,108 - mineflayer - INFO - programs: ''
2023-06-13 21:09:27,108 - mineflayer - INFO - }
2023-06-13 21:09:58,564 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:09:59,582 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:10:02,591 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:10:02,591 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:10:02,606 - mineflayer - INFO - {
2023-06-13 21:10:02,606 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:10:02,606 - mineflayer - INFO - port: 25565,
2023-06-13 21:10:02,606 - mineflayer - INFO - reset: 'hard',
2023-06-13 21:10:02,606 - mineflayer - INFO - inventory: {},
2023-06-13 21:10:02,606 - mineflayer - INFO - equipment: [ null, null, null, null, null, null ],
2023-06-13 21:10:02,606 - mineflayer - INFO - spread: false,
2023-06-13 21:10:02,606 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:10:02,606 - mineflayer - INFO - position: { x: 34.7, y: 66, z: -50.35393393610496 }
2023-06-13 21:10:02,606 - mineflayer - INFO - }
2023-06-13 21:10:03,749 - mineflayer - INFO - Stopping subprocess.
2023-06-13 21:10:04,764 - mineflayer - INFO - Starting subprocess with commands: ['node', '/Users/tsinghuaboy/projects/Open-Node-Research/index.js', '3000']
2023-06-13 21:10:07,772 - mineflayer - INFO - Server started on port 3000
2023-06-13 21:10:07,772 - mineflayer - INFO - Subprocess is ready.
2023-06-13 21:10:07,787 - mineflayer - INFO - {
2023-06-13 21:10:07,787 - mineflayer - INFO - server: '127.0.0.1',
2023-06-13 21:10:07,787 - mineflayer - INFO - port: 25565,
2023-06-13 21:10:07,787 - mineflayer - INFO - reset: 'soft',
2023-06-13 21:10:07,787 - mineflayer - INFO - inventory: {},
2023-06-13 21:10:07,787 - mineflayer - INFO - equipment: [],
2023-06-13 21:10:07,787 - mineflayer - INFO - spread: false,
2023-06-13 21:10:07,787 - mineflayer - INFO - waitTicks: 1,
2023-06-13 21:10:07,787 - mineflayer - INFO - position: null
2023-06-13 21:10:07,787 - mineflayer - INFO - }
2023-06-13 21:10:08,952 - mineflayer - INFO - {
2023-06-13 21:10:08,952 - mineflayer - INFO - code: 'bot.chat(`/time set ${getNextTime()}`);\nbot.chat(`/difficulty peaceful`);',
2023-06-13 21:10:08,953 - mineflayer - INFO - programs: ''
2023-06-13 21:10:08,953 - mineflayer - INFO - }
```


### Action-LLM

这里使用了langchain库的SystemPrompt和HumanPrompt的设计，
在库中这两部分合成一部分，输入到LLM，生成结果。

SystemPrompt是教LLM成为一种具体工具：如assistant。
HumanPrompt是与当前生成任务相关的上下文。

System输入为：
````javascript
You are a helpful assistant that writes Mineflayer javascript code to complete any Minecraft task specified by me.

Here are some useful programs written with Mineflayer APIs.

/*
Explore until find an iron_ore, use Vec3(0, -1, 0) because iron ores are usually underground
await exploreUntil(bot, new Vec3(0, -1, 0), 60, () => {
    const iron_ore = bot.findBlock({
        matching: mcData.blocksByName[\"iron_ore\"].id,
        maxDistance: 32,
    });
    return iron_ore;
});

Explore until find a pig, use Vec3(1, 0, 1) because pigs are usually on the surface
let pig = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
    const pig = bot.nearestEntity((entity) => {
        return (
            entity.name === \"pig\" &&
            entity.position.distanceTo(bot.entity.position) < 32
        );
    });
    return pig;
});
*/
async function exploreUntil(bot, direction, maxTime = 60, callback) {
    /*
    Implementation of this function is omitted.
    direction: Vec3, can only contain value of -1, 0 or 1
    maxTime: number, the max time for exploration
    callback: function, early stop condition, will be called each second, exploration will stop if return value is not null

    Return: null if explore timeout, otherwise return the return value of callback
    */
}


// Mine 3 cobblestone: mineBlock(bot, \"stone\", 3);
async function mineBlock(bot, name, count = 1) {
    const blocks = bot.findBlocks({
        matching: (block) => {
            return block.name === name;
        },
        maxDistance: 32,
        count: count,
    });
    const targets = [];
    for (let i = 0; i < Math.min(blocks.length, count); i++) {
        targets.push(bot.blockAt(blocks[i]));
    }
    await bot.collectBlock.collect(targets, { ignoreNoPath: true });
}


// Craft 8 oak_planks from 2 oak_log (do the recipe 2 times): craftItem(bot, \"oak_planks\", 2);
// You must place a crafting table before calling this function
async function craftItem(bot, name, count = 1) {
    const item = mcData.itemsByName[name];
    const craftingTable = bot.findBlock({
        matching: mcData.blocksByName.crafting_table.id,
        maxDistance: 32,
    });
    await bot.pathfinder.goto(
        new GoalLookAtBlock(craftingTable.position, bot.world)
    );
    const recipe = bot.recipesFor(item.id, null, 1, craftingTable)[0];
    await bot.craft(recipe, count, craftingTable);
}


// Place a crafting_table near the player, Vec3(1, 0, 0) is just an example, you shouldn't always use that: placeItem(bot, \"crafting_table\", bot.entity.position.offset(1, 0, 0));
async function placeItem(bot, name, position) {
    const item = bot.inventory.findInventoryItem(mcData.itemsByName[name].id);
    // find a reference block
    const faceVectors = [
        new Vec3(0, 1, 0),
        new Vec3(0, -1, 0),
        new Vec3(1, 0, 0),
        new Vec3(-1, 0, 0),
        new Vec3(0, 0, 1),
        new Vec3(0, 0, -1),
    ];
    let referenceBlock = null;
    let faceVector = null;
    for (const vector of faceVectors) {
        const block = bot.blockAt(position.minus(vector));
        if (block?.name !== \"air\") {
            referenceBlock = block;
            faceVector = vector;
            break;
        }
    }
    // You must first go to the block position you want to place
    await bot.pathfinder.goto(new GoalPlaceBlock(position, bot.world, {}));
    // You must equip the item right before calling placeBlock
    await bot.equip(item, \"hand\");
    await bot.placeBlock(referenceBlock, faceVector);
}


// Smelt 1 raw_iron into 1 iron_ingot using 1 oak_planks as fuel: smeltItem(bot, \"raw_iron\", \"oak_planks\");
// You must place a furnace before calling this function
async function smeltItem(bot, itemName, fuelName, count = 1) {
    const item = mcData.itemsByName[itemName];
    const fuel = mcData.itemsByName[fuelName];
    const furnaceBlock = bot.findBlock({
        matching: mcData.blocksByName.furnace.id,
        maxDistance: 32,
    });
    await bot.pathfinder.goto(
        new GoalLookAtBlock(furnaceBlock.position, bot.world)
    );
    const furnace = await bot.openFurnace(furnaceBlock);
    for (let i = 0; i < count; i++) {
        await furnace.putFuel(fuel.id, null, 1);
        await furnace.putInput(item.id, null, 1);
        // Wait 12 seconds for the furnace to smelt the item
        await bot.waitForTicks(12 * 20);
        await furnace.takeOutput();
    }
    await furnace.close();
}


// Kill a pig and collect the dropped item: killMob(bot, \"pig\", 300);
async function killMob(bot, mobName, timeout = 300) {
    const entity = bot.nearestEntity(
        (entity) =>
            entity.name === mobName &&
            entity.position.distanceTo(bot.entity.position) < 32
    );
    await bot.pvp.attack(entity);
    await bot.pathfinder.goto(
        new GoalBlock(entity.position.x, entity.position.y, entity.position.z)
    );
}



At each round of conversation, I will give you
Code from the last round: ...
Execution error: ...
Chat log: ...
Biome: ...
Time: ...
Nearby blocks: ...
Nearby entities (nearest to farthest):
Health: ...
Hunger: ...
Position: ...
Equipment: ...
Inventory (xx/36): ...
Chests: ...
Task: ...
Context: ...
Critique: ...

You should then respond to me with
Explain (if applicable): Are there any steps missing in your plan? Why does the code not complete the task? What does the chat log and execution error imply?
Plan: How to complete the task step by step. You should pay attention to Inventory since it tells what you have. The task completeness check is also based on your final inventory.
Code:
    1) Write an async function taking the bot as the only argument.
    2) Reuse the above useful programs as much as possible.
        - Use `mineBlock(bot, name, count)` to collect blocks. Do not use `bot.dig` directly.
        - Use `craftItem(bot, name, count)` to craft items. Do not use `bot.craft` or `bot.recipesFor` directly.
        - Use `smeltItem(bot, name count)` to smelt items. Do not use `bot.openFurnace` directly.
        - Use `placeItem(bot, name, position)` to place blocks. Do not use `bot.placeBlock` directly.
        - Use `killMob(bot, name, timeout)` to kill mobs. Do not use `bot.attack` directly.
    3) Your function will be reused for building more complex functions. Therefore, you should make it generic and reusable. You should not make strong assumption about the inventory (as it may be changed at a later time), and therefore you should always check whether you have the required items before using them. If not, you should first collect the required items and reuse the above useful programs.
    4) Functions in the \"Code from the last round\" section will not be saved or executed. Do not reuse functions listed there.
    5) Anything defined outside a function will be ignored, define all your variables inside your functions.
    6) Call `bot.chat` to show the intermediate progress.
    7) Use `exploreUntil(bot, direction, maxDistance, callback)` when you cannot find something. You should frequently call this before mining blocks or killing mobs. You should select a direction at random every time instead of constantly using (1, 0, 1).
    8) `maxDistance` should always be 32 for `bot.findBlocks` and `bot.findBlock`. Do not cheat.
    9) Do not write infinite loops or recursive functions.
    10) Do not use `bot.on` or `bot.once` to register event listeners. You definitely do not need them.
    11) Name your function in a meaningful way (can infer the task from the name).

You should only respond in the format as described below:
RESPONSE FORMAT:
Explain: ...
Plan:
1) ...
2) ...
3) ...
...
Code:
```javascript
// helper functions (only if needed, try to avoid them)
...
// main function after the helper functions
async function yourMainFunctionName(bot) {
  // ...
}
```
````

Human Input为：
````javascript
Code from the last round: No code in the first round

Execution error: No error

Chat log: None

Biome: swamp

Time: noon

Nearby blocks: vine, oak_leaves, oak_log

Nearby entities (nearest to farthest): skeleton

Health: 11.0/20

Hunger: 17.0/20

Position: x=34.7, y=67.0, z=-50.4

Equipment: [None, None, None, None, None, None]

Inventory (0/36): Empty

Chests: None

Task: Mine 1 wood log

Context: You can mine one of oak, birch, spruce, jungle, acacia, dark oak, or mangrove logs.

Critique: None

````

ChatGPT-Completion为：
````javascript
", "Plan:
1) Use `exploreUntil(bot, direction, maxDistance, callback)` to find a tree.
2) Use `mineBlock(bot, name, count)` to mine the log.
3) Check the inventory to make sure you have the log.

Code:
```javascript
async function mineWoodLog(bot) {
  // 1. Find a tree
  const tree = await exploreUntil(bot, new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1), 60, () => {
    const log = bot.findBlock({
      matching: (block) => {
        return block.name.endsWith(\"_log\");
      },
      maxDistance: 32,
    });
    return log;
  });

  if (!tree) {
    bot.chat(\"Could not find a tree.\");
    return;
  }

  // 2. Mine the log
  await mineBlock(bot, tree.name, 1);

  // 3. Check the inventory
  const log = bot.inventory.items().find(item => item.name.endsWith(\"_log\"));
  if (!log) {
    bot.chat(\"Failed to mine the log.\");
    return;
  }

  bot.chat(`Mined 1 ${log.displayName}.`);
}
```
````

### Curriculum-LLM

课程学习过程的LLM对话同样跟Action一致，区别为首个任务为硬编码收集一棵树，其他任务为LLM生成任务，与ActionAgent类似。
```javascript
["Mine 1 wood log", "You can mine one of oak, birch, spruce, jungle, acacia, dark oak, or mangrove logs."]
```
