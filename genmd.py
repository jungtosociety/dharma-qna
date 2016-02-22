# -*- coding: utf_8 -*-

import sqlite3
import sys  

# sys.setdefaultencoding('utf_8')


def gen_table(f,predicate,orderby):
    f.write('| NO | TITLE         | YT | AM | XLS | PUBLISHED | EN | FR | DE |\n')
    f.write('|----| ------------- |----|----|-----|-----------|----|----|----|\n')

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
        # xlslink = "[![](img/excel.png)](sub/%s/%s)" % (vid,xlsfn)
        xlslink = "[![](img/excel.png)](https://github.com/jungtosociety/dharma-qna/raw/master/sub/%s/%s)" % (vid,xlsfn)
        utubelink = "[<img src=img/youtube.png width=25>](https://youtu.be/%s)" % (youtube)
        amaralink = "[<img src=img/amara.png width=25>](http://amara.org/en/videos/%s)" % (amara) if amara is not None else ''
        # enlink  = "[en](sub/%s/%s)" % (vid,fn_en) if fn_en is not None else ''
        # frlink = "[fr](sub/%s/%s)" % (vid,fn_fr) if fn_fr is not None else ''
        # delink = "[de](sub/%s/%s)" % (vid,fn_de) if fn_de is not None else ''
        enlink = "[en](https://github.com/jungtosociety/dharma-qna/raw/master/sub/%s/%s)" % (vid,fn_en) if fn_en is not None else ''
        frlink = "[fr](https://github.com/jungtosociety/dharma-qna/raw/master/sub/%s/%s)" % (vid,fn_fr) if fn_fr is not None else ''
        delink = "[de](https://github.com/jungtosociety/dharma-qna/raw/master/sub/%s/%s)" % (vid,fn_de) if fn_de is not None else ''
        f.write("| %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" % ( nolink, titlelink, utubelink, amaralink, xlslink, pubdate, enlink, frlink, delink ))

c = sqlite3.connect('dharmaqna.db')

f = open('PROJECTS.md', 'w')
f.write('## Published\n\n');
gen_table(f,'status=\'published\'','v.puborder DESC')

f.write('## Work In Progress\n\n');
gen_table(f,'status IS NULL','v.puborder ASC')
f.close()

