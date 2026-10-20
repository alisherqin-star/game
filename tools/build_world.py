# 世界构建：把每个房间的字符画拼成一张大地图，写出 levels/world.json 并嵌入 index.html。
# 用法：python3 tools/build_world.py
#
# 房间网格：每间 24x14 格，用 size=(宽, 高) 可以横向、纵向占多格，大房间里镜头连续滚动、不换页。
# 房间坐标可以是负数（往北、往西扩）。输出时整体平移到从 0 开始，平移量写进 world.json 的 ox / oy（单位：格），
# 游戏用「世界坐标 − 原点」给按坐标编号的实体和存档里的格子坐标编号，所以往外扩图不会让旧存档失效。字符含义：
#   地形  ' ' 空  '#' 泥土/地面  'r' 岩石  'b' 砖  'B' 塔石  'W' 木箱  '~' 水  'E' 电网  'S' 黑影墙
#         '^' 尖刺  '-' 单向平台  '_' 深渊（掉下去扣血回安全点）  'D' 锁门（集齐 8 种进化）  'K' 裂墙（雷伊布冲撞）  'L' 熔岩
#         'F' 电网，雷云打倒后关闭（捷径）  'H' 断掉的码头，湖蚌打倒后修好（变成单向平台，捷径）
#   实体  'P' 出生点  'e' 史莱姆  'v' 蝙蝠  'p' 刺河豚  'f' 跳跳蛙  'G' 大史莱姆 Boss  'M' 湖蚌 Boss  'Y' 雷云 Boss
#         '1' 水之石  '2' 雷之石  '3' 火之石  'm' 苔藓岩  'i' 冰岩（巨石要藏起来，用伊布的样子靠近才会进化）
#         'y' 迷路的小史莱姆（支线，计划放在夜之墓地的黑影墙后面）
#         'c' 金币  'h' 心之碎片  '*' 闪光石  's' 存档石  '!' 路牌  'N' 村民伊布
#         彩蛋：'T' 古代石板（刻着进化线索的谜语）  'o' 旧时代的果子（吃了回血但不会进化）
#         伙伴：'k' 贝儿出现的地点，notes 写 '步骤|角色'，例如 '1|slimes'（起点村的贝儿是 texts 里以「见习向导贝儿：」开头的村民）
#         RPG：'C' 宝箱（notes 写饰品 id，例如 'bell'）  'g' 商人被吹散的货物包  'u' 材料采集点（notes 写材料 id：berry 树果、spark 电光石）
#              'V' 走散的村民（notes 写 '谁|lost' 是在外面等人找，'谁|home' 是找到后回村站的位置）
#         '!' 和 'N' 的文字按出现顺序取 texts=[...]；'T'、'o'、'k'、'C'、'V'、'u' 的文字按出现顺序取 notes=[...]，
#         果子的写法是 '图片名|吃下时的话'，例如 'food_1_blueberry|……'。
#         彩蛋实体统一排在实体表最后，加新彩蛋不会改变已有实体的编号（旧存档仍然有效）。
#         'T' 'o' 'k' 'C' 'g' 'V' 'u' 的存档编号按坐标生成，移动它们只会影响它们自己。
#
# 装饰：room(..., deco=[(素材名, 列, 地面行[, 像素偏移]), ...])，素材名是 sprites/deco/ 下的文件名（不含 .png）。
#   图片底边中点对齐到「列」那一格的中间、「地面行」那一行的顶边，也就是站在这一行的地面上。
#   装饰只是画面，没有碰撞；画在地形后面。地面上的小草由游戏按坐标自动撒，不用写在这里。
import json, os, sys

RW, RH = 24, 14
T = 16
ROOMS = []
def room(pos, name, region, rows, texts=(), size=(1, 1), deco=(), notes=()):
    w, h = RW * size[0], RH * size[1]
    assert len(rows) == h, (name, len(rows))
    for i, r in enumerate(rows): assert len(r) == w, (name, i, len(r), r)
    for d in deco: assert 0 <= d[1] < w and 0 <= d[2] <= h, (name, d)
    ROOMS.append(dict(pos=pos, name=name, region=region, rows=rows, texts=list(texts), size=size, deco=list(deco), notes=list(notes)))

# ================= 起点村 =================
room((7, 2), '起点村', 'village', [
'                                                ',
' ----                                           ',
'                                                ',
' ----                  T                        ',
'                     ####                       ',
' ----                               c c c       ',
'            ####                  -------       ',
' ----                                           ',
'                                                ',
' ----                                           ',
'   T N   V  s    P  V    N      !    V    N     ',
'################################################',
'################################################',
'################################################'], texts=[
'村长奥斯卡：欢迎回家！东边的草原最近有大史莱姆出没，西边的湖没有水伊布的本事可过不去。',
'见习向导贝儿：我叫贝儿！听说伊布碰到进化石、靠近神奇的巨石就会进化。按 1～9 切换学会的形态，按 X 用技能……我、我想去糖果花园的星光野餐，可是风暴把路吹断了，我一个人不敢去。你会等我一起去吗？',
'路牌：← 湖泊（需要游泳）　　草原 →',
'商人玛姬：风暴把我的货吹得满地都是……收集金币和徽章吧，等路修好了，我这里会有好东西卖。',
], notes=['古代石板（其五）：「冷风从湖北的冰缝里吹出。霜雪覆盖的巨石，在那里等待伊布。」', '古代石板（其一）：「蔚蓝之石，映着池水的光。触碰它的伊布，会生出鱼鳍与长尾。」', 'grandma|home', 'scholar|home', 'trainer|home'], size=(2, 1), deco=[('forest_tree_0', 2, 11), ('env_village_home_elder', 8, 11), ('env_planter', 14, 11), ('forest_tree_1', 19, 11), ('env_fence', 22, 11), ('env_village_home_guide', 28, 11), ('env_bench', 35, 11), ('env_berry_bush', 37, 11), ('env_village_home_merchant', 41.5, 11), ('forest_tree_2', 46, 11)])

# ================= 草原 =================
room((9, 2), '草原·入口', 'plains', [
'                        ',
'             ----       ',
'                        ',
'          ----          ',
'                        ',
'            c c----     ',
'          -----         ',
'                    --- ',
'                  co    ',
'                 ###    ',
' k !      e    u      e ',
'##################    ##',
'##################    ##',
'##################-   ##'], texts=['路牌：踩在怪物头上可以打倒它。被碰到会掉血，血没了就回到存档石。'], notes=['food_1_blueberry|吃了一颗蓝莓，酸酸甜甜的。……伊布没有进化。看来进化可不是靠吃东西的。', '1|slimes', 'berry'], deco=[('forest_tree_0', 6, 11), ('forest_tree_1', 19, 11), ('env_berry_bush', 23, 11, -4)])
room((10, 2), '草原·坑洼', 'plains', [
'                        ',
'                        ',
'            T           ',
'           ----         ',
'                        ',
'       --        --     ',
'                        ',
'                        ',
'                     g  ',
'                     W  ',
'   e        v    c   W c',
'#####^^^#####^^^########',
'########################',
'########################'], notes=['古代石板（其八）：「解开一颗心结，换来一条缎带。哭泣的，未必是敌人。」'], deco=[('forest_tree_2', 2, 11), ('env_stump', 10, 11), ('env_berry_bush', 18, 11)])
room((10, 1), '草原·高崖', 'plains', [
'                        ',
'                        ',
'       h T              ',
'      ####              ',
'                        ',
'                        ',
'                ---     ',
'                        ',
'           ---          ',
'                        ',
'   WW                   ',
'   WW  ---              ',
'#######          #######',
'#######          #######'], texts=[], notes=['古代石板（其六）：「与伙伴在烈日下并肩作战。羁绊满溢时，额前会浮现红玉。」'], deco=[('forest_tree_0', 20, 12)])
room((11, 2), '草原·蝙蝠林', 'plains', [
'                        ',
'                ----    ',
'                        ',
'           ----         ',
'        v          v    ',
'                ----    ',
'              C       T ',
'     ---     ---     ---',
'                        ',
'         ---            ',
'   c  V   e  u   e    c ',
'##    ##################',
'##    ##################',
'##  --##################'], notes=['leaf', '古代石板（其七）：「与伙伴在月光下并肩作战。羁绊满溢时，周身会浮现金环。」', 'grandma|lost', 'berry'], deco=[('forest_tree_0', 2, 11), ('forest_tree_1', 8, 11), ('forest_tree_2', 14, 11), ('forest_tree_0', 20, 11, 4)])
room((12, 2), '草原·史莱姆王', 'plains', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'  !        G          g ',
'########################',
'########################',
'########################'], texts=['路牌：前方是大史莱姆的地盘！它每被踩一次就会分裂出一只小史莱姆。最近它特别暴躁，好像在找什么东西……'], deco=[('env_stump', 6, 11), ('env_berry_bush', 17, 11), ('forest_tree_1', 21, 11)], notes=[])
room((13, 2), '草原·池塘', 'plains', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'           1            ',
' su  !    ####       !  ',
'######~~~~####~~~~######',
'######~T~~####~~~~######',
'###############~~#######'], notes=['berry', '古代石板（其二）：「黄绿之石，困着一声惊雷。它嵌在湖水尽头的岩缝里。」'], texts=['路牌：池塘中央的小岛上闪着蓝光，是水之石！伊布碰到它就会进化成会游泳的水伊布，回头去西边的湖看看吧！', '路牌：→ 雷电塔。塔门的电网只有雷伊布能穿过。右边水塘的底下有股凉凉的水流，不知道通到哪里。'], deco=[('env_berry_bush', 3, 11), ('forest_tree_2', 20, 11)])
room((13, 1), '雷电塔·门口', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BB                    BB',
'BB   Cc          cT   BB',
'BB   ---        ---   BB',
'BB                    BB',
'BB          ----      BB',
'BB                    BB',
'BB  ---               BB',
'BBBBB      !     ---    ',
'BB  W                   ',
'BBT W                   ',
'BBBBBBBBB      BBBBBBBBB',
'BBBBBBBBB      BBBBBBBBB'], texts=['石碑：这里是雷电塔的门厅。从地板的缺口跳下去就是草原的池塘，往东回到中庭继续向上。'], notes=['bell', '古代石板（其三）：「赤红之石，供奉在高塔之巅。电网之后，火焰之前。」', '古代石板（其四）：「荆棘烧尽之处，青苔覆着巨石。伊布在它身旁醒来，耳尖冒出了嫩叶。」'], deco=[('biome_banner', 4, 2), ('biome_banner', 19, 2), ('biome_lamp', 2, 5, 6), ('biome_lamp', 21, 5, -6), ('env_torch_0', 7, 10), ('env_torch_0', 16, 10), ('biome_pillar', 3, 12), ('biome_pillar', 20, 12), ('env_gear', 5, 11), ('env_coil', 18, 12)])


# ================= 湖泊 =================
room((6, 2), '湖畔', 'lake', [
'                        ',
'               ----     ',
'                        ',
'                  ----  ',
'                        ',
'             ----       ',
'                        ',
'                  ----  ',
'                        ',
'             ----       ',
'   fHHHHHHHHH  s   ! u  ',
'###~~~~~~~~~~###########',
'###~~~~~~~~~~###########',
'###~~c~c~c~c~###########'], notes=['berry'], texts=['路牌：湖水又深又宽，没有水伊布过不去。'], deco=[('biome_reeds', 1, 11), ('env_river_stones', 14, 11), ('biome_reeds', 17, 11), ('env_lake_willow', 21, 11), ('env_bench', 21, 11), ('env_fern', 23, 11), ('env_mooring_post', 13, 11), ('env_canoe', 10, 11, 0, 4), ('env_lily_0', 5, 11, 0, 5), ('env_waterweed', 3, 14), ('env_waterweed', 11, 14)])
room((5, 2), '湖面', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'        c      c        ',
'      ---     ---       ',
'                        ',
'                        ',
'   f         f          ',
'  ---       ---         ',
'HHHHHHHHHHHHHHHHHHHHHHHH',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~p~~~~~~~~~~~~~~~~p~~'], deco=[('env_lily_0', 2, 11, 0, 5), ('env_lily_0', 18, 11, 0, 5), ('env_lily_0', 22, 11, 0, 5), ('env_waterweed', 1, 14), ('env_waterweed', 22, 14)])
room((5, 3), '湖底洞穴', 'lakecave', [
'rrrr~~~~~~~~~~~~~~~~rrrr',
'rrr~~~~~~~~~~~~~~~~~~rrr',
'rr~~~~~~~~~~~~~~~~~~~~rr',
'r~~~~p~~~~~~~~~~~~p~~~~r',
'r~~~~~~~~~rrrr~~~~~~~~~r',
'r~~~rrr~~~~~~~~~~rrr~~~r',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~c~~~~~~~~~~~~~~~~c~~~',
'~~~~~~~~~~~p~~~~~~~~~~~~',
'rrr~~~~~~~~~~~~~~~~~~rrr',
'rrrr~~~~~~~~~~~~~~~~rrrr',
'rrrrrr~~~~~~~~~~~~rrrrrr',
'rrrrrrrr~~~~*~~~rrrrrrrr',
'rrrrrrrrr~~~rrrrrrrrrrrr'], deco=[('env_stalactite', 3, 1), ('env_stalactite', 20, 1), ('biome_vine', 10, 0), ('biome_vine', 16, 0), ('biome_crystal_0', 10, 4), ('env_glow_mushrooms', 5, 5), ('biome_crystal_1', 18, 5), ('env_stalagmite', 3, 9), ('env_stalagmite', 20, 9), ('env_crystal_cluster', 8, 12), ('biome_crystal_1', 16, 12), ('env_glow_mushrooms', 14, 13), ('env_waterweed', 10, 13)])
room((4, 2), '湖心', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'           c            ',
'         -----          ',
'                        ',
'                        ',
'                        ',
'HHHfHHHHHHHHHHHHHHHHHHHH',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~p~~~~~~~~~~~~~p~~~~~',
'~~~~~~~~~~h~~~~~~~~~~~~~'], deco=[('env_lily_0', 5, 11, 0, 5), ('env_lily_0', 20, 11, 0, 5), ('env_waterweed', 2, 14), ('env_waterweed', 15, 14), ('env_river_stones', 21, 14)])
room((3, 2), '湖蚌洞', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~M~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~'], deco=[('env_lily_0', 1, 11, 0, 5), ('env_lily_0', 22, 11, 0, 5), ('env_waterweed', 3, 14), ('env_waterweed', 20, 14), ('biome_crystal_0', 5, 14), ('biome_crystal_1', 18, 14)])
room((2, 2), '柠檬岩', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'      2 V               ',
'    ######              ',
'  ! ######   s  u       ',
'####################~~~~',
'####################~~~~',
'####################~~~~'], texts=['路牌：岩缝里嵌着雷之石！伊布碰到它就会进化成雷伊布，冲过草原尽头的电网。'], notes=['trainer|lost', 'berry'], deco=[('biome_reeds', 18, 11), ('env_mooring_post', 19, 11), ('env_lily_0', 22, 11, 0, 5), ('env_waterweed', 23, 14), ('env_boulder', 8, 11), ('env_river_stones', 15, 11), ('env_fern', 0, 11), ('biome_reeds', 3, 11), ('biome_pebbles', 9, 9), ('env_lake_willow', 11, 11)])

# ================= 雷电塔内部（新房间放在最后，已有房间和实体的编号不变，旧存档仍然有效） =================
# 中庭：三屏高的竖井，一路往上爬不换页。塔基西墙是电网门（只有雷伊布能穿过），东墙裂墙后藏着心之碎片。
# 台阶每级两格高，所有形态都爬得上去（普通跳 45.8 像素，三格 48 像素只有雷伊布跳得上）。地板东边的格栅下面是老水道的出水口，水伊布从池塘游过来。
room((14, 0), '雷电塔·中庭', 'tower', [
'BBBBBBBBBBBBBBBBBB  BBBB',
'BBBBBBBBBBBBBBBBBB  BBBB',
'BB                    BB',
'BB                    BB',
'BB    c c c c c C     BB',
'BB    -----------     BB',
'BB                    BB',
'BB  ----         v      ',
'BB                      ',
'BB         ----         ',
'BB                 u    ',
'BB               BBBBBBB',
'BB                    BB',
'BB           ----     BB',
'BB                    BB',
'BB      ----          BB',
'BB                    BB',
'BB ----               BB',
'BB                    BB',
'BB      ----          BB',
'BB      EEE             ',
'BB           ---- v     ',
'BB                 c    ',
'                  ----BB',
'                      BB',
'    u        ----     BB',
'BBBBBB                BB',
'BB      ----          BB',
'BB                    BB',
'BB           ----     BB',
'BB                      ',
'BB      ----     v      ',
'BB                      ',
'BB ----          -----BB',
'BB                    BB',
'BB      -------       BB',
'FF           ccc      BB',
'FF           ----     K ',
'FF  s   !            gKh',
'BBBBBBBBBBBBBBBBB--BBBBB',
'BBBBBBBBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBBBBBBB~~BBBBB'], texts=['石碑：雷电塔。风暴那晚之后，塔里的电网就一直失控，只有雷伊布能穿过。地板下面是老水道，以前塔靠池塘的水降温。一直往上爬，高层供奉着一颗火之石；塔顶上空盘着一团雷云。'], size=(1, 3), deco=[
    ('env_coil', 20, 39), ('env_torch_0', 2, 33), ('env_torch_0', 21, 30), ('env_lever', 4, 26),
    ('env_gear', 20, 18), ('env_torch_0', 2, 19), ('env_torch_0', 21, 15), ('env_torch_0', 2, 7)], notes=['magnet', 'spark', 'spark'])

# 火之祭坛：两屏宽的大厅，镜头连续横移。东墙的门通线圈井，一路往上到塔顶。电网帘子挡住不是雷伊布的形态，尽头的祭坛上是火之石。
# 帘子下面是一道水沟：雷伊布走中间的石桥穿过电网，水伊布从桥下潜过去（电网的第二把钥匙）。
room((15, 0), '雷电塔·火之祭坛', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BB                                            BB',
'BB                                            BB',
'BB                          c c c             BB',
'BB                         -------            BB',
'BB              v                     v         ',
'                    E                           ',
'                    E                           ',
'                    E                     3   BB',
'    s   u   !   V   E        f   o   BBBBBBBBBBB',
'BBBBBBBBBBBBBB~~~BBBBBBB~~~BBBBBBBB^^BBBBBBBBBBB',
'BBBBBBBBBBBBBB~~~~~~~~~~~~~BBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBB~~~~~~~~~~~~~BBBBBBBBBBBBBBBBBBBBB'], texts=['石碑：火之石就供奉在大厅尽头。让伊布碰到它，伊布就会进化成浑身火焰的火伊布。'], notes=['spark', 'scholar|lost', 'food_3_chili|咬了一口辣椒！伊布辣得直吐舌头……但还是没有进化。火之石就在大厅尽头。'], size=(2, 1), deco=[
    ('env_torch_0', 6, 9), ('biome_pillar', 9, 11), ('env_coil', 17, 11), ('env_gear', 24, 4),
    ('env_torch_0', 26, 9), ('biome_pillar', 33, 11), ('env_torch_0', 41, 8), ('env_lever', 44, 10)])

# 老水道：池塘右边水塘的底下通到中庭地板的出水口，整段泡在水里，只有水伊布游得过去（不会游泳的形态憋气只有 2.5 秒）。
# 这是雷电塔的第二个入口：塔门电网要雷伊布，这里要水伊布（DESIGN.md 第 2 节「雷电塔走塔门电网（雷）或从池塘水底游进塔基（水）」）。
room((13, 3), '雷电塔·老水道', 'tower', [
'BBBBBBBBBBBBBBB~~BBBBBBBBBBBBBBBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBBBBB~~BBBBBBBBBBBBBBBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBB~~~~~~~~~~~~~~~~BBBBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBB~~c~~~~~~c~~~~~~BBBBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBB~~~~~~~~~~~~~~~~~BBBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB~~~~~~BBBBBBBBBBB~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBB~~~~~~~BB~~~~~~~~BBB~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBB~~~~p~~BB~~~~~~~~BBB~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBB~~c~~~~~~~~~c~~~~~~~~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBB~~~~~~~~~~~~~~p~~~~~~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBB~~~~~~~~~~~~~~~~~~~~~~BBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBB~~h~u~BBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'], notes=['spark'], size=(2, 1), deco=[
    ('env_waterweed', 13, 5), ('env_waterweed', 22, 11), ('env_waterweed', 36, 11), ('env_gear', 18, 2), ('biome_crystal_0', 31, 6)])


# ================= 雷电塔扩建（第二阶段标杆：28 屏）=================
# 线圈井：火之祭坛东边的竖井，五屏高，一路爬到塔顶。台阶每级两格，所有形态都上得去；墙上的电流跳歪了会碰到。
# 侧门：齿轮回廊（西，第 -1 层，第 49～51 行）、发电室（西，第 -2 层，第 33～35 行，第二圈）、塔顶（西，第 -4 层）。东墙裂缝后面是雷伊布的闪光石。
room((17, -4), '雷电塔·线圈井', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BB                    BB',
'BB                    BB',
'BB                    BB',
'BB                    BB',
'BB                    BB',
'                      BB',
'                      BB',
'    s  !              BB',
'BBBBBBBBB             BB',
'BB                    BB',
'BB       -----        BB',
'BB         c          BB',
'BB -----              BB',
'BB                    BB',
'BB       ----         BB',
'BB EEEE               BB',
'BB             -----  BB',
'BB                    BB',
'BB       -----        BB',
'BB                    BB',
'BBBBBBB  ----         BB',
'BB                    BB',
'BB            -----   BB',
'BB          v         BB',
'BB       -----        BB',
'BB   c         E      BB',
'BB -----       E      BB',
'BB                    BB',
'BB       -----        K ',
'BB                    K*',
'BB             -------BB',
'                      BB',
'          ----        BB',
'           c          BB',
'BBBBBBBB-             BB',
'BB                    BB',
'BB        -----       BB',
'BB                    BB',
'BB              ----- BB',
'BB    v               BB',
'BB        ----        BB',
'BB    u               BB',
'BB  -----             BB',
'BB                   EBB',
'BB        -----      EBB',
'BB               c    BB',
'BB             -----  BB',
'                      BB',
'         -----        BB',
'                      BB',
'BBBBBBB               BB',
'BB                    BB',
'BB        -----       BB',
'BB                    BB',
'BB             -----  BB',
'BB          v         BB',
'BB       ----         BB',
'BB   c                BB',
'BB -----              BB',
'BB                    BB',
'BB       -----        BB',
'                      BB',
'               -----  BB',
'                      BB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BB                    BB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB'], texts=['石碑：线圈井。风暴那晚，雷云往塔里灌电，线圈到现在还在噼啪乱响。再往上就是塔顶。'], notes=['spark'], size=(1, 5), deco=[('env_coil', 20, 66), ('env_torch_0', 2, 58), ('env_coil', 3, 52), ('env_gear', 20, 44), ('env_torch_0', 21, 36), ('env_coil', 2, 22), ('env_gear', 18, 14), ('env_torch_0', 2, 10)])
# 塔顶：三屏宽的 Boss 房，雷云（Y）在头顶来回放雷。打倒以后塔基的电网（中庭的 F）关闭，奖励雷云坠饰。
# 地板西边的洞掉进储电室，再从储电室掉回中庭，是回塔底的捷径。
room((14, -4), '雷电塔·塔顶', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BB                                                                    BB',
'BB                                                                    BB',
'BB                                  Y                                 BB',
'BB                               ------                               BB',
'BB                                                                    BB',
'BB                                                                    BB',
'BB                  -----                     -----                     ',
'BB                                                                      ',
'BB                                                                      ',
'BB    !                                                                 ',
'BBBBBBBBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'], texts=['石碑：塔顶。雷云盘在头顶，地板上的洞通往下面的储电室。'], size=(3, 1), deco=[('biome_pillar', 4, 11), ('env_coil', 14, 11), ('env_coil', 30, 11), ('biome_pillar', 42, 11), ('env_coil', 56, 11), ('biome_pillar', 66, 11), ('biome_banner', 22, 1), ('biome_banner', 48, 1)])
# 储电室：三屏高。上面接塔顶地板的洞，下面的洞掉进中庭（只能往下，是捷径）；东门是齿轮回廊。
# 顶上的平台放着一堆金币，要从下面一级一级爬上去。
room((14, -3), '雷电塔·储电室', 'tower', [
'BBBBBBBBBB  BBBBBBBBBBBB',
'BBBBBBBBBB  BBBBBBBBBBBB',
'BB                    BB',
'BB                    BB',
'BB                    BB',
'BB         c c c      BB',
'BB    BBBBBBBBBB      BB',
'BB                    BB',
'BB---                 BB',
'BB                    BB',
'BB----                BB',
'BB        c           BB',
'BB      -----         BB',
'BB  v                 BB',
'BB            -----   BB',
'BB                    BB',
'BB      -----         BB',
'BB  c                 BB',
'BB-----               BB',
'BB                    BB',
'BB      -----         BB',
'BB                    BB',
'BB            -----   BB',
'BB        c           BB',
'BB      -----         BB',
'BB                    BB',
'BB-----               BB',
'BB                    BB',
'BB      -----         BB',
'BB              v     BB',
'BB            -----   BB',
'BB                    BB',
'BB      -----         BB',
'BB                    BB',
'BB-----               BB',
'BB                      ',
'BB      -----           ',
'BB  !                   ',
'BBBBBBBBBBBBBBBBBB  BBBB',
'BB                    BB',
'BBBBBBBBBBBBBBBBBB  BBBB',
'BBBBBBBBBBBBBBBBBB  BBBB'], texts=['石碑：储电室。地板东边的洞直通中庭，从这里掉下去最快回到塔底。'], size=(1, 3), deco=[('env_coil', 3, 38), ('env_coil', 21, 38), ('env_gear', 20, 28), ('env_torch_0', 21, 20), ('env_gear', 3, 12), ('env_coil', 14, 6)])
# 齿轮回廊：两屏宽的矮走廊，东接线圈井，西接储电室。两道木箱墙一直顶到天花板，要火伊布烧掉或雷伊布冲刺撞开。
room((15, -1), '雷电塔·齿轮回廊', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'           c   W                W   c           ',
'          ---- W                W -----         ',
'               W        v       W               ',
'               W                W               ',
'      u        W           f    W               ',
'BBBBBBBBBBBBBBBBBBBBBBEEEBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'], notes=['spark'], size=(2, 1), deco=[('env_gear', 4, 10), ('env_gear', 20, 10), ('env_lever', 27, 10), ('env_gear', 43, 10), ('env_torch_0', 9, 5), ('env_torch_0', 38, 5)])
# 发电室：第二圈回访。冷却水管断了，中间是十几格宽的深坑：太阳伊布从东边的高台滑过去，或者冰伊布冻住坑上飞的蝙蝠踩过去。
# 西边是发电机（以后放雷伊布的强化「电磁飞檐」），现在先放一片心之碎片。
room((15, -3), '雷电塔·发电室', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                            BB',
'BB                                       c    BB',
'BB                                     ------ BB',
'BB                                  c         BB',
'BB                                -----       BB',
'BB                                            BB',
'BB                                      ------BB',
'BB                                            BB',
'BB                                 -----      BB',
'BB                                              ',
'BB                                      -----   ',
'BB   h   !        v      v                      ',
'BBBBBBBBBBBBB                 BBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBB                 BBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBB                 BBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBB                 BBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBB_________________BBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBB_________________BBBBBBBBBBBBBBBBBB'], texts=['石碑：发电机停了。等它重新转起来，雷伊布也许能学会贴着墙跑。'], size=(2, 2), deco=[('env_coil', 4, 22), ('env_gear', 7, 22), ('env_coil', 10, 22), ('env_gear', 33, 22), ('env_lever', 44, 22), ('env_torch_0', 31, 12)])
# 东翼：中庭东墙外的机房，从中庭第 23 行的台子往东走进来。地上的洞掉进南门。
room((15, 1), '雷电塔·东翼', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BB                                            BB',
'BB                                            BB',
'BB                            v               BB',
'BB                u                         c BB',
'                -----        W            ----BB',
'            c               WW                BB',
'          -----             WW      -----     BB',
'BB                    f     WW   c            BB',
'BBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBB  BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'], notes=['spark'], size=(2, 1), deco=[('env_coil', 8, 10), ('env_gear', 24, 10), ('env_coil', 34, 10), ('env_gear', 44, 10), ('env_torch_0', 15, 6), ('env_torch_0', 39, 6)])
# 南门：雷电塔往南去火山洞的门。现在被落石堵着，火山洞做好以后从这里往下接。
room((15, 2), '雷电塔·南门', 'tower', [
'BBBB  BBBBBBBBBBBBBBBBBB',
'BBBB  BBBBBBBBBBBBBBBBBB',
'                      BB',
'                      BB',
'                      BB',
'BBBBBB                BB',
'BBBBBB  ----          BB',
'BBBBBB                BB',
'BBBBBB        ----    BB',
'BBBBBB                BB',
'BBBBBB   ----     rrrrBB',
'BBBBBB  c   !  c  rrrrBB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB'], texts=['路牌：↓ 火山洞。风暴吹落的大石头把路堵死了，得等人来搬开。'])


# ================= 草原扩建（第二阶段标杆：连起点村 30 屏）=================
# 地面一层（起点村、入口、坑洼、蝙蝠林、史莱姆王、池塘）往上叠了三层山坡，往下挖了两间地洞。
# 上下两层之间靠下面房间天上的木板爬上去，上面房间的地上留一个口；所有形态都走得通，台阶每级两格。
# 起点村·大橡树坡：村子北边的山坡，村口那棵大橡树就在这里（剧本第 3.7 节奥斯卡傍晚站的地方）。
# 从村子西头的木板爬上来；东边接草原·西坡，天上的木板通花田。树下的宝箱是奥克利橡果。
room((7, 1), '起点村·大橡树坡', 'village', [
'                                                ',
'                                      ----      ',
'                                   c            ',
'                                  ----          ',
'                                       c        ',
'                      v               ----      ',
'                                                ',
'                                  ----          ',
'                                       c        ',
'            #####                     ----      ',
'            #####  !   C      e                 ',
'     ###########################################',
'     ###########################################',
' ----###########################################'], texts=['石碑：大橡树。三百年前，奥克利家的佩妮在这里种下一颗橡果。'], notes=['acorn'], size=(2, 1), deco=[('forest_tree_2', 23, 11), ('forest_tree_0', 8, 11), ('env_bench', 27, 11), ('flower', 33, 11), ('flower', 44, 11), ('bush', 14, 8), ('forest_tree_1', 45, 11)])
# 草原·花田：大橡树坡上面。西边以后接湖泊北岸，东边接风车坡。
room((7, 0), '草原·花田', 'plains', [
'                                                ',
'                                                ',
'                                                ',
'                                                ',
'                    v                           ',
'                                                ',
'                         c c                    ',
'              c         -----                   ',
'               e                                ',
'            #######                             ',
'        u   #######           e                 ',
'####################################         ###',
'####################################         ###',
'####################################  ----   ###'], notes=['berry'], size=(2, 1), deco=[('flower', 3, 11), ('flower', 6, 11), ('flower', 21, 11), ('flower', 33, 11), ('bush', 15, 9), ('forest_tree_1', 46, 11), ('env_fern', 30, 11)])
# 草原·西坡：草原入口上面。从入口天上的木板爬上来，西接大橡树坡，往上通风车坡。东边是土崖（高崖要从别的路去）。
room((9, 1), '草原·西坡', 'plains', [
'      ----            ##',
'                      ##',
'        ----          ##',
'    c                 ##',
'   ----               ##',
'         c     v      ##',
'        ----          ##',
'    c                 ##',
'   ----               ##',
'  e                   ##',
'###########        #####',
'###########    ----#####',
'###########        #####',
'###########----    #####'], deco=[('forest_tree_0', 20, 10), ('bush', 1, 10)])
# 草原·风车坡：两屏宽的山坡，有存档石。西接花田，东接果园；西坡从地上的口爬上来，天上的木板通北崖。地面盖住了高崖。
room((9, 0), '草原·风车坡', 'plains', [
'                                                ',
'                                     ----       ',
'                                   c            ',
'                                  ----          ',
'                                                ',
'                    v                 ----      ',
'                                   c            ',
'                                  ----          ',
'                           e                    ',
'                        ########      ----      ',
'                s   !   ########            e   ',
'######     #####################################',
'######     #####################################',
'######---- #####################################'], texts=['石碑：风车坡。风暴那晚之后，风车就没停过，转得嘎吱嘎吱响。'], size=(2, 1), deco=[('exp_wind_windmill', 28, 9), ('forest_tree_2', 4, 11), ('bush', 12, 11), ('flower', 33, 11), ('forest_tree_1', 45, 11)])
# 草原·北崖：草原最北边的岩坡。地上一排木箱盖着个小坑，火伊布烧开（或雷伊布跑过去撞碎）能拿到心之碎片。
room((9, -1), '草原·北崖', 'plains', [
'##                                              ',
'##                                              ',
'##                                              ',
'##                                              ',
'##                      v                       ',
'##     c                                        ',
'##                                              ',
'##    rrr   c e                                 ',
'##    rrr                   e                   ',
'##  rrrrrrr               rrrrr                 ',
'## !rrrrrrr               rrrrr             u   ',
'####################WWW#############      ######',
'#################### h #############      ######',
'#################################### ---- ######'], texts=['路牌：北崖。再往北就是森林，路在瀑布那边。'], notes=['berry'], size=(2, 1), deco=[('env_boulder', 17, 11), ('forest_tree_2', 33, 11), ('env_fern', 24, 11), ('forest_tree_0', 46, 11)])
# 草原·瞭望台：望远镜在台子上。剧情伏笔：东边的风暴。
room((11, -1), '草原·瞭望台', 'plains', [
'                        ',
'                        ',
'                        ',
'     v                  ',
'                        ',
'                        ',
'         c  !  c        ',
'        ---------       ',
'                        ',
'   ----                 ',
'                    e   ',
'########################',
'########################',
'########################'], texts=['石碑：瞭望台。天气好的时候，往东能看到很远很远的地方。最近东边的天上，总卷着一团风暴……'], deco=[('exp_wind_telescope', 12, 7), ('forest_tree_1', 21, 11), ('bush', 2, 11)])
# 草原·森林边缘：瀑布从上面的瀑布顶冲下来，落进地上的水塘。水伊布能逆着瀑布游上去（二十多格高，不会游泳的憋不住气）。
# 西接瞭望台，东接东坡顶。
room((12, -1), '草原·森林边缘', 'plains', [
'               ~~       ',
'               ~~       ',
'               ~~       ',
'               ~~       ',
'               ~~       ',
'               ~~       ',
'        v      ~~       ',
'               ~~       ',
'   c           ~~   c   ',
'  ---          ~~  ---  ',
'    !          ~~    e  ',
'############~~~~~~~~####',
'############~~~~~~~~####',
'########################'], texts=['路牌：森林边缘。瀑布从山上冲下来，上面就是森林高台。'], deco=[('forest_tree_2', 7, 11), ('forest_tree_0', 22, 11), ('env_fern', 11, 11), ('env_fern', 20, 11)])
# 草原·瀑布顶：瀑布的源头，奖励一堆金币。以后从这里往北接森林高台（现在吊桥断了）。
room((12, -2), '草原·瀑布顶', 'plains', [
'                        ',
'                        ',
'  c                  c  ',
'   c c c!               ',
'############~~~~~~~~####',
'############~~~~~~~~####',
'############~~~~~~~~####',
'###############~~#######',
'###############~~#######',
'###############~~#######',
'###############~~#######',
'###############~~#######',
'###############~~#######',
'###############~~#######'], texts=['路牌：↑ 森林高台。风暴把吊桥吹断了，现在还过不去……'], deco=[('forest_tree_1', 21, 4), ('env_stump', 3, 4)])
# 草原·东坡：两屏高，贴着雷电塔的西墙。下面西接小溪，上面西接森林边缘。
room((13, -1), '草原·东坡', 'plains', [
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'                     BBB',
'   u                 BBB',
'##########           BBB',
'##########           BBB',
'##########----       BBB',
'              c      BBB',
'             ----    BBB',
'                     BBB',
'                 ----BBB',
'        v     c      BBB',
'             ----    BBB',
'                     BBB',
'                 ----BBB',
'              c      BBB',
'             ----    BBB',
'      e          !   BBB',
'#####################BBB',
'#####################BBB',
'#####################BBB'], texts=['石碑：雷电塔的外墙。墙缝里还在冒火花。'], notes=['berry'], size=(1, 2), deco=[('forest_tree_0', 4, 25), ('bush', 18, 25), ('forest_tree_1', 5, 11)])
# 草原·北坡：蝙蝠林上面。从蝙蝠林天上的木板爬上来；东接蘑菇丘，往上通果园。西边是土崖（挡着高崖）。
room((11, 1), '草原·北坡', 'plains', [
'##                      ',
'##    ----              ',
'## c                    ',
'##----                  ',
'##             v        ',
'##    ----              ',
'##                      ',
'##----                  ',
'##     c                ',
'##    ----              ',
'##                  e   ',
'############      ######',
'############      ######',
'############ ---- ######'], deco=[('forest_tree_2', 21, 11), ('bush', 9, 11)])
# 草原·蘑菇丘：史莱姆王上面（地面挡住 Boss 房）。西接北坡，天上的木板通小溪。
room((12, 1), '草原·蘑菇丘', 'plains', [
'                      ##',
'                  ----##',
'                      ##',
'                    --##',
'                 c    ##',
'                ----  ##',
'                      ##',
'                    --##',
'                 c    ##',
'                ----  ##',
'    !  u  e           ##',
'########################',
'########################',
'########################'], texts=['路牌：蘑菇丘。罗丝奶奶最喜欢来这里采蘑菇。'], notes=['berry'], deco=[('forest_plant_0', 2, 11), ('forest_plant_1', 8, 11), ('forest_plant_2', 13, 11), ('bush', 15, 11), ('env_stump', 11, 11)])
# 草原·果园：两处树果采集点。西接风车坡，东接小溪；北坡从地上的口爬上来。
room((11, 0), '草原·果园', 'plains', [
'                        ',
'                        ',
'                        ',
'          v             ',
'                        ',
'                   c    ',
'                  ----  ',
'               c        ',
'             -----      ',
'                        ',
'   e          u      u  ',
'######     #############',
'######     #############',
'######---- #############'], notes=['berry', 'berry'], deco=[('env_berry_bush', 13, 11), ('env_berry_bush', 17, 11), ('env_berry_bush', 21, 11), ('forest_tree_2', 2, 11)])
# 草原·小溪：水塘底下一条十格长的暗水道，只有水伊布游得到尽头的金币。
# 西接果园，东接东坡；蘑菇丘从地上的口爬上来。
room((12, 0), '草原·小溪', 'plains', [
'                        ',
'                        ',
'                        ',
'                        ',
'          v             ',
'                        ',
'                        ',
'                        ',
'                        ',
'            c c         ',
'  !                     ',
'#####~~~~##########    #',
'#####~~~~~~~~p~~~~#    #',
'#####~~~~~~~~~~c~c#--  #'], texts=['路牌：小溪。水塘底下好像有条暗道，一直通到土里。'], deco=[('biome_reeds', 4, 11), ('biome_reeds', 9, 11), ('forest_tree_0', 15, 11), ('bush', 23, 11)])
# 草原·兔子洞：草原入口地上的洞下来。地上一排木箱盖着个坑，火伊布烧开（或雷伊布跑过去撞碎）能拿到伊布的闪光石。东接蘑菇洞。
room((9, 3), '草原·兔子洞', 'burrow', [
'rrrrrrrrrrrrrrrrrr    rrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrr    rrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrr   -rrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrr    rrrrrrrr           rrrrrrr',
'rrrrrrrrrrrrrrrrrr-   rrrrrrrr        c  rrrrrrr',
'rr                            rrrr              ',
'rr                  ---              v          ',
'rr                                              ',
'rr             ---       c c c                  ',
'rr        e                       e             ',
'rrrrrrWWWWWWrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrr      rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrr   *  rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'], size=(2, 1), deco=[('env_glow_mushrooms', 12, 10), ('env_stalactite', 26, 5), ('env_glow_mushrooms', 40, 10)])
# 草原·蘑菇洞：有存档石。西接兔子洞，西头的竖井一级一级爬上蝙蝠林。
room((11, 3), '草原·蘑菇洞', 'burrow', [
'rr    rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rr--  rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rr    rrrrrrrrrrrr             rrrrrrrrrrrrrrrrr',
'rr  --rrrrrrrrrrrr  c   c   c  rrrrrrrrrrrrrrrrr',
'rr    rrrrrrrrrrrr             rrrrrrrrrrrrrrrrr',
'  --                  rrrrr                  rrr',
'                              v              rrr',
'      ---                                    rrr',
'                                             rrr',
'            e       s                 e   !  rrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'], texts=['路牌：蘑菇洞。罗丝奶奶说，这里的发光蘑菇晚上能当灯用。'], size=(2, 1), deco=[('env_glow_mushrooms', 9, 10), ('env_glow_mushrooms', 16, 10), ('env_glow_mushrooms', 33, 10), ('env_stalactite', 14, 5), ('env_stalactite', 36, 5)])


# ================= 湖泊扩建（第二阶段标杆：含湖底洞穴 28 屏）=================
# 水面一层往上叠了两层（东岸、栈道、浮岛、柠檬岩上空、西崖顶；北岸高地、观鸟台、东北坡），往西到西岸和西瀑布，
# 水下挖了一圈洞（码头下、湖心深处、蚌壳湾、沉木、西水洞）和更深的湖底深渊。上面两层从村子、花田就能走到，
# 但跟柠檬岩之间隔着水，雷之石仍然要水伊布才拿得到；水下全部要游泳。湖蚌打倒后湖畔到湖心的水面上出现木栈道（H）。
# 湖泊·东岸：湖畔天上的木板爬上来；西接栈道，往上通东北坡。东边是土崖（挡着大橡树坡的口子）。
room((6, 1), '湖泊·东岸', 'lake', [
'                      ##',
'    ----              ##',
'                      ##',
'       ----           ##',
'    c                 ##',
'   ----               ##',
'                      ##',
'       ----           ##',
'    c                 ##',
'   ----               ##',
' !         f        u ##',
'##############      ####',
'##############      ####',
'############## ---- ####'], texts=['路牌：湖泊·东岸。往西有条旧栈道，能走到湖中间的浮岛。'], notes=['berry'], deco=[('env_lake_willow', 12, 11), ('biome_reeds', 21, 11), ('env_mooring_post', 2, 11)])
# 湖泊·东北坡：东接草原·花田，西接观鸟台；东岸从地上的口爬上来。
room((6, 0), '湖泊·东北坡', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'            c    c      ',
'               f        ',
'             ####       ',
'             ####    c  ',
'###      ###############',
'###      ###############',
'### ---- ###############'], deco=[('forest_tree_1', 20, 11), ('biome_reeds', 10, 11)])
# 湖泊·观鸟台：高处鸟窝里的金币离台子四格高，要叶伊布二段跳（雷伊布跳起来也够得着）。
room((5, 0), '湖泊·观鸟台', 'lake', [
'                        ',
'                        ',
'               c c c    ',
'                ---     ',
'                        ',
'                        ',
'         c ! c          ',
'         ------         ',
'                        ',
'    ----                ',
'  f                 u   ',
'########################',
'########################',
'########################'], texts=['石碑：观鸟台。水鸟都被风暴吹跑了，只剩高处那个空鸟窝。'], notes=['berry'], deco=[('exp_canopy_basket', 17, 3), ('env_lake_willow', 21, 11)])
# 湖泊·北岸高地：两屏宽，有存档石。西头的岩壁上是冰缝（石板其五「冷风从湖北的冰缝里吹出」），以后从这里往北接冰窟。
room((3, 0), '湖泊·北岸高地', 'lake', [
'######                                          ',
'##  ##                                          ',
'##  ##                                          ',
'##  ##                                          ',
'##  ##                                          ',
'##  ##                                          ',
'##                                              ',
'##                                              ',
'##                                c c           ',
'######                          -------         ',
'######  !       f     u       s           f     ',
'################################################',
'################################################',
'################################################'], texts=['路牌：冰缝。冷风从里面呼呼地吹出来，往上还能爬，可伊布现在还上不去。'], notes=['berry'], size=(2, 1), deco=[('exp_ice_icespark_0', 3, 6), ('forest_tree_2', 12, 11), ('forest_tree_0', 26, 11), ('forest_tree_1', 45, 11), ('env_boulder', 19, 11)])
# 湖泊·栈道：湖面上空的旧木栈道，有两处断口。东接东岸，西接浮岛；掉下去就是湖面。
room((5, 1), '湖泊·栈道', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'       cc      cc       ',
'                        ',
'    f              f    ',
'-------  ------  -------',
'                        ',
'                        '], deco=[('env_mooring_post', 12, 11)])
# 湖泊·浮岛：五块浮在天上的土块。最高那块离旁边四格高，上面的心之碎片要叶伊布。掉下去是湖心和湖蚌洞的水。
room((3, 1), '湖泊·浮岛', 'lake', [
'                                                ',
'                                                ',
'                                                ',
'                                                ',
'                    h                           ',
'                  #####                         ',
'                  #####                         ',
'                                                ',
'    u  !                    c c                 ',
'###########               ########              ',
'###########       f       ########        f     ',
'###########   #########              ###########',
'              #########              ###########',
'                                                '], texts=['路牌：浮岛。风暴把湖边的土块卷到了天上，到现在还没落下来。'], notes=['berry'], size=(2, 1), deco=[('forest_tree_0', 3, 9), ('bush', 20, 11), ('biome_reeds', 30, 9), ('forest_tree_1', 44, 11), ('flower', 21, 5)])
# 湖泊·柠檬岩上空：柠檬岩上面的岩台，地面整块挡住柠檬岩（雷之石要从水里去）。
room((2, 1), '湖泊·柠檬岩上空', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'       cc               ',
'                c       ',
'      rrrr     rrr      ',
'      rrrr  f  rrr  !   ',
'########################',
'########################',
'########################',
'########################',
'########################'], texts=['路牌：柠檬岩的上面。底下的岩缝里有东西在噼啪响……'], deco=[('env_boulder', 3, 9), ('biome_reeds', 22, 9)])
# 湖泊·西崖顶：两屏宽。水塘往下是西瀑布；东接柠檬岩上空。
room((0, 1), '湖泊·西崖顶', 'lake', [
'##                                              ',
'##                                              ',
'##                                              ',
'##                                              ',
'##                                              ',
'##                      c c                     ',
'##                    ------                    ',
'##                                              ',
'## c c              !           f               ',
'######~~~~~~~~~~~~##############################',
'######~~~~~~~~~~~~##############################',
'######~~~~~~~~~~~~##############################',
'##########~~####################################',
'##########~~####################################'], texts=['路牌：西崖顶。瀑布从这里的水塘流下去。'], size=(2, 1), deco=[('forest_tree_2', 3, 9), ('biome_reeds', 7, 9), ('biome_reeds', 16, 9), ('forest_tree_0', 40, 9)])
# 湖泊·西岸：东接柠檬岩，西接西瀑布。
room((1, 2), '湖泊·西岸', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                c c     ',
'               -----    ',
'      f     u        !  ',
'########################',
'########################',
'########################'], texts=['路牌：西岸。柠檬岩西边的小沙滩。'], notes=['berry'], deco=[('biome_reeds', 2, 11), ('env_canoe', 9, 11), ('env_lake_willow', 20, 11)])
# 湖泊·西瀑布：瀑布从西崖顶落进水塘，水塘往下通西水洞。
room((0, 2), '湖泊·西瀑布', 'lake', [
'##        ~~            ',
'##        ~~            ',
'##        ~~            ',
'##        ~~            ',
'##        ~~            ',
'##        ~~            ',
'##        ~~            ',
'##        ~~            ',
'## c      ~~            ',
'##        ~~            ',
'##  !     ~~        f   ',
'######~~~~~~~~~~~~######',
'######~~~~~~~~~~~~######',
'######~~~~~~~~~~~~######'], texts=['路牌：西瀑布。水伊布能顺着瀑布游上西崖顶。'], deco=[('biome_reeds', 19, 11), ('env_river_stones', 22, 11)])
# 湖泊·码头下：湖畔的水塘底下，西接湖底洞穴。
room((6, 3), '湖泊·码头下', 'lakecave', [
'rrr~~~~~~~~~~~~rrrrrrrrr',
'rrr~~~~~~~~~~~~rrrrrrrrr',
'rrr~~~~~~~c~~~~rrrrrrrrr',
'rrr~~~~~~~~~~~~rrrrrrrrr',
'rrr~~~~~p~~~~~~rrrrrrrrr',
'rrr~~~~~~~~~~~~rrrrrrrrr',
'~~~~~~~~~~~~~~~rrrrrrrrr',
'~~~~~~~~~~~~~~~rrrrrrrrr',
'~~~~~c~~~~~~c~~rrrrrrrrr',
'rrr~~~~~~~~~~~~rrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr'], deco=[('env_waterweed', 5, 10), ('env_waterweed', 13, 10)])
# 湖泊·湖心深处：湖心底下的大水室。东接湖底洞穴，西接蚌壳湾，底下通湖底深渊。
room((4, 3), '湖泊·湖心深处', 'lakecave', [
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~p~~~~~~~~~~~',
'~~~~~~~~~~~~~~~rrrr~~~~~',
'~~~~~~rrrr~~~~~rrrr~~~~~',
'~~~~~~rrrr~~~~~~~~~~~~~~',
'~~~c~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~c~~~~~p~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'rrrrrrrrrr~~~~rrrrrrrrrr',
'rrrrrrrrrr~~~~rrrrrrrrrr',
'rrrrrrrrrr~~~~rrrrrrrrrr',
'rrrrrrrrrr~~~~rrrrrrrrrr',
'rrrrrrrrrr~~~~rrrrrrrrrr'], deco=[('env_waterweed', 2, 9), ('biome_crystal_0', 17, 9)])
# 湖泊·蚌壳湾：湖蚌洞底下。东接湖心深处，西接沉木，底下通湖底深渊。
room((3, 3), '湖泊·蚌壳湾', 'lakecave', [
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~c~~~~~~~~~~~c~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~p~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~rr~~~~~rrrrrrr~~rrrrrr',
'rrrr~~~~~rrrrrrr~~~~~~rr',
'rrrr~~~~~rrrrrrr~c~c~crr',
'rrrr~~~~~rrrrrrr~~~~~~rr',
'rrrr~~~~~rrrrrrrrrrrrrrr',
'rrrr~~~~~rrrrrrrrrrrrrrr'], deco=[('exp_abyss_shell', 10, 8), ('exp_abyss_shell', 20, 12), ('env_waterweed', 2, 8)])
# 湖泊·沉木：柠檬岩底下，沉着几根被风暴吹断的木头。
room((2, 3), '湖泊·沉木', 'lakecave', [
'rrrrrrrrrrrrrrrrrrrr~~~~',
'rrrrrrrrrrrrrrrrrrrr~~~~',
'rrrrrrrrrrrrrrrrrrrr~~~~',
'rr~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~c~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~p~~~~~~~',
'~~~~~~rrrrrrr~~~~~~~~~~~',
'~~~~~~~~~c~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~rrrrrr~~~~',
'rr~~c~~~~~~~~~~~~~~~~~~~',
'rrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr'], deco=[('env_canoe', 10, 6), ('env_waterweed', 20, 10)])
# 湖泊·西水洞：西瀑布的水塘底下，两屏宽。东接沉木。
room((0, 3), '湖泊·西水洞', 'lakecave', [
'rrrrrr~~~~~~~~~~~~rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrr~~~~~~~~~~~~rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrr~~~~~~~~~~~~rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrr~~~~~~~~~~rr~~~~~~~~~~~~~~~~~~rr~~~~~~~~~rrr',
'rrrr~~~~~~~~~~rr~~~~~~~~~~~~~~~~~~rr~~~~c~~~~~~~',
'rrrr~~~~~~~~~~rr~~~~p~~~~~~~~~~~~~rr~~~~~~~~~~~~',
'rrrr~~~~~~~~~~rr~~~~~~~~~~~~~~~~~~rr~~~~~~~~~~~~',
'rrrr~~~~~~~~~~~~~~~~~~~~rr~~~~~~~~~~~~~~~~~~~~~~',
'rrrr~~~~~~~~~~~~~~~~~~~~rr~~~~p~~~~~~~~~~~~~~~~~',
'rrrr~~~~c~c~~~~~~~~~~~~~rr~~~~~~~~~~~~~~~~~~~rrr',
'rrrr~~~~~~~~~~~~~~~~~~~~rr~~~~~~~~~~~~~~~~~~~rrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr~~~~~~rrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr~c~c~crrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'], size=(2, 1), deco=[('env_waterweed', 6, 11), ('biome_crystal_1', 30, 11), ('env_waterweed', 42, 11)])
# 湖泊·湖底深渊：三屏宽，湖底洞穴、湖心深处、蚌壳湾都能潜下来。中间往下的沟以后接深渊海沟（要深潜）。
room((3, 4), '湖泊·湖底深渊', 'lakecave', [
'rrrr~~~~~rrrrrrrrrrrrrrrrrrrrrrrrr~~~~rrrrrrrrrrrrrrrrrrr~~~rrrrrrrrrrrr',
'rrrr~~~~~rrrrrrrrrrrrrrrrrrrrrrrrr~~~~rrrrrrrrrrrrrrrrrrr~~~rrrrrrrrrrrr',
'rrrr~~~~~rrrrrrrrrrrrrrrrrrrrrrrrr~~~~rrrrrrrrrrrrrrrrrrr~~~rrrrrrrrrrrr',
'rr~~~~~~~~~~~~~~~~~~rrr~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~rr',
'rr~~~~~~~~~~~~~~~~~~rrr~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~p~~~~~~~rr',
'rr~~~~~~~~~~p~~~~~~~rrr~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~rr',
'rr~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~p~~~~~~~~~~~~~~~~~~~~~~~~~~~~~rr',
'rr~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~rrr~~~~~~~~~~~~~~~~~~~~~rr',
'rr~~~~~~c~~~~~~~~~~~~~~~~~c~~~~~~~~~~~~~~~~~~~rrr~~~c~~~~~~~~~~~~~~~~~rr',
'rr~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~rrr~~~~~~~~~~~~~~~~~~~~~rr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrr~~~~rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr~~~~~rrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrr~!~~rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr~~h~~rrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'], texts=['石碑：再往下是深渊海沟。水太深太黑，水伊布现在还潜不下去。'], size=(3, 1), deco=[('biome_crystal_0', 10, 10), ('exp_abyss_kelp', 24, 10), ('biome_crystal_1', 44, 10), ('exp_abyss_kelp', 60, 10)])

# ================= 输出 =================
def build():
    mx = min(0, min(r['pos'][0] for r in ROOMS)); my = min(0, min(r['pos'][1] for r in ROOMS))   # 往北、往西扩出去的格数
    gw = max(r['pos'][0] + r['size'][0] for r in ROOMS) - mx; gh = max(r['pos'][1] + r['size'][1] for r in ROOMS) - my
    TW, TH = gw * RW, gh * RH
    grid = [['#'] * TW for _ in range(TH)]          # 未定义的区域全是实心
    rooms_out, ents, texts_out, decos = [], [], [], []
    occupied = set()
    for i, r in enumerate(ROOMS):
        rx, ry = r['pos'][0] - mx, r['pos'][1] - my; sw, sh = r['size']
        for dx in range(sw):
            for dy in range(sh):
                assert (rx + dx, ry + dy) not in occupied, ('房间重叠', r['name']); occupied.add((rx + dx, ry + dy))
        x0, y0 = rx * RW, ry * RH; ti = ni = 0
        for yy, row in enumerate(r['rows']):
            for xx, ch in enumerate(row):
                X, Y = x0 + xx, y0 + yy
                if ch in 'Pevpf GMY123miych*s!NTokCgVu'.replace(' ', ''):
                    e = dict(t=ch, x=X, y=Y, room=i)
                    if ch in '!N': e['text'] = r['texts'][ti] if ti < len(r['texts']) else '……'; ti += 1
                    if ch in 'TokCVu': assert ni < len(r['notes']), ('notes 不够', r['name']); e['text'] = r['notes'][ni]; ni += 1
                    ents.append(e)
                    nb = [row[xx - 1] if xx > 0 else ' ', row[xx + 1] if xx + 1 < len(row) else ' ']
                    grid[Y][X] = '~' if '~' in nb else ' '      # 水里的实体所在格仍是水
                else: grid[Y][X] = ch
        rooms_out.append(dict(id=i, name=r['name'], region=r['region'], x=x0, y=y0, w=sw * RW, h=sh * RH))
        for d in r['deco']:
            assert os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites', 'deco', d[0] + '.png')), ('装饰素材不存在', d[0])
            decos.append(dict(k=d[0], x=(x0 + d[1]) * T + T // 2 + (d[3] if len(d) > 3 else 0), y=(y0 + d[2]) * T + (d[4] if len(d) > 4 else 0)))
    # 自动草地：泥土上方是空气 → '='
    for y in range(TH):
        for x in range(TW):
            if grid[y][x] == '#' and y > 0 and grid[y - 1][x] in ' -' : grid[y][x] = '='
        assert ti == len(r['texts']), ('texts 数量和路牌 / 村民不一致', r['name'], ti, len(r['texts']))
        assert ni == len(r['notes']), ('notes 数量和石板 / 果子不一致', r['name'], ni, len(r['notes']))
    # 后加的实体种类各自成组排在最后（先彩蛋，再伙伴地点），已有实体的编号不变
    ents = [e for e in ents if e['t'] not in 'TokCgVu'] + [e for e in ents if e['t'] in 'To'] + [e for e in ents if e['t'] == 'k'] + [e for e in ents if e['t'] in 'CgVu']
    start = next(e for e in ents if e['t'] == 'P')
    world = dict(tw=TW, th=TH, ox=-mx * RW, oy=-my * RH, rows=[''.join(r) for r in grid], rooms=rooms_out, entities=[e for e in ents if e['t'] != 'P'], start=dict(x=start['x'], y=start['y']), deco=decos)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    os.makedirs(os.path.join(root, 'levels'), exist_ok=True)
    json.dump(world, open(os.path.join(root, 'levels', 'world.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    html_path = os.path.join(root, 'index.html')
    if os.path.exists(html_path):
        html = open(html_path, encoding='utf-8').read()
        b, e = '/* WORLD_BEGIN */', '/* WORLD_END */'
        if b in html and e in html:
            i, j = html.index(b) + len(b), html.index(e)
            html = html[:i] + '\nconst WORLD = ' + json.dumps(world, ensure_ascii=False, separators=(',', ':')) + ';\n' + html[j:]
            open(html_path, 'w', encoding='utf-8').write(html); print('world embedded into index.html')
    print(f'world {TW}x{TH} tiles, {len(rooms_out)} rooms, {len(ents)} entities, {len(decos)} deco')

if __name__ == '__main__':
    build()
