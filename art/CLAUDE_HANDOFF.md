# 场景美术包：Claude 接入说明

## 当前交付与边界

此包基于仓库 `563e3d6`（Restyle the interface after Terraria），只提供场景美术及接入示例。没有改动 `index.html`、角色 PNG、世界地图、技能、存档或新的界面代码。**用户已否决重画的伊布和水伊布；请保持仓库原始角色造型、配色与绘制方式。**

含 84 张场景 PNG：森林 26、湖泊 20、洞穴 18、塔 18、通用 2。其中 12 张为横向循环视差背景；动画分为火把 4 帧、睡莲 3 帧、湖水表面 2 帧、洞穴水面 2 帧。全部资产由本包脚本按像素坐标生成，没有取用泰拉瑞亚的游戏图像。

`art/index.html` 是可离线打开的素材审阅页，包含四个区域构图示范和按区域分组的原尺寸素材目录。预览中的现有伊布仅作比例参照。它不是游戏关卡，也不包含新增玩法。

## 目录

| 路径 | 内容 |
|---|---|
| `sprites/deco/forest_*.png` | 树木、草和小型蘑菇 |
| `sprites/deco/biome_*.png` | 芦苇、石头、水晶、垂藤、柱子、灯与旗帜 |
| `sprites/deco/env_*.png` | 木屋、长椅、花盆、码头、独木舟、水草、大水晶与塔内机械等 |
| `sprites/tiles/{forest,biome,env}_*.png` | 16×16 瓦片与半透明水体 |
| `sprites/backgrounds/env_*.png` | 四个地区，每区三层，384×224，横向循环 |
| `art/manifest.json` | 每张 PNG 的资源 id、路径、尺寸、锚点、所属区域、哈希和动画 |
| `art/renderer-example.js` | 无依赖的绘制/动画/背景滚动示例，可按现有架构移植 |
| `tools/make_*assets.py`, `tools/make_environment_pack.py` | 素材源代码，固定种子，可重复生成 |
| `tools/build_art_catalog.py` | 生成 manifest 和内嵌资源的独立审阅页 |

## 最小接入路径

1. 将新增文件复制进仓库相同相对目录。不要用任何旧试玩版覆盖最新 `index.html`。
2. 运行 `python3 tools/embed_assets.py`，现有脚本会把新增分类下的 PNG 一并内嵌。素材包自身没有运行这步修改游戏。
3. 沿用现有 `loadAssets()` / `IMG`，按 manifest 中的 `id` 访问，例如 `IMG['deco/env_village_cottage']`。
4. 先接起点村：背景三层 → 后景树与房屋 → 地形 → 玩家/敌人 → 低密度前景草。房屋只是背景装饰，没有可进入内部或碰撞逻辑。
5. 湖泊采用 `biome_shore_*`、独木舟、码头、睡莲、水草；洞穴采用 `biome_cave_*`、水晶与岩柱；塔采用 `biome_tower_*`、旗帜、残柱和机械。
6. 用房间区域或瓦片所属区域选择材质，而不是用素材改变原碰撞类型。不要把危险砖或能力门替换成普通装饰而丢失识别性。
7. 接入后检查原始角色、九种形态能力、地图/背包界面、存档和移动端按钮。美术不应影响物理数值、碰撞或掉落随机序列。

## 坐标与渲染约定

- 原生 384×224 画面，16px 地形网格；不开抗锯齿，整数像素绘制，放大使用 nearest。
- PNG 采用 RGBA，普通直通 alpha。透明 PNG 不需要去底色。
- `anchor` 是相对于图片左上角的**像素边界坐标**。地面道具一般为 `[width/2,height]`，挂饰为 `[width/2,0]`，瓦片/背景为 `[0,0]`。底边锚点等于 height 是有意设计。
- 世界坐标绘制：`screenX = worldX - cameraX - anchor[0]`，Y 同理。移动摄像机时不要再给精灵增加第二次相机偏移。
- 背景绘制在地形前，按 layer_0 → layer_1 → layer_2 顺序，建议视差系数 `.12/.23/.38`，垂直底对齐。深处背景可以降低 alpha，保留可玩地形对比。
- 瓦片四变体用坐标哈希选择；不要逐帧调用 `Math.random()`，否则纹理闪烁并影响游戏概率。
- 水体 PNG 自带透明度，建议先以 `globalAlpha=1` 接入，避免与旧 `.65` 相乘导致水体过淡。水面两帧用 4fps；湖面反光可另叠加少量短线。
- 所有道具默认 `collision: none`。码头是 48×40 的视觉模块，如需站立，另在地图中定义一层平台；齿轮、拉杆、线圈、栅门尚无互动、状态或伤害实现。
- 火把 8fps、睡莲 3fps；使用游戏模拟时间计时，暂停时动画停止。帧尺寸与锚点一致。
- 视口裁剪要按完整图片包围盒判断，例如树为 80×112，木屋为 96×80，不能只看锚点是否在屏幕内。
- 凡代码改变 canvas alpha/composite 状态，应使用 save/restore，不影响后续角色和 UI。

## 重建

依赖 Python 3 和 Pillow。已经提交 PNG，可直接使用，不必重建。

```sh
python3 tools/make_forest_assets.py
python3 tools/make_biome_assets.py
python3 tools/make_environment_pack.py
python3 tools/build_art_catalog.py
python3 tools/validate_art_pack.py
# 完成系统接入后才执行，会上写游戏 index.html：
python3 tools/embed_assets.py
```

## 视觉验收重点

原角色保持不变；前景轮廓清晰；装饰不能冒充可站立的平台；蓝色水晶和黄色机关不要压过敌人/道具；灯光保持局部，不要全屏泛白；移动时背景接缝不能出现空列。没有做完整昼夜循环、真实动态遮挡光照或复杂水反射，这些可以由系统后续添加。

## 本次校验结果

- 84 张 PNG 的尺寸、RGBA 模式、SHA-256、锚点范围均通过验证；4 组动画帧尺寸/锚点一致。
- 三个素材生成器重新运行后，所有 PNG 哈希保持一致。
- 接入示例的锚点换算、动画循环、负相机位置下的背景循环和瓦片变体范围通过 `node tools/test_art_renderer.mjs`。
- 审阅页加载 84 张场景图片及 2 张原始角色比例参照；五个分类显示数量正确，浏览器无错误或警告；390px 手机模拟视口无横向溢出。
- 这是美术包的验证，新增素材尚未接入最新游戏系统，不能视为完整游戏测试。
