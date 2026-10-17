# 用法：python3 tools/embed_assets.py
# 把 sprites/ 下所有 PNG 以 base64 写入 index.html 的 ASSET_PNG 标记之间（键为 "类别/文件名"，不含 .png）。
import os, json, base64
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
data = {}
for cat in sorted(os.listdir(os.path.join(root, 'sprites'))):
    d = os.path.join(root, 'sprites', cat)
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if f.endswith('.png'):
            data[f'{cat}/{f[:-4]}'] = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(d, f), 'rb').read()).decode()
html_path = os.path.join(root, 'index.html')
html = open(html_path, encoding='utf-8').read()
begin, end = '/* ASSET_PNG_BEGIN */', '/* ASSET_PNG_END */'
i, j = html.index(begin) + len(begin), html.index(end)
html = html[:i] + '\nconst ASSET_PNG = ' + json.dumps(data, separators=(',', ':')) + ';\n' + html[j:]
open(html_path, 'w', encoding='utf-8').write(html)
print('embedded', len(data), 'images,', sum(len(v) for v in data.values()) // 1024, 'KB')
