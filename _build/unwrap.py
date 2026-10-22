import re
HREFS=['https://www.u-fukui.ac.jp/eng/','https://www.u-fukui.ac.jp/','https://pure.flib.u-fukui.ac.jp/en/persons/amil-khanzada/','https://pure.flib.u-fukui.ac.jp/ja/persons/amil-khanzada/','https://virufy.org']
def unwrap(s):
    for h in HREFS:
        e=re.escape(h)
        s=re.sub(r'<a class="institution" href="'+e+r'">(.*?)</a>',r'<span class="institution">\1</span>',s)
        s=re.sub(r'<a href="'+e+r'">(.*?)</a>',r'\1',s)
    return s
