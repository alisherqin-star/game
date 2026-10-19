# 进度门检查：穷举拿能力的所有顺序，确认不会卡关、能走到终局。
# 用法：python3 tools/check_progression.py
# 门表对应 DESIGN.md 第 3.2 节和第 4 节。改设计时两边一起改：每一项列出「任意一组满足即可」的条件。
import sys

GATES = {
    # 序章
    '水伊布': [set()],                                        # 草原·池塘的水之石
    # 第一圈
    '雷伊布': [{'水伊布'}],                                    # 湖泊·柠檬岩（要游泳）
    '火伊布': [{'雷伊布'}, {'水伊布'}],                         # 雷电塔顶：塔门电网，或从池塘水底游进塔基
    '叶伊布': [{'火伊布'}, {'雷伊布'}],                         # 火山洞 → 森林山脚秘洞：荆棘烧开，或撞开旁边的裂岩
    # 第二圈
    '冰伊布': [{'叶伊布', '雷伊布'}, {'叶伊布', '火伊布'}],       # 湖泊北边二段跳上冰窟外围；雪峰的冰岩在冰墙后：雷撞或火融
    '三段跳': [{'叶伊布', '火伊布'}, {'叶伊布', '水伊布'}],       # 森林高台（二段跳或逆瀑布游上去）→ 古树之心（烧开腐根）
    '太阳伊布': [{'冰伊布'}, {'叶伊布'}],                        # 天空遗迹：冻住森林瀑布爬上去，或二段跳借风洞
    '瞬移': [{'太阳伊布'}],                                     # 风之塔要滑翔
    '冰桥': [{'冰伊布'}],                                       # 雪峰顶
    '电磁飞檐': [{'冰伊布'}, {'太阳伊布'}],                      # 雷电塔发电室：冻住冷却水管，或滑过去
    '月亮伊布': [{'太阳伊布'}, {'冰伊布'}],                      # 地下水道南边断崖：滑翔，或冻住飞过的蝙蝠踩过去
    # 第三圈
    '夜视': [{'月亮伊布'}],                                     # 影之祭坛（黑影墙）
    '仙子伊布': [{'月亮伊布'}],                                 # 糖果花园（黑影墙后的小路）+ 绒绒的约定
    '飘带钩爪': [{'仙子伊布'}],                                 # 糖果花园深处
    '深潜': [{'夜视'}],                                         # 湖底洞穴深处很黑
    '熔岩泳': [{'飘带钩爪'}],                                   # 火山洞深处荡过熔岩坑
    '影之封印': [{'夜视'}],
    '花园封印': [{'飘带钩爪'}],
    '海沟封印': [{'深潜'}],
    '核心封印': [{'熔岩泳'}],
}
EVOS = ['水伊布', '雷伊布', '火伊布', '叶伊布', '冰伊布', '太阳伊布', '月亮伊布', '仙子伊布']
FINAL = set(EVOS) | {'影之封印', '花园封印', '海沟封印', '核心封印'}   # 进化祭坛的锁门


def close(have):
    """拿到能拿的所有非进化项目（强化、封印），进化要玩家选择顺序。"""
    have = set(have)
    changed = True
    while changed:
        changed = False
        for k, opts in GATES.items():
            if k not in EVOS and k not in have and any(o <= have for o in opts):
                have.add(k); changed = True
    return have


def orders():
    out = []
    def dfs(have, seq):
        nxt = [e for e in EVOS if e not in have and any(o <= have for o in GATES[e])]
        if not nxt:
            out.append((seq, have)); return
        for e in nxt:
            dfs(close(have | {e}), seq + [e])
    dfs(close(set()), [])
    return out


def main():
    bad = [k for k, opts in GATES.items() for o in opts for need in o if need not in GATES]
    if bad:
        print('门表里引用了不存在的项目：', sorted(set(bad))); return 1
    res = orders()
    stuck = [seq for seq, have in res if not FINAL <= have]
    print(f'8 种进化一共有 {len(res)} 种合法顺序。')
    if stuck:
        print(f'有 {len(stuck)} 种顺序走不到终局，例如：', ' → '.join(stuck[0])); return 1
    print('所有顺序都能拿齐 8 种进化和 4 道封印，走到终局。')
    print('每种进化最早 / 最晚第几个拿到：')
    for e in EVOS:
        pos = [seq.index(e) + 1 for seq, _ in res]
        print(f'  {e}：{min(pos)} ～ {max(pos)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
