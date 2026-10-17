# 游戏素材（除角色外）的像素画源文件。
# 用法：python3 tools/make_assets.py  → 写出 sprites/<类别>/<名字>.png 和 sprites/ASSET_SHEET.png
# 每张图是字符画：一个字母一个像素，'.' 透明，字母颜色见各自调色板。
import os, sys
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sprites')
ASSETS = {}   # 'category/name' -> (rows, palette)
def A(name, pal, rows):
    w = len(rows[0]); assert all(len(r) == w for r in rows), (name, [len(r) for r in rows])
    ASSETS[name] = (rows, pal)

# ---------------- 地形瓦片 16x16 ----------------
T_GRASS = dict(G='#9ced72', g='#62c94e', d='#3f9d38', k='#2d7a2a', B='#a86f3e', b='#8e5a2e', p='#c48c5c', q='#6f4521')
A('tiles/grass_top', T_GRASS, [
'GgGGGgGGGGgGGGGg',
'gGggGgggGgggGggG',
'ggdgggdggggdgggg',
'dgdddgdgddgddgdd',
'kdkkdkkdkkkdkkdk',
'BBBBBBBBBBBBBBBB',
'BBpBBBBBBbBBBBBB',
'BBBBBbbBBBBBBpBB',
'BbBBBBBBBqBBBBBB',
'BBBBBBBBpBBbbBBB',
'BBBBpBBBBBBBBBBB',
'BBBbbBBBBBBBBqBB',
'BBBBBBBBBBpBBBBB',
'BqBBBBBbBBBBBBBB',
'BpBBBBBBBBBBBbBB',
'BBBBBBBBqBBBBBBB'])
A('tiles/dirt', T_GRASS, [
'BBBBBBBBBBBBBBBB',
'BBbBBBBBpBBBBBBB',
'BBBBBBqBBBBBbbBB',
'BpBBBBBBBBBBBBBB',
'BBBBBbBBBBqBBBBB',
'BBBBBBBBBBBBBBpB',
'BBqBBBBBpBBBBBBB',
'BBBBBBBBBBBBbBBB',
'BBBBpBBBBBBBBBBB',
'BBBBBBBbbBBBBqBB',
'BbBBBBBBBBBBBBBB',
'BBBBBBBBBBpBBBBB',
'BBBqBBBBBBBBBBBB',
'BBBBBBpBBBBbBBBB',
'BBBBBBBBBBBBBBBB',
'BpBBBBBBBqBBBBpB'])
T_BRICK = dict(m='#6e3418', B='#d8744a', H='#f2a373', S='#b2543a')
A('tiles/brick', T_BRICK, [
'mmmmmmmmmmmmmmmm',
'mHHHHHHmmHHHHHHm',
'mHBBBBSmmHBBBBSm',
'mHBBBBSmmHBBBBSm',
'mHBBBBSmmHBBBBSm',
'mSSSSSSmmSSSSSSm',
'mmmmmmmmmmmmmmmm',
'mHHmmHHHHHHmmHHm',
'mHSmmHBBBBSmmHSm',
'mHSmmHBBBBSmmHSm',
'mHSmmHBBBBSmmHSm',
'mSSmmSSSSSSmmSSm',
'mmmmmmmmmmmmmmmm',
'mHHHHHHmmHHHHHHm',
'mHBBBBSmmHBBBBSm',
'mSSSSSSmmSSSSSSm'])
T_CRATE = dict(o='#5a3a18', H='#e6b878', W='#c48f4a', S='#8c5e2a', d='#7a4f1e', n='#3a2a18')
A('tiles/crate', T_CRATE, [
'oooooooooooooooo',
'oHHHHHHHHHHHHHSo',
'oHWWWWWWWWWWWWSo',
'oHWnWWWWWWWWnWSo',
'oHWWdWWWWWWdWWSo',
'oHWWWdWWWWdWWWSo',
'oHWWWWdWWdWWWWSo',
'oHWWWWWddWWWWWSo',
'oHWWWWWddWWWWWSo',
'oHWWWWdWWdWWWWSo',
'oHWWWdWWWWdWWWSo',
'oHWWdWWWWWWdWWSo',
'oHWnWWWWWWWWnWSo',
'oHWWWWWWWWWWWWSo',
'oSSSSSSSSSSSSSSo',
'oooooooooooooooo'])
T_WATER = dict(F='#ffffff', L='#a6e4ff', W='#3d8de0', w='#2f6fc4', k='#265ca8', I='#eefaff', i='#c4ecff', c='#8fd0f0')
A('tiles/water_surface_0', T_WATER, [
'LLFFLLLLLLLFFLLL',
'WLLLLWWWWWLLLLWW',
'WWWWWWWWWWWWWWWW',
'WWWWWWWWWWWWWWWW',
'WWwWWWWWWWWwWWWW',
'WWWWWWwwWWWWWWWW',
'WWWWWWWWWWWWWWWW',
'WwWWWWWWWWWWwwWW',
'WWWWWWWWWWWWWWWW',
'WWWWwwWWWWWWWWWW',
'WWWWWWWWWWwWWWWW',
'WWWWWWWWWWWWWWWW',
'WwwWWWWWWWWWWWwW',
'WWWWWWWWwwWWWWWW',
'WWWWWWWWWWWWWWWW',
'WWWWWWWWWWWWWWWW'])
A('tiles/water_surface_1', T_WATER, [
'LLLLLFFLLLLLLLFF',
'WWLLLLLWWWWLLLLL',
'WWWWWWWWWWWWWWWW',
'WWWWWWWWWWWWWWWW',
'WWWWWwWWWWWWWwWW',
'WWwwWWWWWWwwWWWW',
'WWWWWWWWWWWWWWWW',
'WWWWWWWwWWWWWWWW',
'WWWWWWWWWWWWWWWW',
'WWWWWWwwWWWWWwWW',
'WWwWWWWWWWWWWWWW',
'WWWWWWWWWWWWWWWW',
'WWWWwwWWWWWWwwWW',
'WWWWWWWWWwWWWWWW',
'WWWWWWWWWWWWWWWW',
'WWWWWWWWWWWWWWWW'])
A('tiles/water_body', T_WATER, [
'wwwwwwwwwwwwwwww',
'wwWwwwwwwwwwwWww',
'wwwwwwwwWWwwwwww',
'wwwwwwwwwwwwwwww',
'wwwwwWwwwwwwwwww',
'wwwwwwwwwwwwkwww',
'wwwwwwwwwwwwwwww',
'wwwWWwwwwwwwwwww',
'wwwwwwwwwwWwwwww',
'wwwwwwwwwwwwwwww',
'wwkwwwwwwwwwwwww',
'wwwwwwwWwwwwwwww',
'wwwwwwwwwwwwwWWw',
'wwwwwwwwwwwwwwww',
'wwwwWwwwwwwwwwww',
'wwwwwwwwwkwwwwww'])
A('tiles/ice_surface', T_WATER, [
'IIIIIIIIIIIIIIII',
'IiIIIIiiIIIIIiII',
'iiFIIiiiIFIIiiii',
'iiiiiiiiiiiiiiii',
'cccciccccccicccc',
'WWWWWWWWWWWWWWWW',
'WWwWWWWWWWWwWWWW',
'WWWWWWwwWWWWWWWW',
'WWWWWWWWWWWWWWWW',
'WwWWWWWWWWWWwwWW',
'WWWWWWWWWWWWWWWW',
'WWWWwwWWWWWWWWWW',
'WWWWWWWWWWwWWWWW',
'WWWWWWWWWWWWWWWW',
'WwwWWWWWWWWWWWwW',
'WWWWWWWWwwWWWWWW'])
T_FENCE = dict(P='#7f8494', p='#c6cad6', q='#4c505c', n='#2e3038', Y='#ffe94a', y='#fff8b0', g='#ffd23c')
A('tiles/fence_0', T_FENCE, [
'.ppP.........ppP',
'.pPq.........pPq',
'.pPq.........pPq',
'.nPq...YY....nPq',
'.pPq..Yy.....pPq',
'.pPq.Yy...Y..pPq',
'.pPqYy...Yy..pPq',
'.nPq....Yy...nPq',
'.pPq...Yy....pPq',
'.pPq..Yy..YY.pPq',
'.pPq.Yy..Yy..pPq',
'.nPq....Yy...nPq',
'.pPq...Yy....pPq',
'.pPq..YY.....pPq',
'.pPq.........pPq',
'.qqq.........qqq'])
A('tiles/fence_1', T_FENCE, [
'.ppP.........ppP',
'.pPq.........pPq',
'.pPq.........pPq',
'.nPq.....Y...nPq',
'.pPq....Yy...pPq',
'.pPq.Y.Yy....pPq',
'.pPq.yYy.....pPq',
'.nPq..Yy.Y...nPq',
'.pPq...YyYy..pPq',
'.pPq....Yy...pPq',
'.pPq...Yy....pPq',
'.nPq..Yy..Y..nPq',
'.pPq.Yy..Yy..pPq',
'.pPq.....Y...pPq',
'.pPq.........pPq',
'.qqq.........qqq'])
T_SHADOW = dict(S='#241640', v='#3d2a6a', V='#6a4aa8', e='#d9a6ff', w='#f3e6ff')
A('tiles/shadow_0', T_SHADOW, [
'SSSSSSSSSSSSSSSS',
'SSvvSSSSSSSSvSSS',
'SvVVvSSSSSSvVvSS',
'SvVeVvSSSSSvVVvS',
'SSvVVvSSSSSSvvSS',
'SSSvvSSSSSSSSSSS',
'SSSSSSSSvvSSSSSS',
'SSSSSSSvVVvSSSSS',
'SSSSSSvVeeVvSSSS',
'SSSSSSvVwwVvSSSS',
'SSSSSSSvVVvSSSSS',
'SSvSSSSSvvSSSSSS',
'SvVvSSSSSSSSSvSS',
'SSvSSSSSSSSSvVvS',
'SSSSSSSSSSSSSvSS',
'SSSSSSSSSSSSSSSS'])
A('tiles/shadow_1', T_SHADOW, [
'SSSSSSSSSSSSSSSS',
'SSSvSSSSSSSSSSSS',
'SSvVvSSSSSSSvvSS',
'SSvVVvSSSSSvVVvS',
'SSSvVvSSSSSvVeVS',
'SSSSvSSSSSSSvvSS',
'SSSSSSSSvvSSSSSS',
'SSSSSSSvVVvSSSSS',
'SSSSSSvVwwVvSSSS',
'SSSSSSvVeeVvSSSS',
'SSSSSSSvVVvSSSSS',
'SSSSSSSSvvSSSSSS',
'SSvvSSSSSSSSSSSS',
'SvVVvSSSSSSSvSSS',
'SSvvSSSSSSSvVvSS',
'SSSSSSSSSSSSvSSS'])
T_SPIKE = dict(G='#e2e8f0', g='#9aa4b4', o='#3a3f4c', B='#a86f3e', b='#8e5a2e')
A('tiles/spikes', T_SPIKE, [
'................',
'...o.......o....',
'..oGo.....oGo...',
'..oGo.....oGo...',
'.oGGgo...oGGgo..',
'.oGGgo...oGGgo..',
'.oGggo...oGggo..',
'oGGgggo.oGGgggo.',
'oGGgggo.oGGgggo.',
'oGggggo.oGggggo.',
'oooooooooooooooo',
'BBBBBBBBBBBBBBBB',
'BBbBBBBBBBbBBBBB',
'BBBBBBbBBBBBBBBB',
'BBBBBBBBBBBBbBBB',
'BbBBBBBBBBBBBBBB'])
# 单向浮空平台（可从下方跳上去）
T_PLAT = dict(o='#4a3416', W='#b7824a', H='#e4b878', S='#8a5c2c', g='#62c94e', G='#9ced72')
A('tiles/platform', T_PLAT, [
'GgGGgGGGGgGGGGgG',
'oooooooooooooooo',
'oHHHHHHHHHHHHHHo',
'oWWWWoWWWWoWWWWo',
'oWWWWoWWWWoWWWWo',
'oSSSSoSSSSoSSSSo',
'oooooooooooooooo',
'................',
'................',
'................',
'................',
'................',
'................',
'................',
'................',
'................'])

# ---------------- 物品 14x14 ----------------
A('items/food_1_blueberry', dict(o='#1b2860', B='#4a66d8', H='#8fa8ff', d='#2e45b0', g='#4f9a3a', G='#7fd060'), [
'......g.......',
'.....gG.......',
'....oo.oo.....',
'...oBHoBHo....',
'..oBHBBBBBo...',
'..oBBBBBdBo...',
'..oBBdoBBBo...',
'.oo.oodoooo...',
'oBHo.oBHBo....',
'oBBBooBBBBo...',
'oBBdBoBBdBo...',
'.oBBBo.oBBo...',
'..ooo...oo....',
'..............'])
A('items/food_2_lemon', dict(o='#6a5410', Y='#f7e23b', H='#fff7a8', d='#d9b818', g='#4a9a2a', G='#7fd060', b='#8a6a10'), [
'..........gG..',
'.........gG...',
'........oo....',
'.....ooobo....',
'...ooYYYYoo...',
'..oYHYYYYYYo..',
'.oYHHYYYYYYdo.',
'.oYHYYYYYYYdo.',
'.oYYYYYYYYddo.',
'.oYYYYYYYdddo.',
'..oYYYYYdddo..',
'...ooYYdddoo..',
'.....ooooo....',
'..............'])
A('items/food_3_chili', dict(o='#5a1010', R='#e0322b', H='#ff8a70', d='#a81c18', g='#3f8a2a', G='#7fd060'), [
'....gG........',
'...gGg........',
'....og........',
'....oRo.......',
'....oRHo......',
'.....oRHo.....',
'.....oRRHo....',
'......oRRHo...',
'......odRRo...',
'.......odRRo..',
'.......odRdo..',
'........oddo..',
'.........oo...',
'..............'])
A('items/food_4_leaf', dict(o='#2f6a1a', g='#5db83a', H='#9cea6c', d='#3f8a2a', v='#2d5e18'), [
'............o.',
'..........ooHo',
'........ooHHHo',
'.......oHHgHgo',
'......oHgggvgo',
'.....ogggvggo.',
'....ogggvgggo.',
'...oggvgggdo..',
'..ogdvggddo...',
'..ogvgdddo....',
'.ovdddddo.....',
'.oodooo.......',
'oo............',
'..............'])
A('items/food_5_icecream', dict(o='#4a3a6a', I='#c6ecff', H='#ffffff', p='#ffb6d5', c='#e0a86a', d='#a8743e', k='#7a5020', s='#ff6b8a'), [
'.....ooo......',
'....oHHIo.....',
'...oHIIIIo....',
'...oIIpIIo....',
'..oIIpspIIo...',
'..oIIIpIIIo...',
'...oIIIIIo....',
'..occcccccco..',
'...ocdcdcdo...',
'...occcccco...',
'....ocdcdo....',
'....occcco....',
'.....ocdo.....',
'......oo......'])
A('items/food_6_suncake', dict(o='#7a3a00', Y='#ffd34a', H='#fff2a0', r='#f5a623', R='#e07a10'), [
'......r.......',
'..r...r...r...',
'...r.oooo.r...',
'....oYYYYo....',
'...oYHHYYYo...',
'.rroYHYYYYorr.',
'...oYYYYYYo...',
'...oYYYYRYo...',
'....oYYRRo....',
'...r.oooo.r...',
'..r...r...r...',
'......r.......',
'..............',
'..............'])
A('items/food_7_mooncake', dict(o='#5a3010', B='#cf9240', H='#ecc070', d='#9a6424', y='#f5d442', k='#7a4a18'), [
'....oooooo....',
'...oBHHHHBo...',
'..oBHdddddBo..',
'.oBHdBBBBBdBo.',
'.oBdBBydyBBdo.',
'.oBdBydyyBBdo.',
'.oBdByyydBBdo.',
'.oBdBBdBBBBdo.',
'.oBBdBBBBBdBo.',
'..oBBdddddBo..',
'...okBBBBko...',
'....oooooo....',
'..............',
'..............'])
A('items/food_8_candy', dict(o='#6a2a50', P='#ff7fb0', H='#ffc2dc', r='#ff5a5a', y='#ffe14a', g='#6ae07a', c='#5ad0ff', w='#ffffff'), [
'..............',
'..............',
'oo....oooo...o',
'oPo..oryygo.oo',
'oPPo.oryygoPPo',
'oPHPooryygoPHo',
'oPHHoryyggoHPo',
'oPPHoryyggoPPo',
'oPPo.oryygoPPo',
'oPo..orryyo.oo',
'oo....oooo...o',
'..............',
'..............',
'..............'])

# ---------------- 怪物 ----------------
# 紫色史莱姆（地面巡逻）16x14，两帧
P_SLIME = dict(o='#2a1040', B='#9a63e0', H='#c9a3ff', d='#6a3fa8', w='#ffffff', e='#1a1020', m='#5a2a8a', t='#ff8aa8')
A('enemies/slime_0', P_SLIME, [
'......oooo......',
'....ooHHHHoo....',
'...oHHBBBBHHo...',
'..oHBBBBBBBBHo..',
'..oBBwwBBwwBBo..',
'.oBBBweBBweBBBo.',
'.oBBBwwBBwwBBBo.',
'.oBBBBBBBBBBBBo.',
'.oBBBBmmmmBBBBo.',
'.oBBBBBttBBBBBo.',
'.oBdBBBBBBBBdBo.',
'..odddBBBBdddo..',
'...oddddddddo...',
'....oooooooo....'])
A('enemies/slime_1', P_SLIME, [
'................',
'.....oooooo.....',
'...ooHHHHHHoo...',
'..oHHBBBBBBHHo..',
'.oHBBwwBBwwBBHo.',
'.oBBBweBBweBBBo.',
'.oBBBwwBBwwBBBo.',
'oBBBBBBBBBBBBBBo',
'oBBBBBmmmmBBBBBo',
'oBBBBBBttBBBBBBo',
'oBdBBBBBBBBBBdBo',
'.oddddBBBBddddo.',
'..oddddddddddo..',
'...oooooooooo...'])
# 飞行的蝙蝠（提高难度用）16x12，两帧
P_BAT = dict(o='#1a1030', B='#4a3a7a', H='#7a66b8', d='#2e2250', e='#ff5a5a', w='#ffffff', t='#ffe0e0')
A('enemies/bat_0', P_BAT, [
'o..............o',
'oo............oo',
'oBo..........oBo',
'oBBo..oooo..oBBo',
'oBBBooBHHBooBBBo',
'oBBBBBBHHBBBBBBo',
'.oBBBBeBBeBBBBo.',
'..oBBBBttBBBBo..',
'...ooBBBBBBoo...',
'.....oBBBBo.....',
'......oddo......',
'.......oo.......'])
A('enemies/bat_1', P_BAT, [
'................',
'................',
'................',
'......oooo......',
'...oooBHHBooo...',
'..oBBBBHHBBBBo..',
'.oBBBBeBBeBBBBo.',
'oBBBBBBttBBBBBBo',
'oBBooBBBBBBooBBo',
'ooo..oBBBBo..ooo',
'......oddo......',
'.......oo.......'])

# ---------------- UI ----------------
P_COIN = dict(o='#7a5000', Y='#ffd23c', H='#fff4a0', d='#e0a000', k='#b87800')
A('ui/coin_0', P_COIN, ['..oooo..', '.oHHYdo.', 'oHYYYYdo', 'oHYYYYdo', 'oYYYYddo', 'oYYYdddo', '.oYdddo.', '..oooo..'])
A('ui/coin_1', P_COIN, ['...oo...', '..oHYo..', '.oHYYdo.', '.oHYYdo.', '.oYYddo.', '.oYdddo.', '..oddo..', '...oo...'])
A('ui/coin_2', P_COIN, ['...oo...', '...oo...', '..oHdo..', '..oHdo..', '..oYdo..', '..oYdo..', '...oo...', '...oo...'])
A('ui/coin_3', P_COIN, ['...oo...', '..oHYo..', '.oHYYdo.', '.oHYYdo.', '.oYYddo.', '.oYdddo.', '..oddo..', '...oo...'])
P_HEART = dict(o='#5a1020', R='#ff4a6a', H='#ff9ab0', d='#c02848', k='#3a2030', K='#4a2a3a')
A('ui/heart_full', P_HEART, ['.oo..oo.', 'oRHooRHo', 'oRRRRRRo', 'oRRRRRdo', '.oRRRdo.', '..oRdo..', '...oo...'])
A('ui/heart_empty', P_HEART, ['.oo..oo.', 'okKookKo', 'okkkkkko', 'okkkkkko', '.okkkko.', '..okko..', '...oo...'])
A('ui/sign', dict(o='#4a2a10', W='#dca860', H='#f0cc8a', S='#a8783a', d='#6b4420', k='#3a2410'), [
'oooooooooooooo',
'oHHHHHHHHHHHSo',
'oHWWWWkkWWWWSo',
'oHWWWWkkWWWWSo',
'oHWWWWkkWWWWSo',
'oHWWWWWWWWWWSo',
'oHWWWWkkWWWWSo',
'oSSSSSSSSSSSSo',
'oooooooooooooo',
'......odd.....',
'......odd.....',
'......odd.....',
'......odd.....',
'......odd.....'])
A('ui/flag', dict(o='#4a4a5a', P='#d8d8e4', p='#a8a8b8', R='#e8405e', r='#b82846', Y='#ffd84a', y='#f0a020', w='#ffffff'), [
'......oYYo......',
'.....oYwYYo.....',
'.....oYYYYo.....',
'......oyyo......',
'......oPp.......',
'......oPpoooooo.',
'......oPpRRRRRRo',
'......oPpRRwwRRo',
'......oPpRRwwRRo',
'......oPpRRRRrro',
'......oPpRRRrro.',
'......oPprrrro..',
'......oPpooo....',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'......oPp.......',
'.....ooooo......',
'....ooooooo.....'])

# ---------------- 背景装饰 ----------------
P_CLOUD = dict(W='#ffffff', S='#dcedff')
A('deco/cloud_big', P_CLOUD, [
'..........WWWW..................',
'.......WWWWWWWWW......WWWW......',
'.....WWWWWWWWWWWWW..WWWWWWWW....',
'...WWWWWWWWWWWWWWWWWWWWWWWWWWW..',
'.WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.',
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
'.WSSWWWWWWWWSSSWWWWWWWWSSWWWWWS.',
'..SSSSSSSSSSSSSSSSSSSSSSSSSSSS..',
'....SSSSSSSSSSSSSSSSSSSSSSSS....'])
A('deco/cloud_small', P_CLOUD, [
'......WWWW..........',
'...WWWWWWWWW..WWW...',
'.WWWWWWWWWWWWWWWWWW.',
'WWWWWWWWWWWWWWWWWWWW',
'WSSWWWWWWSSWWWWWWWSW',
'.SSSSSSSSSSSSSSSSSS.',
'...SSSSSSSSSSSSSS...'])
P_BUSH = dict(o='#2d6e2a', g='#4fb043', G='#7fd66a', H='#a8ec8a', d='#3a8a33', f='#ff8ab0', y='#ffe36a')
A('deco/bush', P_BUSH, [
'......ooo...ooo.....',
'....ooGGGoooGGGoo...',
'..ooGHGGGGGGGGGGGoo.',
'.oGHHGGGGfGGGGGGGGGo',
'oGHGGGGGGGGGGyGGGGdo',
'oGGGGGdGGGGGGGGGGddo',
'oGGdGGGGGGGdGGGGdddo',
'.oGGGGGGGdGGGGGdddo.',
'..oodddddddddddddoo.',
'....ooooooooooooo...'])
P_TREE = dict(o='#2a5a28', g='#4fb043', G='#7fd66a', H='#a8ec8a', d='#3a8a33', T='#8a5a30', t='#6b4320', k='#4a2e14')
A('deco/tree', P_TREE, [
'........oooooo..........',
'......ooGGGGGGoo........',
'....ooGHHGGGGGGGoo......',
'...oGHHGGGGGGGGGGGo.....',
'..oGHGGGGGGGGGGGGGGo....',
'..oGGGGGGdGGGGGGGGdo....',
'.oGGGGGGGGGGGGdGGGddo...',
'.oGGdGGGGGGGGGGGGGddo...',
'.oGGGGGGGGGGdGGGGdddo...',
'..oGGGGGdGGGGGGGdddo....',
'..oGdGGGGGGGGGGddddo....',
'...oGGGGGGGGGdddddo.....',
'....ooGGGGdddddddo......',
'......ooooooooooo.......',
'.........oTTto..........',
'.........oTTto..........',
'.........oTTto..........',
'.........oTTto..........',
'.........oTTto..........',
'........oTTTtko.........',
'.......oTTTttkko........',
'......oooooooooo........'])
P_HILL = dict(g='#8fd68c', d='#78c27a', k='#62ad68')
A('deco/flower', dict(o='#3a7a2a', g='#4fb043', p='#ff8ab0', w='#ffffff', y='#ffe36a'), [
'.p.p.',
'pwywp',
'.p.p.',
'..g..',
'.ggg.'])


# ---------------- 银河恶魔城新增 ----------------
T_ROCK = dict(R='#6e6a7a', r='#5a566a', d='#46425a', h='#8a86a0', k='#36324a')
A('tiles/rock', T_ROCK, [
'RRhRRRRRrRRRRRhR', 'RRRRRRRRRRRRRRRR', 'RrRRRRdRRRRrRRRR', 'RRRRRRRRRRRRRRRR', 'RRRRhRRRRRRRRdRR', 'RRRRRRRRRRkRRRRR', 'RdRRRRRRrRRRRRRR', 'RRRRRRRRRRRRRRhR',
'RRRRrRRRRRRRRRRR', 'RRRRRRRRdRRRRRRR', 'RhRRRRRRRRRRrRRR', 'RRRRRRkRRRRRRRRR', 'RRRRRRRRRRRRRdRR', 'RRdRRRRRRhRRRRRR', 'RRRRRRRRRRRRRRRR', 'RRRRrRRRRRRRkRRR'])
T_STONE = dict(m='#2e2a44', B='#5c5878', H='#7e7a9c', S='#44405e')
A('tiles/stone', T_STONE, [
'mmmmmmmmmmmmmmmm', 'mHHHHHHmmHHHHHHm', 'mHBBBBSmmHBBBBSm', 'mHBBBBSmmHBBBBSm', 'mHBBBBSmmHBBBBSm', 'mSSSSSSmmSSSSSSm', 'mmmmmmmmmmmmmmmm', 'mHHmmHHHHHHmmHHm',
'mHSmmHBBBBSmmHSm', 'mHSmmHBBBBSmmHSm', 'mHSmmHBBBBSmmHSm', 'mSSmmSSSSSSmmSSm', 'mmmmmmmmmmmmmmmm', 'mHHHHHHmmHHHHHHm', 'mHBBBBSmmHBBBBSm', 'mSSSSSSmmSSSSSSm'])
T_LAVA = dict(L='#ff7a2a', l='#e04a14', H='#ffd24a', k='#b02a08')
A('tiles/lava_0', T_LAVA, ['HHLLHHHHLLLHHHLL', 'LLLLLLLLLLLLLLLL', 'LLlLLLLLLLLlLLLL', 'LLLLLLllLLLLLLLL', 'lLLLLLLLLLLLllLL', 'LLLLLLLLLLLLLLLL', 'LLLllLLLLLLLLLLL', 'LLLLLLLLLLlLLLLL', 'llLLLLLLLLLLLLlL', 'LLLLLLLLllLLLLLL', 'LLLLLLLLLLLLLLLL', 'LLkLLLLLLLLLkLLL', 'LLLLLLLkkLLLLLLL', 'LLLLLLLLLLLLLLLL', 'LkLLLLLLLLLLkLLL', 'LLLLLLLLLLLLLLLL'])
A('tiles/lava_1', T_LAVA, ['LLHHLLLHHLLLHHLL', 'LLLLLLLLLLLLLLLL', 'LLLLLlLLLLLLLlLL', 'LLllLLLLLLllLLLL', 'LLLLLLLLLLLLLLLL', 'LLLLLLLlLLLLLLLL', 'LLLLLLLLLLLLLLLL', 'LLLLLLllLLLLLlLL', 'LLlLLLLLLLLLLLLL', 'LLLLLLLLLLLLLLLL', 'LLLLllLLLLLLllLL', 'LLLLLLLLLkLLLLLL', 'LLkLLLLLLLLLLLLL', 'LLLLLLLLLLLLkLLL', 'LLLLLLLLLLLLLLLL', 'LLLLLLkLLLLLLLLL'])
A('tiles/cracked', dict(R='#6e6a7a', r='#5a566a', d='#46425a', k='#221e30', h='#8a86a0'), [
'RRRRRRRRRRRRRRRR', 'RRRRRRRkRRRRRRRR', 'RRRRRRkRRRRRRRRR', 'RRRRRkRRRkkRRRRR', 'RRkkkRRRRRRkRRRR', 'RkRRRRRRRRRRkRRR', 'RRRRRRRRdRRRRkRR', 'RRRRkRRRRRRRkRRR',
'RRRkRRRRRRRkRRRR', 'RRkRRRkkRRkRRRRR', 'RRRRkkRRkkRRRRRR', 'RRRkRRRRRRkRRRRR', 'RRkRRRRRRRRkRRRR', 'RRRRRRRRRRRRkRRR', 'RRRRRRRRRRRRRkRR', 'RRRRRRRRRRRRRRRR'])
A('tiles/door', dict(o='#2a1a40', D='#5a3a8a', H='#8a6ac0', y='#ffd84a', k='#3a2460'), [
'oooooooooooooooo', 'oHHHHHHHHHHHHHHo', 'oHDDDDDDDDDDDDko', 'oHDDDDDDDDDDDDko', 'oHDDDDyyyyDDDDko', 'oHDDDyDDDDyDDDko', 'oHDDyDDDDDDyDDko', 'oHDDyDDyyDDyDDko',
'oHDDyDDyyDDyDDko', 'oHDDyDDDDDDyDDko', 'oHDDDyDDDDyDDDko', 'oHDDDDyyyyDDDDko', 'oHDDDDDDDDDDDDko', 'oHDDDDDDDDDDDDko', 'okkkkkkkkkkkkkko', 'oooooooooooooooo'])
A('ui/save_stone_0', dict(o='#2a2a40', S='#9a9ab8', s='#6e6e90', c='#7fe8ff', C='#ffffff', g='#4a4a66'), [
'......oooo......', '.....oSSSSo.....', '....oSSccSSo....', '....oScCCcSo....', '...oSScCCcSSo...', '...oSSScCSSSo...', '...oSSSccSSSo...', '...oSSSSSSSSo...',
'...oSSSSSSSSo...', '...osSSSSSSso...', '...osssSSssso...', '..oggssssssggo..', '.oggggggggggggo.', 'oggggggggggggggo', 'oooooooooooooooo', '................'])
A('ui/save_stone_1', dict(o='#2a2a40', S='#9a9ab8', s='#6e6e90', c='#7fe8ff', C='#ffffff', g='#4a4a66'), [
'......oooo......', '.....oSSSSo.....', '....oSSCCSSo....', '....oSCCCCSo....', '...oSSCCCCSSo...', '...oSSSCCSSSo...', '...oSSScCSSSo...', '...oSSSSSSSSo...',
'...oSSSSSSSSo...', '...osSSSSSSso...', '...osssSSssso...', '..oggssssssggo..', '.oggggggggggggo.', 'oggggggggggggggo', 'oooooooooooooooo', '................'])
A('items/heart_piece', dict(o='#5a1020', R='#ff4a6a', H='#ff9ab0', d='#c02848'), ['.oo.oo..', 'oRHoRHo.', 'oRRRRRo.', 'oRRRRdo.', '.oRRdo..', '..oRo...', '...o....', '........'])
A('items/shiny_stone', dict(o='#4a3a10', Y='#ffe96a', H='#ffffff', d='#d9a822', s='#fff4c0'), ['....o.....', '...oYo....', '..oYHYo...', '.oYHHHYo..', 'oYYHHHYYo.', '.oYYHYYo..', '..oYYYo...', '...oYo....', '....o.....', '..........'])
A('ui/bubble', dict(o='#2a2040', W='#ffffff', k='#5a4a7a'), ['.oooooo.', 'oWWWWWWo', 'oWkWkWko', 'oWWWWWWo', '.oooooo.', '...oo...', '...o....', '........'])
# 大史莱姆 Boss 24x20
P_BIG = dict(o='#2a1040', B='#8e5bd3', H='#c9a3ff', d='#5e36a0', w='#ffffff', e='#1a1020', m='#4a2480', t='#ff8aa8')
A('enemies/bigslime_0', P_BIG, [
'........oooooooo........', '......ooHHHHHHHHoo......', '....ooHHBBBBBBBBHHoo....', '...oHHBBBBBBBBBBBBHHo...', '..oHBBBBBBBBBBBBBBBBHo..', '..oBBBwwwBBBBBBwwwBBBo..', '.oBBBBweeBBBBBBweeBBBBo.', '.oBBBBwwwBBBBBBwwwBBBBo.',
'.oBBBBBBBBBBBBBBBBBBBBo.', '.oBBBBBBBmmmmmmBBBBBBBo.', '.oBBBBBBBmttttmBBBBBBBo.', '.oBBBBBBBBmmmmBBBBBBBBo.', '.oBBBBBBBBBBBBBBBBBBBBo.', '.oBdBBBBBBBBBBBBBBBBdBo.', '..odddBBBBBBBBBBBBdddo..', '..oddddddBBBBBBdddddddo.'[:24],
'...odddddddddddddddddo..', '....oddddddddddddddddo..'[:24], '.....oooooooooooooooo...', '........................'])
A('enemies/bigslime_1', P_BIG, [
'........................', '.........oooooo.........', '......oooHHHHHHooo......', '....ooHHHBBBBBBHHHoo....', '..ooHBBBBBBBBBBBBBBHoo..', '.oHBBBwwwBBBBBBwwwBBBHo.', 'oBBBBBweeBBBBBBweeBBBBBo', 'oBBBBBwwwBBBBBBwwwBBBBBo',
'oBBBBBBBBBBBBBBBBBBBBBBo', 'oBBBBBBBBmmmmmmBBBBBBBBo', 'oBBBBBBBBmttttmBBBBBBBBo', 'oBBBBBBBBBmmmmBBBBBBBBBo', 'oBdBBBBBBBBBBBBBBBBBBdBo', 'odddBBBBBBBBBBBBBBBBdddo', 'oddddddBBBBBBBBBBddddddo', '.oddddddddddddddddddddo.',
'..oddddddddddddddddddo..', '...oooooooooooooooooo...', '........................', '........................'])
# 刺河豚 14x12 / 鼓起 16x16
P_PUF = dict(o='#3a2a10', Y='#f0c24a', H='#fff0a0', d='#c08a20', w='#ffffff', e='#1a1020', s='#e8e8e8', f='#8ac8ff')
A('enemies/puffer_0', P_PUF, ['....oooooo....', '...oYYYYYYo...', '..oYHYYYYYYo..', '.oYHYYwwYYYYo.', 'oYYYYYweYYYYfo', 'oYYYYYwwYYYYfo', 'oYYYYYYYYYYYfo', '.oYYYYYYYYYYo.', '.oYdYYYYYYdYo.', '..oddYYYYddo..', '...oddddddo...', '....oooooo....'])
A('enemies/puffer_1', P_PUF, ['..s..oooooo..s..', '...oYYYYYYYYo...', '.soYHYYYYYYYYos.', '.oYHYYYwwYYYYYo.', 'soYYYYYweYYYYYos', 'oYYYYYYwwYYYYYfo', 'oYYYYYYYYYYYYYfo', 'soYYYYYYYYYYYYos', 'oYYYYYYYYYYYYYYo', 'soYYYYYYYYYYYYos', '.oYdYYYYYYYYdYo.', '.soddYYYYYYddos.', '..oddddddddddo..', '...oddddddddo...', '..s..oooooo..s..', '................'])
# 跳跳蛙 16x14
P_FROG = dict(o='#1e4a14', G='#5fc14a', H='#9ce87a', d='#3a8a2a', w='#ffffff', e='#1a1020', b='#e8f0a0')
A('enemies/frog_0', P_FROG, ['...oo......oo...', '..oweo....oweo..', '..owwo....owwo..', '.ooGGooooooGGoo.', 'oGGGGGGGGGGGGGGo', 'oGHGGGGGGGGGGGGo', 'oGGGGGGGGGGGGGGo', 'oGGbbbbbbbbbbGGo', '.oGbbbbbbbbbbGo.', '.oGGGGGGGGGGGGo.', '..oGdGGGGGGdGo..', '.oGGo.oGGo.oGGo.', 'oGGo...oo...oGGo', 'oooo........oooo'])
A('enemies/frog_1', P_FROG, ['................', '................', '...oo......oo...', '..oweo....oweo..', '..owwo....owwo..', '.ooGGooooooGGoo.', 'oGGGGGGGGGGGGGGo', 'oGHGGGGGGGGGGGGo', 'oGGbbbbbbbbbbGGo', '.oGbbbbbbbbbbGo.', '..oGGGGGGGGGGo..', '.oGGGGGGGGGGGGo.', 'oGGGo......oGGGo', 'oooo........oooo'])
# 湖蚌 Boss 24x16（闭合 / 张开）
P_CLAM = dict(o='#2a2a40', S='#9aa0c0', H='#d8dcf0', s='#6a7098', p='#ffb6d5', P='#ffffff', m='#e86a8a', e='#1a1020')
A('enemies/clam_0', P_CLAM, ['........oooooooo........', '.....oooHHHHHHHHooo.....', '...ooHHHSSSSSSSSHHHoo...', '..oHHSSSSSSSSSSSSSSHHo..', '.oHSSSSSSSSSSSSSSSSSSHo.', '.oSSSSSSSSSSSSSSSSSSSSo.', 'oSSSSSSSSSSSSSSSSSSSSSSo', 'oooooooooooooooooooooooo',
'oSSSSSSSSSSSSSSSSSSSSSSo', '.oSSSSSSSSSSSSSSSSSSSSo.', '.osSSSSSSSSSSSSSSSSSSso.', '..ossSSSSSSSSSSSSSSsso..', '...oosssssssssssssoo....'[:24], '.....oooosssssoooo......', '........oooooo..........', '........................'])
A('enemies/clam_1', P_CLAM, ['..oooooooooooooooooooo..', '.oHHHHHHHHHHHHHHHHHHHHo.', '.oHSSSSSSSSSSSSSSSSSSHo.', '..oSSSSSSSSSSSSSSSSSSo..', '...ooSSSSSSSSSSSSSSoo...', '.....oooooooooooooo.....', '.......oppPPPPppo.......', '......opPPPPPPPPpo......',
'......opPPmPPmPPpo......', '......opPPPeePPPpo......', '.......oppPPPPppo.......', 'oSSSSSSSoooooooSSSSSSSSo', '.oSSSSSSSSSSSSSSSSSSSSo.', '..ossSSSSSSSSSSSSSSsso..', '....oosssssssssssssoo...', '.......oooooooooo.......'])
# 村民伊布用角色图；对话用 ui/bubble

# ---------------- 输出 ----------------
def render(rows, pal):
    w, h = len(rows[0]), len(rows)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            ch = rows[y][x]
            if ch == '.' or ch == ' ': continue
            c = pal[ch]; img.putpixel((x, y), (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255))
    return img

if __name__ == '__main__':
    for name, (rows, pal) in ASSETS.items():
        p = os.path.join(ROOT, name + '.png'); os.makedirs(os.path.dirname(p), exist_ok=True)
        render(rows, pal).save(p)
    print('wrote', len(ASSETS), 'assets to', os.path.abspath(ROOT))
