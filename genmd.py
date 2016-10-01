# -*- coding: utf_8 -*-

import sqlite3
import sys  

# sys.setdefaultencoding('utf_8')

def utf8(str):
    return unicode(str if str is not None else '').encode('utf8')    

def githublink(vid,fn,text=None):
    baseurl = "https://github.com/jungtosociety/dharma-qna/raw/master/sub"
    if text is None:
        text = fn
    if fn is not None and fn != '' :
        return "[%s](%s/%s/%s)" % (text,baseurl,vid,fn) 
    else:
        return ''

def gentab_published(f):
#     f.write('---\n\
# layout: page\n\
# title: Project List\n\
# permalink: /project.html\n\
# ---\n\
# \n\n');

    f.write('| NO | TITLE         | YT | AM | XLS | PUBDATE | EN | FR | DE | CN |\n')
    f.write('|----| ------------- |----|----|-----|---------|----|----|----|----|\n')

    for row in c.execute('SELECT v.vid,en.title,v.xlsfn,v.pubdate,v.youtube,v.amara, \
                                 en.fn as enfn, fr.fn as frfn ,de.fn as defn, cn.fn as cnfn \
                            FROM video v \
                            LEFT OUTER JOIN en ON v.vid = en.vid \
                            LEFT OUTER JOIN fr ON v.vid = fr.vid \
                            LEFT OUTER JOIN de ON v.vid = de.vid \
                            LEFT OUTER JOIN cn ON v.vid = cn.vid \
                           WHERE status=\'published\' \
                           ORDER BY v.pubdate DESC \
                             ' ):
        vid     = row["vid"]
        title   = row["title"] #.encode('utf8')
        xlsfn   = row["xlsfn"]
        pubdate = row["pubdate"]
        youtube = row["youtube"]
        amara   = row["amara"]
        fn_en   = row["enfn"]
        fn_fr   = row["frfn"]
        fn_de   = row["defn"]
        fn_cn   = row["cnfn"]
        titlelink = title
        nolink = "[%s](https://github.com/jungtosociety/dharma-qna/blob/master/sub/%s)" % (vid,vid)
        xlslink = githublink(vid,xlsfn,'![](img/excel.png)')
        utubelink = "[![](img/youtube.png)](https://youtu.be/%s)" % (youtube)
        amaralink = "[![](img/amara.png)](http://amara.org/en/videos/%s)" % (amara) if amara is not None else ''
        enlink = githublink(vid,fn_en,'en')
        frlink = githublink(vid,fn_fr,'fr')
        delink = githublink(vid,fn_de,'de')
        cnlink = githublink(vid,fn_cn,'cn')
        f.write("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" % ( nolink, titlelink, utubelink, amaralink, xlslink, pubdate, 
                enlink, frlink, delink, cnlink ))

def gentab_subtitling(f,wip=True):
    f.write('| NO | TITLE         | YT/AM | XLS/PUBDATE | ASSIGNED | REVIEW/NOTE |\n')
    f.write('|----| ------------- |-------|-------------|----------|--------|\n')
             
    if wip:
      whereorderby = 'WHERE status IS NULL ORDER BY v.pubdate ASC'
    else:
      whereorderby = 'WHERE status=\'published\' ORDER BY v.pubdate ASC'

    for row in c.execute('SELECT v.vid, v.title, v.xlsfn, v.pubdate, v.youtube, v.amara, \
                                 v.subworker, v.subbegin, v.subend, v.memo, \
                                 v.playtime, en.title as entitle \
                            FROM video v \
                            LEFT OUTER JOIN en ON v.vid = en.vid \
                            '+whereorderby ):
        vid     = row["vid"]
        title   = utf8(row["title"])
        xlsfn   = row["xlsfn"]
        pubdate = utf8(row["pubdate"])
        youtube = row["youtube"]
        amara   = row["amara"]
        worker  = utf8(row["subworker"])
        begin   = utf8(row["subbegin"])
        end     = utf8(row["subend"])
        memo    = utf8(row["memo"])
        playtime  = utf8(row["playtime"])
        entitle   = row["entitle"]
        entitle   = utf8("%s" % (entitle) if entitle is not None else '') 
        nolink = utf8("[%s](sub/%s)" % (vid,vid))
        xlslink = utf8(githublink(vid,xlsfn,'![](img/excel.png)'))
        utubelink = utf8("[![](img/youtube.png)](https://youtu.be/%s)" % (youtube) if youtube is not None else '')
        amaralink = utf8("[![](img/amara.png)](http://amara.org/en/videos/%s)" % (amara) if amara is not None else '')
        f.write("| %s | %s   | %s %s      | %s | %s      |    |\n" % ( nolink, title, utubelink, playtime, xlslink, worker ))
        f.write("|    | %s   | %s amara   | %s | %s ~ %s | %s |\n" % ( entitle, amaralink, pubdate, begin, end, memo ))

if __name__ == "__main__":
    c = sqlite3.connect('dharmaqna.db')
    c.row_factory = sqlite3.Row

    f = open('PROJECTS.md', 'w')
    f.write('* KO: Korean Subtitle\n')
    f.write('* EN: English Subtitle\n')
    f.write('* DE: German(Deutsch) Subtitle\n')
    f.write('* CN: Chinese(中文) Subtitle\n')
    f.write('\n')
    gentab_published(f)
    f.close()

    f = open('SUBTITLING.md', 'w')
    f.write('## Work In Progress\n\n')
    gentab_subtitling(f)
    f.write('## Published\n\n')
    gentab_subtitling(f,False)
    f.close()
