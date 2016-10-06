# -*- coding: utf_8 -*-

import sqlite3
import sys  
import subprocess

import os # for probeExcelFile
import re # for probeExcelFile

# sys.setdefaultencoding('utf_8')

# cmd[0]   command alias to generate log file
# cmd[1:]  command line program and its arguments 
def run_cmd(cmd,raise_exception=True):
    command = ' '.join(cmd[0:])
    # print command
    # command = 'php -r "echo gethostname();"'
    p = subprocess.Popen(command, universal_newlines=True, shell=True, 
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = p.stdout.read()
    retcode = p.wait()
    if retcode != 0 and raise_exception:
        raise Exception("failed to execute "+command)
    return text
    # return retcode

def utf8(str):
    return unicode(str if str is not None else '').encode('utf8')    

# returns excel file of given vid
def getxlsfn(vid):
    files=os.listdir('sub/'+vid)
    regex = re.compile('.*'+vid+'.*xlsx$')
    matches = [string for string in files if re.match(regex, string)]
    if len(matches) != 0:
        return matches[0]
    else:
        return ''

def getsubfn(vid,lang):
    files=os.listdir('sub/'+vid)
    regex = re.compile(lang+'-'+vid+'.*sbv$')
    matches = [string for string in files if re.match(regex, string)]
    if len(matches) != 0:
        return matches[0]
    else:
        return ''

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

    for row in c.execute('SELECT v.vid,en.title,v.pubdate,v.youtube,v.amara \
                            FROM video v \
                            LEFT OUTER JOIN en ON v.vid = en.vid \
                           WHERE status=\'published\' \
                           ORDER BY v.pubdate DESC \
                             ' ):
        vid     = row["vid"]
        title   = row["title"] #.encode('utf8')
        xlsfn   = getxlsfn(vid)
        pubdate = row["pubdate"]
        youtube = row["youtube"]
        amara   = row["amara"]
        fn_en   = getsubfn(vid,'en')
        fn_fr   = getsubfn(vid,'fr')
        fn_de   = getsubfn(vid,'de')
        fn_cn   = getsubfn(vid,'cn')
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

def gentab_subtitling(f,status=None):
    f.write('| NO | TITLE / TITLE(EN) | YT / DUR | XLS | AMA | ASSIGNED / PUBDATE | NOTE / WORKINGDATE  |\n')
    f.write('|----| ----------------- |----------|-----|-----|--------------------|---------------------|\n')
             
    if status is not None:
      whereorderby = 'WHERE status=\''+status+'\' ORDER BY v.pubdate ASC'
    else:
      whereorderby = 'WHERE status IS NULL ORDER BY v.pubdate ASC, v.youtube DESC'

    for row in c.execute('SELECT v.vid, v.title, v.pubdate, v.youtube, v.amara, \
                                 v.subworker, v.subbegin, v.subend, v.memo, \
                                 v.playtime, en.title as entitle \
                            FROM video v \
                            LEFT OUTER JOIN en ON v.vid = en.vid \
                            '+whereorderby ):
        vid     = row["vid"]
        title   = utf8(row["title"])
        xlsfn   = getxlsfn(vid)
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
        f.write("| %s | %s   | %s | %s | %s | %s      | %s    |\n" % ( nolink, title, utubelink, xlslink, amaralink, worker, memo ))
        f.write("|    | %s   | %s |    |    | %s      | %s ~ %s |\n" % ( entitle, playtime, pubdate, begin, end ))



def genReadme(subid=None):

    # langname: language name like Englith
    # langcode: language code like en
    def printSubInfoPerLang(f, row, vid, langname, langcode):
        subfn = getsubfn(vid,langcode)
        if row[langcode+"title"] is not None and row[langcode+"title"] != '' :
            f.write("| "+langname+" Subtitle | "+utf8(githublink(vid,subfn,row[langcode+"title"]))+"<br>"+
                                               "by "+utf8(row[langcode+"con"])+"<br>"+
                                               "on "+utf8(row[langcode+"pubdate"])+"<br>"+"|\n")
        else:
            f.write("| "+langname+" Subtitle | N/A |\n")

    c = sqlite3.connect('dharmaqna.db')
    c.row_factory = sqlite3.Row

    if subid is not None:
        whereclause = 'WHERE v.vid = '+str(subid)
    else:
        whereclause = ''
    for row in c.execute('SELECT v.vid,v.title,v.pubdate,v.youtube_org,v.youtube,v.amara, \
                                 v.subworker,v.subbegin,v.subend,v.memo,v.playtime, \
                                 v.xdim, v.ydim, \
                                 ko.title as kotitle, ko.contributors || \',subtitle(\' || v.subworker || \')\' as kocon, v.pubdate as kopubdate, \
                                 en.title as entitle, en.contributors || \',subtitle(\' || v.subworker || \')\' as encon, v.pubdate as enpubdate, \
                                 fr.title as frtitle, fr.contributors as frcon, fr.pubdate as frpubdate, \
                                 de.title as detitle, de.contributors as decon, de.pubdate as depubdate, \
                                 cn.title as cntitle, cn.contributors as cncon, cn.pubdate as cnpubdate, \
                                 th.title as thtitle, th.contributors as thcon, th.pubdate as thpubdate \
                            FROM video v \
                 LEFT OUTER JOIN ko ON v.vid = ko.vid \
                 LEFT OUTER JOIN en ON v.vid = en.vid \
                 LEFT OUTER JOIN fr ON v.vid = fr.vid \
                 LEFT OUTER JOIN de ON v.vid = de.vid \
                 LEFT OUTER JOIN cn ON v.vid = cn.vid \
                 LEFT OUTER JOIN th ON v.vid = th.vid \
                            '+whereclause+' \
                           ORDER BY v.pubdate ASC ' ):
        vid     = row["vid"]
        nolink = utf8("[%s](sub/%s)" % (vid,vid))        
        xlslink = utf8(githublink(vid,getxlsfn(vid)))
        utubelink_org = utf8("[https://youtu.be/%s](https://youtu.be/%s)" % (row["youtube_org"],row["youtube_org"]) if row["youtube_org"] is not None else '')
        utubelink = utf8("[https://youtu.be/%s](https://youtu.be/%s)" % (row["youtube"],row["youtube"]) if row["youtube"] is not None else '')
        amaralink = utf8("[http://amara.org/en/videos/%s](http://amara.org/en/videos/%s)" % (row["amara"],row["amara"]) if row["amara"] is not None else '')
        begin   = utf8(row["subbegin"])
        end     = utf8(row["subend"])
        memo    = utf8(row["memo"])
        
        
        curr_fn = 'sub/'+vid+'/README.md'
        f = open(curr_fn, 'w')
        f.write("|  key  |  value  |\n")
        f.write("|-------|---------|\n")
        f.write("| ID            | "+vid+" |\n")
        printSubInfoPerLang(f,row,vid,"Korean","ko")
        printSubInfoPerLang(f,row,vid,"English","en")
        printSubInfoPerLang(f,row,vid,"French","fr")
        printSubInfoPerLang(f,row,vid,"German","de")
        printSubInfoPerLang(f,row,vid,"Chinese","cn")
        f.write("| Original YouTube Link  | "+utubelink_org+" |\n")
        f.write("| YouTube Link  | "+utubelink+" |\n")
        f.write("| Amara Link    | "+amaralink+" |\n")
        f.write("| Transcript(ko/en) | "+xlslink+" |\n")
        f.write("| Playtime | "+utf8(row["playtime"])+" |\n")
        f.write(utf8("| Resolution | %sx%s|\n" % (row["xdim"],row["ydim"])))
        f.close()

        if run_cmd(['git','diff',curr_fn],raise_exception=False) != '':
            print ' - updated '+curr_fn

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
    if run_cmd(['git','diff','PROJECTS.md'],raise_exception=False) != '':
        print ' - updated '+'PROJECTS.md'

    f = open('SUBTITLING.md', 'w')
    f.write('## 3. Subtitling\n\n')
    gentab_subtitling(f,'sub')
    f.write('## 4. Reviewing\n\n')
    gentab_subtitling(f,'review')
    f.write('## 1. Video Converting\n\n')
    gentab_subtitling(f,'video')
    f.write('## 2. Ready to Subtitle (unassigned)\n\n')
    gentab_subtitling(f,'unassigned')
    f.write('## 5. Published\n\n')
    gentab_subtitling(f,'published')
    f.close()
    if run_cmd(['git','diff','SUBTITLING.md'],raise_exception=False) != '':
        print ' - updated '+'SUBTITLING.md'


    if len(sys.argv) < 2 :
        genReadme()
    else:
        genReadme(sys.argv[1])
    