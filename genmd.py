# -*- coding: utf_8 -*-

import sqlite3
import sys  

# sys.setdefaultencoding('utf_8')

def githublink(vid,fn,text):
    baseurl = "https://github.com/jungtosociety/dharma-qna/raw/master/sub"
    if fn is not None and fn != '' :
        return "[%s](%s/%s/%s)" % (text,baseurl,vid,fn) 
    else:
        return ''

def gen_table(f,predicate,orderby):
    f.write('| NO | TITLE         | YT | AM | XLS | PUBDATE | EN | FR | DE |\n')
    f.write('|----| ------------- |----|----|-----|---------|----|----|----|\n')

    for row in c.execute('SELECT v.vid,en.title,v.xlsfn,v.pubdate,v.youtube,v.amara,en.fn,fr.fn,de.fn \
                            FROM video v \
                            LEFT OUTER JOIN en ON v.vid = en.vid \
                            LEFT OUTER JOIN fr ON v.vid = fr.vid \
                            LEFT OUTER JOIN de ON v.vid = de.vid \
                           WHERE '+predicate+' \
                           ORDER BY '+orderby+' \
                             ' ):
        vid     = row[0]
        title   = row[1] #.encode('utf8')
        xlsfn   = row[2]
        pubdate = row[3]
        youtube = row[4]
        amara   = row[5]
        fn_en   = row[6]
        fn_fr   = row[7]
        fn_de   = row[8]
        # titlelink = "[%s](https://youtu.be/%s)" % (vid, title, youtube)
        titlelink = title
        nolink = "[%s](sub/%s)" % (vid,vid)
        xlslink = githublink(vid,xlsfn,'![](img/excel.png)')
        utubelink = "[<img src=img/youtube.png width=25>](https://youtu.be/%s)" % (youtube)
        amaralink = "[<img src=img/amara.png width=25>](http://amara.org/en/videos/%s)" % (amara) if amara is not None else ''
        enlink = githublink(vid,fn_en,'en')
        frlink = githublink(vid,fn_fr,'fr')
        delink = githublink(vid,fn_de,'de')
        f.write("| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" % ( nolink, titlelink, utubelink, amaralink, xlslink, pubdate, enlink, frlink, delink ))

c = sqlite3.connect('dharmaqna.db')

f = open('PROJECTS.md', 'w')
f.write('## Published\n\n');
gen_table(f,'status=\'published\'','v.puborder DESC')

f.write('## Work In Progress\n\n');
gen_table(f,'status IS NULL','v.puborder ASC')
f.close()

