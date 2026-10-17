# 世界构建：把每个房间的字符画拼成一张大地图，写出 levels/world.json 并嵌入 index.html。
# 用法：python3 tools/build_world.py
#
# 房间网格：每间 24x14 格（可以横向占多格）。字符含义：
#   地形  ' ' 空  '#' 泥土/地面  'r' 岩石  'b' 砖  'B' 塔石  'W' 木箱  '~' 水  'E' 电网  'S' 黑影墙
#         '^' 尖刺  '-' 单向平台  '_' 深渊（掉下去扣血回安全点）  'D' 锁门（集齐 8 种进化）  'K' 裂墙（雷伊布冲撞）  'L' 熔岩
#   实体  'P' 出生点  'e' 史莱姆  'v' 蝙蝠  'p' 刺河豚  'f' 跳跳蛙  'G' 大史莱姆 Boss  'M' 湖蚌 Boss
#         '1' 水之石  '2' 雷之石  '3' 火之石  'm' 苔藓岩  'i' 冰岩（巨石要藏起来，用伊布的样子靠近才会进化）
#         'y' 迷路的小史莱姆（支线，计划放在夜之墓地的黑影墙后面）
#         'c' 金币  'h' 心之碎片  '*' 闪光石  's' 存档石  '!' 路牌  'N' 村民伊布
#
# 装饰：room(..., deco=[(素材名, 列, 地面行[, 像素偏移]), ...])，素材名是 sprites/deco/ 下的文件名（不含 .png）。
#   图片底边中点对齐到「列」那一格的中间、「地面行」那一行的顶边，也就是站在这一行的地面上。
#   装饰只是画面，没有碰撞；画在地形后面。地面上的小草由游戏按坐标自动撒，不用写在这里。
import json, os, sys

RW, RH = 24, 14
T = 16
ROOMS = []
def room(pos, name, region, rows, texts=(), size=(1, 1), deco=()):
    w = RW * size[0]
    assert len(rows) == RH, (name, len(rows))
    for i, r in enumerate(rows): assert len(r) == w, (name, i, len(r), r)
    for d in deco: assert 0 <= d[1] < w and 0 < d[2] <= RH, (name, d)
    ROOMS.append(dict(pos=pos, name=name, region=region, rows=rows, texts=list(texts), size=size, deco=list(deco)))

# ================= 起点村 =================
room((7, 2), '起点村', 'village', [
'                                                ',
'                                                ',
'                                                ',
'                                                ',
'                     ####                       ',
'                                    c c c       ',
'            ####                  -------       ',
'                                                ',
'                                                ',
'                                                ',
'     N      s    P       N      !         N     ',
'################################################',
'################################################',
'################################################'], texts=[
'村长伊布：欢迎回家！东边的草原最近有大史莱姆出没，西边的湖没有水伊布的本事可过不去。',
'存档石：碰一下就能回满血并记录位置。',
'小伊布：听说伊布碰到水之石、雷之石、火之石就会进化，森林和冰窟里还藏着会让伊布进化的神奇巨石！按 1～9 可以切换已经学会的形态，按 X 使用当前形态的技能。',
'路牌：← 湖泊（需要游泳）　　草原 →',
'商人伊布：收集金币和徽章，以后我这里会有好东西卖。',
], size=(2, 1), deco=[('forest_tree_0', 2, 11), ('env_village_cottage', 8, 11), ('env_planter', 14, 11), ('forest_tree_1', 19, 11), ('env_fence', 22, 11), ('env_village_cottage', 28, 11), ('env_bench', 35, 11), ('env_berry_bush', 38, 11), ('env_stump', 40, 11), ('forest_tree_2', 46, 11)])

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
'                  c     ',
'                 ###    ',
'   !      e           e ',
'########################',
'########################',
'########################'], texts=['路牌：踩在怪物头上可以打倒它。被碰到会掉血，血没了就回到存档石。'], deco=[('forest_tree_0', 6, 11), ('forest_tree_1', 19, 11), ('env_berry_bush', 23, 11, -4)])
room((10, 2), '草原·坑洼', 'plains', [
'                        ',
'                        ',
'                        ',
'            --          ',
'                        ',
'       --        --     ',
'                        ',
'                        ',
'                        ',
'                     W  ',
'   e        v    c   W c',
'#####^^^#####^^^########',
'########################',
'########################'], deco=[('forest_tree_2', 2, 11), ('env_stump', 10, 11), ('env_berry_bush', 18, 11)])
room((10, 1), '草原·高崖', 'plains', [
'                        ',
'                        ',
'       h                ',
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
'#######          #######'], texts=[], deco=[('forest_tree_0', 20, 12)])
room((11, 2), '草原·蝙蝠林', 'plains', [
'                        ',
'                        ',
'                        ',
'                        ',
'        v          v    ',
'                        ',
'                        ',
'     ---     ---     ---',
'                        ',
'                        ',
'   c      e      e    c ',
'########################',
'########################',
'########################'], deco=[('forest_tree_0', 2, 11), ('forest_tree_1', 8, 11), ('forest_tree_2', 14, 11), ('forest_tree_0', 20, 11, 4)])
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
'  !        G            ',
'########################',
'########################',
'########################'], texts=['路牌：前方是大史莱姆的地盘！它每被踩一次就会分裂出一只小史莱姆。最近它特别暴躁，好像在找什么东西……'], deco=[('env_stump', 6, 11), ('env_berry_bush', 17, 11), ('forest_tree_1', 21, 11)])
room((13, 2), '草原·池塘', 'plains', [
'                        ',
'          EEEE          ',
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
'######~~~~####~~~~######',
'########################'], texts=['路牌：池塘中央的小岛上闪着蓝光，是水之石！伊布碰到它就会进化成会游泳的水伊布，回头去西边的湖看看吧！', '路牌：↑ 雷电塔。电网只有雷伊布能过。'], deco=[('env_berry_bush', 3, 11), ('forest_tree_2', 20, 11)])
room((13, 1), '雷电塔·门口', 'tower', [
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BBBBBBBBBBBBBBBBBBBBBBBB',
'BB                    BB',
'BB    c          c    BB',
'BB   ---        ---   BB',
'BB                    BB',
'BB        ---         BB',
'BB                    BB',
'BB  ---          ---  BB',
'BB         !          BB',
'BB                    BB',
'BB                    BB',
'BBBBBBBBB      BBBBBBBBB',
'BBBBBBBBB      BBBBBBBBB'], texts=['石碑：雷电塔暂未开放，施工中。'])

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
        x0, y0 = rx * RW, ry * RH; ti = 0
        for yy, row in enumerate(r['rows']):
            for xx, ch in enumerate(row):
                X, Y = x0 + xx, y0 + yy
                if ch in 'Pevpf GM123miych*s!N'.replace(' ', ''):
                    e = dict(t=ch, x=X, y=Y, room=i)
                    if ch in '!N': e['text'] = r['texts'][ti] if ti < len(r['texts']) else '……'; ti += 1
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
