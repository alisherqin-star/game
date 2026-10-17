# 用法：python3 tools/embed_sprites.py <sprites_b64.json>
# 把 {form: {normal: dataURI, shiny: dataURI}} 写入 index.html 的 SPRITE_PNG 标记之间。
import json, sys, os
data = json.load(open(sys.argv[1]))
html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
html = open(html_path, encoding='utf-8').read()
begin, end = '/* SPRITE_PNG_BEGIN */', '/* SPRITE_PNG_END */'
i, j = html.index(begin) + len(begin), html.index(end)
html = html[:i] + '\nconst SPRITE_PNG = ' + json.dumps(data, separators=(',', ':')) + ';\n' + html[j:]
open(html_path, 'w', encoding='utf-8').write(html)
print('embedded', len(data), 'forms')
