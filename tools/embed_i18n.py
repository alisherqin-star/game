"""Build the local language bank and embed it without changing game data."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def main():
 bank={}
 for n,line in enumerate((ROOT/'locales/translations.tsv').read_text().splitlines(),1):
  if not line.strip():continue
  row=line.split('\t');assert len(row)==3,(n,row)
  zh,ja,en=row;bank[zh]={'ja':ja,'en':en}
  # Dialog renderer splits speaker and body; make both individually translatable.
  if '：' in zh and zh.index('：')<9 and '：' in ja and ': ' in en:
   zname,zbody=zh.split('：',1);jname,jbody=ja.split('：',1);ename,ebody=en.split(': ',1)
   bank.setdefault(zname,{'ja':jname,'en':ename});bank[zbody]={'ja':jbody,'en':ebody}
 (ROOT/'locales/catalog.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
 runtime=(ROOT/'locales/runtime.js').read_text().replace('/* LOCALE_DATA */',json.dumps(bank,ensure_ascii=False,separators=(',',':')))
 html=ROOT/'index.html';s=html.read_text();block='/* I18N_BEGIN */\n'+runtime+'\n/* I18N_END */'
 if '/* I18N_BEGIN */' in s:s=re.sub(r'/\* I18N_BEGIN \*/.*?/\* I18N_END \*/',lambda m:block,s,flags=re.S)
 else:s=s.replace("'use strict';","'use strict';\n"+block,1)
 html.write_text(s);print('Embedded',len(bank),'translation keys in Chinese / Japanese / English')
if __name__=='__main__':main()
