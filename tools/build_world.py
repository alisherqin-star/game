# 世界构建：把每个房间的字符画拼成一张大地图，写出 levels/world.json 并嵌入 index.html。
# 用法：python3 tools/build_world.py
#
# 房间网格：每间 24x14 格，用 size=(宽, 高) 可以横向、纵向占多格，大房间里镜头连续滚动、不换页。字符含义：
#   地形  ' ' 空  '#' 泥土/地面  'r' 岩石  'b' 砖  'B' 塔石  'W' 木箱  '~' 水  'E' 电网  'S' 黑影墙
#         '^' 尖刺  '-' 单向平台  '_' 深渊（掉下去扣血回安全点）  'D' 锁门（集齐 8 种进化）  'K' 裂墙（雷伊布冲撞）  'L' 熔岩
#   实体  'P' 出生点  'e' 史莱姆  'v' 蝙蝠  'p' 刺河豚  'f' 跳跳蛙  'G' 大史莱姆 Boss  'M' 湖蚌 Boss
#         '1' 水之石  '2' 雷之石  '3' 火之石  'm' 苔藓岩  'i' 冰岩（巨石要藏起来，用伊布的样子靠近才会进化）
#         'y' 迷路的小史莱姆（支线，计划放在夜之墓地的黑影墙后面）
#         'c' 金币  'h' 心之碎片  '*' 闪光石  's' 存档石  '!' 路牌  'N' 村民伊布
#         彩蛋：'T' 古代石板（刻着进化线索的谜语）  'o' 旧时代的果子（吃了回血但不会进化）
#         伙伴：'k' 绒绒出现的地点，notes 写 '步骤|角色'，例如 '1|slimes'（起点村的绒绒是 texts 里以「见习向导绒绒：」开头的村民）
#         RPG：'C' 宝箱（notes 写饰品 id，例如 'bell'）  'g' 商人被吹散的货物包
#              'V' 走散的村民（notes 写 '谁|lost' 是在外面等人找，'谁|home' 是找到后回村站的位置）
#         '!' 和 'N' 的文字按出现顺序取 texts=[...]；'T'、'o'、'k'、'C'、'V' 的文字按出现顺序取 notes=[...]，
#         果子的写法是 '图片名|吃下时的话'，例如 'food_1_blueberry|……'。
#         彩蛋实体统一排在实体表最后，加新彩蛋不会改变已有实体的编号（旧存档仍然有效）。
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
    for d in deco: assert 0 <= d[1] < w and 0 < d[2] <= h, (name, d)
    ROOMS.append(dict(pos=pos, name=name, region=region, rows=rows, texts=list(texts), size=size, deco=list(deco), notes=list(notes)))

# ================= 起点村 =================
room((7, 2), '起点村', 'village', [
'                                                ',
'                                                ',
'                                                ',
'                       T                        ',
'                     ####                       ',
'                                    c c c       ',
'            ####                  -------       ',
'                                                ',
'                                                ',
'                                                ',
'   T N   V  s    P  V    N      !    V    N     ',
'################################################',
'################################################',
'################################################'], texts=[
'村长老橡：欢迎回家！东边的草原最近有大史莱姆出没，西边的湖没有水伊布的本事可过不去。',
'见习向导绒绒：我叫绒绒！听说伊布碰到进化石、靠近神奇的巨石就会进化。按 1～9 切换学会的形态，按 X 用技能……我、我想去糖果花园的星光野餐，可是风暴把路吹断了，我一个人不敢去。你会等我一起去吗？',
'路牌：← 湖泊（需要游泳）　　草原 →',
'商人栗栗：风暴把我的货吹得满地都是……收集金币和徽章吧，等路修好了，我这里会有好东西卖。',
], notes=['古代石板（其五）：「冷风从湖北的冰缝里吹出。霜雪覆盖的巨石，在那里等待伊布。」', '古代石板（其一）：「蔚蓝之石，映着池水的光。触碰它的伊布，会生出鱼鳍与长尾。」', 'grandma|home', 'scholar|home', 'trainer|home'], size=(2, 1), deco=[('forest_tree_0', 2, 11), ('env_village_cottage', 8, 11), ('env_planter', 14, 11), ('forest_tree_1', 19, 11), ('env_fence', 22, 11), ('env_village_cottage', 28, 11), ('env_bench', 35, 11), ('env_berry_bush', 38, 11), ('env_stump', 40, 11), ('forest_tree_2', 46, 11)])

# ================= 草原 =================
room((9, 2), '草原·入口', 'plains', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'            c c         ',
'          -----         ',
'                        ',
'                  co    ',
'                 ###    ',
' k !      e           e ',
'########################',
'########################',
'########################'], texts=['路牌：踩在怪物头上可以打倒它。被碰到会掉血，血没了就回到存档石。'], notes=['food_1_blueberry|吃了一颗蓝莓，酸酸甜甜的。……伊布没有进化。看来进化可不是靠吃东西的。', '1|slimes'], deco=[('forest_tree_0', 6, 11), ('forest_tree_1', 19, 11), ('env_berry_bush', 23, 11, -4)])
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
'   WW  ---           V  ',
'#######          #######',
'#######          #######'], texts=[], notes=['古代石板（其六）：「与伙伴在烈日下并肩作战。羁绊满溢时，额前会浮现红玉。」', 'trainer|lost'], deco=[('forest_tree_0', 20, 12)])
room((11, 2), '草原·蝙蝠林', 'plains', [
'                        ',
'                        ',
'                        ',
'                        ',
'        v          v    ',
'                        ',
'              C       T ',
'     ---     ---     ---',
'                        ',
'                        ',
'   c  V   e      e    c ',
'########################',
'########################',
'########################'], notes=['leaf', '古代石板（其七）：「与伙伴在月光下并肩作战。羁绊满溢时，周身会浮现金环。」', 'grandma|lost'], deco=[('forest_tree_0', 2, 11), ('forest_tree_1', 8, 11), ('forest_tree_2', 14, 11), ('forest_tree_0', 20, 11, 4)])
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
' s   !    ####       !  ',
'######~~~~####~~~~######',
'######~T~~####~~~~######',
'########################'], notes=['古代石板（其二）：「黄绿之石，困着一声惊雷。它嵌在湖水尽头的岩缝里。」'], texts=['路牌：池塘中央的小岛上闪着蓝光，是水之石！伊布碰到它就会进化成会游泳的水伊布，回头去西边的湖看看吧！', '路牌：→ 雷电塔。塔门的电网只有雷伊布能穿过。'], deco=[('env_berry_bush', 3, 11), ('forest_tree_2', 20, 11)])
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
'BBBBBBBBB      BBBBBBBBB'], texts=['石碑：这里是雷电塔的门厅。从地板的缺口跳下去就是草原的池塘，往东回到中庭继续向上。'], notes=['bell', '古代石板（其三）：「赤红之石，供奉在高塔之巅。电网之后，火焰之前。」', '古代石板（其四）：「荆棘烧尽之处，青苔覆着巨石。伊布在它身旁醒来，耳尖冒出了嫩叶。」'])


# ================= 湖泊 =================
room((6, 2), '湖畔', 'lake', [
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
'   f           s   !    ',
'###~~~~~~~~~~###########',
'###~~~~~~~~~~###########',
'###~~c~c~c~c~###########'], texts=['路牌：湖水又深又宽，没有水伊布过不去。'])
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
'                        ',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~p~~~~~~~~~~~~~~~~p~~'])
room((5, 3), '湖底洞穴', 'lakecave', [
'rrrr~~~~~~~~~~~~~~~~rrrr',
'rrr~~~~~~~~~~~~~~~~~~rrr',
'rr~~~~~~~~~~~~~~~~~~~~rr',
'r~~~~p~~~~~~~~~~~~p~~~~r',
'r~~~~~~~~~rrrr~~~~~~~~~r',
'r~~~rrr~~~~~~~~~~rrr~~~r',
'r~~~~~~~~~~~~~~~~~~~~~~r',
'r~~c~~~~~~~~~~~~~~~~c~~r',
'rr~~~~~~~~~p~~~~~~~~~~rr',
'rrr~~~~~~~~~~~~~~~~~~rrr',
'rrrr~~~~~~~~~~~~~~~~rrrr',
'rrrrrr~~~~~~~~~~~~rrrrrr',
'rrrrrrrr~~~~*~~~rrrrrrrr',
'rrrrrrrrrrrrrrrrrrrrrrrr'])
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
'   f                    ',
'~~~~~~~~~~~~~~~~~~~~~~~~',
'~~~~p~~~~~~~~~~~~~p~~~~~',
'~~~~~~~~~~h~~~~~~~~~~~~~'])
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
'~~~~~~~~~~~~~~~~~~~~~~~~'])
room((2, 2), '柠檬岩', 'lake', [
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'                        ',
'      2                 ',
'    ######              ',
'  ! ######   s          ',
'####################~~~~',
'####################~~~~',
'####################~~~~'], texts=['路牌：岩缝里嵌着雷之石！伊布碰到它就会进化成雷伊布，冲过草原尽头的电网。'])

# ================= 雷电塔内部（新房间放在最后，已有房间和实体的编号不变，旧存档仍然有效） =================
# 中庭：三屏高的竖井，一路往上爬不换页。塔基西墙是电网门（只有雷伊布能穿过），东墙裂墙后藏着心之碎片。
room((14, 0), '雷电塔·中庭', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BB                    BB',
'BB                    BB',
'BB    c c c c c C     BB',
'BB    -----------     BB',
'BB                    BB',
'BB               v      ',
'BB   ----               ',
'BB                      ',
'BB                      ',
'BB        -----  BBBBBBB',
'BB                    BB',
'BB    ----            BB',
'BB                    BB',
'BB                    BB',
'BB      ----          BB',
'BB      EEEE          BB',
'BB                    BB',
'BB          ---       BB',
'BB                    BB',
'BB               v    BB',
'BB  ------            BB',
'           c          BB',
'                      BB',
'         -----        BB',
'BBBBBB                BB',
'BB         -----      BB',
'BB                    BB',
'BB                    BB',
'BB  -----             BB',
'BB              v     BB',
'BB                    BB',
'BB          -----     BB',
'BB                    BB',
'BB     c  c  c        BB',
'EE    ---------    ---BB',
'EE                    K ',
'EE  s   !           g Kh',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB'], texts=['石碑：雷电塔。风暴那晚之后，塔里的电网就一直失控，只有雷伊布能穿过。一直往上爬，塔顶供奉着一颗火之石。'], size=(1, 3), deco=[
    ('env_coil', 18, 39), ('env_torch_0', 2, 33), ('env_torch_0', 21, 30), ('env_lever', 4, 26),
    ('env_gear', 20, 24), ('env_torch_0', 2, 19), ('env_torch_0', 21, 15), ('env_torch_0', 2, 7)], notes=['magnet'])

# 塔顶：两屏宽的大厅，镜头连续横移。电网帘子挡住不是雷伊布的形态，尽头的祭坛上是火之石。
room((15, 0), '雷电塔·塔顶', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BB                                            BB',
'BB                                            BB',
'BB                          c c c             BB',
'BB                         -------            BB',
'BB              v                     v       BB',
'                    E                         BB',
'                    E                         BB',
'                    E                     3   BB',
'    s       !   V   E        f   o   BBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBB^^^BBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'], texts=['石碑：火之石就供奉在大厅尽头。让伊布碰到它，伊布就会进化成浑身火焰的火伊布。'], notes=['scholar|lost', 'food_3_chili|咬了一口辣椒！伊布辣得直吐舌头……但还是没有进化。火之石就在大厅尽头。'], size=(2, 1), deco=[
    ('env_torch_0', 6, 9), ('biome_pillar', 9, 11), ('env_coil', 17, 11), ('env_gear', 24, 4),
    ('env_torch_0', 26, 9), ('biome_pillar', 33, 11), ('env_torch_0', 41, 8), ('env_lever', 44, 10)])

# ================= 输出 =================
def build():
    gw = max(r['pos'][0] + r['size'][0] for r in ROOMS); gh = max(r['pos'][1] + r['size'][1] for r in ROOMS)
    TW, TH = gw * RW, gh * RH
    grid = [['#'] * TW for _ in range(TH)]          # 未定义的区域全是实心
    rooms_out, ents, texts_out, decos = [], [], [], []
    occupied = set()
    for i, r in enumerate(ROOMS):
        rx, ry = r['pos']; sw, sh = r['size']
        for dx in range(sw):
            for dy in range(sh):
                assert (rx + dx, ry + dy) not in occupied, ('房间重叠', r['name']); occupied.add((rx + dx, ry + dy))
        x0, y0 = rx * RW, ry * RH; ti = ni = 0
        for yy, row in enumerate(r['rows']):
            for xx, ch in enumerate(row):
                X, Y = x0 + xx, y0 + yy
                if ch in 'Pevpf GM123miych*s!NTokCgV'.replace(' ', ''):
                    e = dict(t=ch, x=X, y=Y, room=i)
                    if ch in '!N': e['text'] = r['texts'][ti] if ti < len(r['texts']) else '……'; ti += 1
                    if ch in 'TokCV': assert ni < len(r['notes']), ('notes 不够', r['name']); e['text'] = r['notes'][ni]; ni += 1
                    ents.append(e)
                    nb = [row[xx - 1] if xx > 0 else ' ', row[xx + 1] if xx + 1 < len(row) else ' ']
                    grid[Y][X] = '~' if '~' in nb else ' '      # 水里的实体所在格仍是水
                else: grid[Y][X] = ch
        rooms_out.append(dict(id=i, name=r['name'], region=r['region'], x=x0, y=y0, w=sw * RW, h=sh * RH))
        for d in r['deco']:
            assert os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites', 'deco', d[0] + '.png')), ('装饰素材不存在', d[0])
            decos.append(dict(k=d[0], x=(x0 + d[1]) * T + T // 2 + (d[3] if len(d) > 3 else 0), y=(y0 + d[2]) * T))
    # 自动草地：泥土上方是空气 → '='
    for y in range(TH):
        for x in range(TW):
            if grid[y][x] == '#' and y > 0 and grid[y - 1][x] in ' -' : grid[y][x] = '='
        assert ti == len(r['texts']), ('texts 数量和路牌 / 村民不一致', r['name'], ti, len(r['texts']))
        assert ni == len(r['notes']), ('notes 数量和石板 / 果子不一致', r['name'], ni, len(r['notes']))
    # 后加的实体种类各自成组排在最后（先彩蛋，再伙伴地点），已有实体的编号不变
    ents = [e for e in ents if e['t'] not in 'TokCgV'] + [e for e in ents if e['t'] in 'To'] + [e for e in ents if e['t'] == 'k'] + [e for e in ents if e['t'] in 'CgV']
    start = next(e for e in ents if e['t'] == 'P')
    world = dict(tw=TW, th=TH, rows=[''.join(r) for r in grid], rooms=rooms_out, entities=[e for e in ents if e['t'] != 'P'], start=dict(x=start['x'], y=start['y']), deco=decos)
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
