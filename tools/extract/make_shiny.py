# 用法：python3 tools/extract/make_shiny.py
# 从 sprites/characters/<形态>.png 生成 <形态>_shiny.png（按正作闪光配色做色相/饱和度映射）
import os, colorsys
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'sprites', 'characters')
def in_hue(h, lo, hi): return (lo <= h <= hi) if lo <= hi else (h >= lo or h <= hi)
# 规则：(色相下限, 上限, 饱和度下限, 亮度下限, 亮度上限) -> (目标色相, 最低饱和度, 饱和度倍率, 亮度增量)
RULES = {
  'eevee':    [((15, 60, 0.15, 0.2, 0.95), (42, 0.0, 0.35, 0.14))],                                   # 银白色
  'vaporeon': [((170, 230, 0.2, 0.15, 0.95), (300, 0.55, 1.0, 0.02))],                                 # 紫粉色
  'jolteon':  [((30, 70, 0.3, 0.2, 0.95), (76, 0.7, 1.0, 0.0))],                                       # 黄绿色
  'flareon':  [((350, 40, 0.3, 0.2, 0.85), (46, 0.8, 1.0, 0.1)), ((40, 70, 0.3, 0.6, 0.97), (54, 0.7, 1.0, 0.0))],   # 金黄身体、浅黄颈毛
  'leafeon':  [((10, 50, 0.3, 0.2, 0.95), (54, 0.6, 1.0, 0.03)), ((95, 175, 0.2, 0.15, 0.95), (165, 0.5, 1.0, -0.04))],  # 黄色皮毛、青绿叶子
  'glaceon':  [((170, 235, 0.2, 0.15, 0.95), (165, 0.6, 1.0, 0.0))],                                   # 青绿色
  'espeon':   [((250, 345, 0.04, 0.25, 0.95), (112, 0.5, 1.0, 0.02)), ((195, 250, 0.1, 0.15, 0.6), (125, 0.35, 1.0, 0.0))],  # 薄荷绿
  'umbreon':  [((30, 70, 0.4, 0.2, 0.95), (212, 0.75, 1.0, 0.0))],                                     # 蓝环
  'sylveon':  [((300, 25, 0.2, 0.2, 0.95), (205, 0.5, 1.0, 0.0)), ((185, 245, 0.2, 0.2, 0.95), (335, 0.5, 1.0, 0.0))],  # 粉蓝互换
}
def shinify(form, img):
    img = img.convert('RGBA'); px = img.load(); w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0: continue
            hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255); hh *= 360
            for (lo, hi, smin, lmin, lmax), (th, sfloor, smul, dl) in RULES[form]:
                if in_hue(hh, lo, hi) and s >= smin and lmin <= l <= lmax:
                    ns = max(sfloor, min(1, s * smul)); nl = max(0, min(1, l + dl))
                    nr, ng, nb = colorsys.hls_to_rgb(th / 360, nl, ns)
                    px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), a); break
    return img
if __name__ == '__main__':
    for form in RULES:
        shinify(form, Image.open(os.path.join(D, form + '.png'))).save(os.path.join(D, form + '_shiny.png')); print('shiny', form)
