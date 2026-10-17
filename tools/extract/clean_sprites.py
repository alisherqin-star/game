# 用法：python3 tools/extract/clean_sprites.py [sprites/characters]
# 清理切图产生的杂点：只保留主体连通块、填补内部空洞、抹平稀有杂色、补齐深色描边。
import os, sys
from collections import Counter, deque
from PIL import Image
import numpy as np

def clean(img):
    a = np.array(img.convert('RGBA')); h, w, _ = a.shape
    fg = a[:, :, 3] > 0
    # 1) 最大 8 连通块 + 面积 >= 6 且紧挨主体的块保留，其余删掉
    lab = np.zeros((h, w), int); comps = []
    for y in range(h):
        for x in range(w):
            if fg[y, x] and lab[y, x] == 0:
                cid = len(comps) + 1; lab[y, x] = cid; q = deque([(y, x)]); pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and fg[ny, nx] and lab[ny, nx] == 0: lab[ny, nx] = cid; q.append((ny, nx))
                comps.append(pts)
    main = max(range(len(comps)), key=lambda i: len(comps[i])) + 1
    keep = np.zeros((h, w), bool)
    for i, pts in enumerate(comps, 1):
        if i == main or len(pts) >= 6: 
            for (y, x) in pts: keep[y, x] = True
    a[~keep] = 0; fg = keep
    # 2) 填补被包围的透明孔（4 连通不接触边界）
    outside = np.zeros((h, w), bool); q = deque()
    for y in range(h):
        for x in range(w):
            if (y in (0, h - 1) or x in (0, w - 1)) and not fg[y, x]: outside[y, x] = True; q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not fg[ny, nx] and not outside[ny, nx]: outside[ny, nx] = True; q.append((ny, nx))
    holes = (~fg) & (~outside)
    for y in range(h):
        for x in range(w):
            if holes[y, x]:
                nb = [tuple(a[y+dy, x+dx]) for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= y+dy < h and 0 <= x+dx < w and fg[y+dy, x+dx]]
                if nb: a[y, x] = Counter(nb).most_common(1)[0][0]; fg[y, x] = True
    # 3) 稀有颜色（占比 < 4%）若被 3 个以上同色邻居包围则并入
    def pass_rare():
        cnt = Counter(tuple(a[y, x]) for y in range(h) for x in range(w) if fg[y, x]); total = sum(cnt.values()); changed = 0
        for y in range(h):
            for x in range(w):
                if not fg[y, x]: continue
                v = tuple(a[y, x])
                if cnt[v] >= total * 0.04: continue
                nb = [tuple(a[y+dy, x+dx]) for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= y+dy < h and 0 <= x+dx < w and fg[y+dy, x+dx]]
                if len(nb) >= 3:
                    c, n = Counter(nb).most_common(1)[0]
                    if n >= 3 and c != v: a[y, x] = c; changed += 1
        return changed
    for _ in range(3):
        if pass_rare() == 0: break
    # 4) 轮廓：与透明相邻的前景像素若偏亮，替换为该图最常见的深色（描边色）
    cnt = Counter(tuple(a[y, x]) for y in range(h) for x in range(w) if fg[y, x])
    lum = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    darks = [c for c in cnt if lum(c) < 70]
    outline = max(darks, key=lambda c: cnt[c]) if darks else min(cnt, key=lum)
    for y in range(h):
        for x in range(w):
            if not fg[y, x]: continue
            edge = any(not (0 <= y+dy < h and 0 <= x+dx < w) or not fg[y+dy, x+dx] for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)))
            if edge and lum(tuple(a[y, x])) > 110: a[y, x] = outline
    return Image.fromarray(a)

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'sprites', 'characters')
    for f in sorted(os.listdir(d)):
        if f.endswith('.png'):
            p = os.path.join(d, f); clean(Image.open(p)).save(p); print('cleaned', f)
