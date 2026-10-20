# 跨世代背景音乐来源

本游戏用 Web Audio 合成播放 MIDI 改编，不是官方原版录音。原作音乐归相应权利人，改编作者如下。

| 世代 | 曲目 | MIDI 来源 / 改编署名 |
|---|---|---|
| 1 | 真新镇 | [Joo *Johnnyz* Buaes](https://www.vgmusic.com/music/console/nintendo/gameboy/) |
| 2 | 自然公园 | [Katsumi No](https://www.vgmusic.com/music/console/nintendo/gameboy/) |
| 3 | 未白镇 | [Game Freak / pokeemerald-expansion contributors](https://github.com/rh-hideout/pokeemerald-expansion) |
| 3 | 丰缘 101 号道路 | [Game Freak / pokeemerald-expansion contributors](https://github.com/rh-hideout/pokeemerald-expansion) |
| 3 | 绿宝石标题曲 | [Game Freak / pokeemerald-expansion contributors](https://github.com/rh-hideout/pokeemerald-expansion) |
| 4 | 对战竹兰 | [TomTheTyranitar](https://www.vgmusic.com/music/console/nintendo/ds/) |
| 5 | 帆巴市 | [SawtoothOcean](https://www.vgmusic.com/music/console/nintendo/ds/) |
| 6 | 映雪市 | [Keiji Uotami](https://www.vgmusic.com/music/console/nintendo/3ds/) |
| 7 | 对战格拉吉欧 | [ShinkoNetCavy](https://www.vgmusic.com/music/console/nintendo/3ds/) |
| 8 | 对战彼特 | [LukeeGD / LukeZGD](https://github.com/LukeZGD/LukeZGD.github.io/blob/main/midi-files/index.html) |
| 8 | 伽勒尔 1 号道路 | [LukeeGD / LukeZGD](https://github.com/LukeZGD/LukeZGD.github.io/blob/main/midi-files/index.html) |
| 9 | 第零区 | [ColoredGreen](https://www.vgmusic.com/file/112ca80bb7adf111df23e2665a1e0370.html) |
| 原创 | 橡树下 | Claude 为本作作曲（`tools/compose_music.py`） |
| 原创 | 湖面 | Claude 为本作作曲（`tools/compose_music.py`） |
| 原创 | 雷电塔 | Claude 为本作作曲（`tools/compose_music.py`） |
| 原创 | 地洞 | Claude 为本作作曲（`tools/compose_music.py`） |
| 原创 | 风里的声音 | Claude 为本作作曲，引用「橡树下」的主题 |

进入游戏后首次点击或按键开启声音。底部「音乐」可选曲、调音量和静音；P 键快捷静音。
音乐偏好单独存储，不改变游戏存档。自动模式按场景选曲；同一区域循环后可切换下一首。

当前播放使用 Web Audio 的平滑谐波音色，区分键盘、吉他、贝斯、长笛、弦乐及简化打击乐，加入柔和的起落包络和高频滤波，不再播放 GBA 的短循环采样。`samples/` 中保留先前从本地 pokeemerald-expansion 取得的音色副本及来源记录，当前播放器不调用这些文件。

标「原创」的五首由 `tools/compose_music.py` 直接写成 MIDI，不改编任何已有作品，可以随游戏自由使用；改曲子就改这个脚本，再运行 `python3 tools/compose_music.py`。

修改 MIDI 后运行 `python3 tools/embed_music.py`；修改素材后运行 `python3 tools/unify_play_assets.py`、`python3 tools/embed_assets.py`、`python3 tools/build_art_catalog.py`。
