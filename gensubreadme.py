# -*- coding: utf_8 -*-

import sqlite3
import sys  
from genmd import utf8
from genmd import githublink
import subprocess


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

def genReadme(subid=None):

    # langname: language name like Englith
    # langcode: language code like en
    def printSubInfoPerLang(f, row, vid, langname, langcode):
        if row[langcode+"title"] is not None and row[langcode+"title"] != '' :
            f.write("| "+langname+" Subtitle | "+utf8(githublink(vid,row[langcode+"sub"],row[langcode+"title"]))+"<br>"+
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
    for row in c.execute('SELECT v.vid,v.title,v.xlsfn,v.pubdate,v.youtube_org,v.youtube,v.amara, \
                                 v.subworker,v.subbegin,v.subend,v.memo,v.playtime, \
                                 v.xdim, v.ydim, \
                                 ko.title as kotitle, ko.fn as kosub, ko.contributors || \',subtitle(\' || v.subworker || \')\' as kocon, v.pubdate as kopubdate, \
                                 en.title as entitle, en.fn as ensub, en.contributors || \',subtitle(\' || v.subworker || \')\' as encon, v.pubdate as enpubdate, \
                                 fr.title as frtitle, fr.fn as frsub, fr.contributors as frcon, fr.pubdate as frpubdate, \
                                 de.title as detitle, de.fn as desub, de.contributors as decon, de.pubdate as depubdate, \
                                 cn.title as cntitle, cn.fn as cnsub, cn.contributors as cncon, cn.pubdate as cnpubdate, \
                                 th.title as thtitle, th.fn as thsub, th.contributors as thcon, th.pubdate as thpubdate \
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
        xlslink = utf8(githublink(vid,row["xlsfn"]))
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
    if len(sys.argv) < 2 :
        genReadme()
    else:
        genReadme(sys.argv[1])
    
