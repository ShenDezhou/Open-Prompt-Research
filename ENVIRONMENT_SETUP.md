# 基于MineCraftServer的智能交互系统搭建

* MAC环境下，安装openjdk20。
```shell
brew install openjdk
echo 'export PATH="/usr/local/opt/openjdk/bin:$PATH"' >> ~/.zshrc
```

* 下载MC服务器[mc-server-1.13.1](https://launcher.mojang.com/v1/objects/fe123682e9cb30031eae351764f653500b7396c9/server.jar)，
* 下载MC服务器[mc-server-1.18.1](https://launcher.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar)，

* 启动MC-Server服务

```shell
java -Xms1200m -Xmx1300m -jar server.jar nogui --singleplayer brian
```
>启动过程需要修改eula.txt中变量为true后，重启服务。

启动日志如下：
```python
[21:50:14] [Server thread/INFO]: Starting minecraft server version 1.13.1
[21:50:14] [Server thread/INFO]: Loading properties
[21:50:15] [Server thread/INFO]: Default game type: SURVIVAL
[21:50:15] [Server thread/INFO]: Generating keypair
[21:50:15] [Server thread/INFO]: Starting Minecraft server on *:25565
[21:50:15] [Server thread/INFO]: Using default channel type
[21:50:15] [Server thread/INFO]: Preparing level "world"
[21:50:15] [Server thread/INFO]: Found new data pack vanilla, loading it automatically
[21:50:15] [Server thread/INFO]: Reloading ResourceManager: Default
[21:50:15] [Server thread/INFO]: Loaded 524 recipes
[21:50:16] [Server thread/INFO]: Loaded 571 advancements
[21:50:19] [Server thread/INFO]: Preparing start region for dimension minecraft:overworld
[21:50:20] [Server thread/INFO]: Preparing spawn area: 0%
[21:50:28] [Server thread/INFO]: Time elapsed: 8803 ms
[21:50:28] [Server thread/INFO]: Done (13.488s)! For help, type "help"
```

# 登录MC-server服务器

使用单机模式登录。

```javascript
import mineflayer from 'mineflayer'

const bot = mineflayer.createBot({
  host: 'localhost', // minecraft server ip
  username: 'brian', // minecraft username
  auth: 'offline' // for offline mode servers, you can set this to 'offline'
  // port: 25565,                // only set if you need a port that isn't 25565
  // version: false,             // only set if you need a specific version or snapshot (ie: "1.8.9" or "1.16.5"), otherwise it's set automatically
  // password: '12345678'        // set if you want to use password-based auth (may be unreliable)
})
```

# 使用javascript库进行登录交互

```python
from javascript import require, On, Once, AsyncTask, once, off

mineflayer = require('mineflayer')

BOT_USERNAME = f'brian'

bot = mineflayer.createBot({ 'host': '127.0.0.1', 'username': BOT_USERNAME, 'auth': 'offline'})

# The spawn event
once(bot, 'login')
bot.chat('I spawned')
```

使用javascript、mineflayer登录服务器，执行动作。

# 使用mineflayer登录

```javascript
import mineflayer from 'mineflayer';
import { mineflayer as mineflayerViewer } from 'prismarine-viewer';

const bot = mineflayer.createBot({
  host: '127.0.0.1', // minecraft server ip
  username: 'brian', // minecraft username
  auth: 'offline' // for offline mode servers, you can set this to 'offline'
  // port: 25565,                // only set if you need a port that isn't 25565
  // version: false,             // only set if you need a specific version or snapshot (ie: "1.8.9" or "1.16.5"), otherwise it's set automatically
//   password: ''        // set if you want to use password-based auth (may be unreliable)
})

bot.on('chat', (username, message) => {
  if (username === bot.username) return
  console.log(username + ',' + message)
  bot.chat(message)
  console.log(bot.username + ',' + message)
})

// Log errors and kick reasons:
bot.on('kicked', console.log)
bot.on('error', console.log)

bot.on('connect', function () {
  console.info('connected')
})
bot.on('disconnect', function (packet) {
  console.log('disconnected: ' + packet.reason)
})

bot.once('spawn', () => {
  mineflayerViewer(bot, {
   port: 1024,
   firstPerson: true }) // if first person is false, you get a bird's-eye view
})
```

使用mineflayer登录，并用mineflayer-viewer在浏览器上以第一视角查看bot。
