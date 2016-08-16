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
    c = sqlite3.connect('dharmaqna.db')
    c.row_factory = sqlite3.Row

    if subid is not None:
        whereclause = 'WHERE v.vid = '+str(subid)
    else:
        whereclause = ''
    for row in c.execute('SELECT v.vid,v.title,v.xlsfn,v.pubdate,v.youtube_org,v.youtube,v.amara, \
                                 v.subworker,v.subbegin,v.subend,v.subfinal,v.memo,v.playtime, \
                                 v.xdim, v.ydim, \
                                 ko.title as kotitle, ko.fn as kosub, ko.contributors as kocon, \
                                 en.title as entitle, en.fn as ensub, en.contributors as encon, \
                                 fr.title as frtitle, fr.fn as frsub, fr.contributors as frcon, fr.pubdate as frpubdate, \
                                 de.title as detitle, de.fn as desub, de.contributors as decon, de.pubdate as depubdate \
                            FROM video v \
                 LEFT OUTER JOIN ko ON v.vid = ko.vid \
                 LEFT OUTER JOIN en ON v.vid = en.vid \
                 LEFT OUTER JOIN fr ON v.vid = fr.vid \
                 LEFT OUTER JOIN de ON v.vid = de.vid \
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
        final   = utf8(row["subfinal"])
        memo    = utf8(row["memo"])
        
        
        curr_fn = 'sub/'+vid+'/README.md'
        f = open(curr_fn, 'w')
        f.write("|  key  |  value  |\n")
        f.write("|-------|---------|\n")
        f.write("| ID            | "+vid+" |\n")
        f.write("| Title         | "+utf8(row["title"])+" |\n")
        f.write("| Korean Subtitle | "+utf8(githublink(vid,row["kosub"]))+" |\n")
        f.write("| English Title | "+utf8(row["entitle"])+" |\n")
        f.write("| English Subtitle | "+utf8(githublink(vid,row["ensub"]))+" |\n")
        f.write("| Korean/English Published     | "+utf8(row["pubdate"])+" |\n")
        f.write("| Transcript Contributor(s)   | "+utf8(row["kocon"])+" |\n")
        f.write("| Translation Contributor(s)   | "+utf8(row["encon"])+" |\n")
        f.write("| Subtitling Contributor(s)   | "+utf8(row["subworker"])+" |\n")
        f.write("| French Title | "+utf8(row["frtitle"])+" |\n")
        f.write("| French Subtitle | "+utf8(githublink(vid,row["frsub"]))+" |\n")
        f.write("| French Subtitle Published | "+utf8(row["frpubdate"])+" |\n")
        f.write("| French Subtitle Contributor(s) | "+utf8(row["frcon"])+" |\n")
        f.write("| German Title | "+utf8(row["detitle"])+" |\n")
        f.write("| German Subtitle | "+utf8(githublink(vid,row["desub"]))+" |\n")
        f.write("| German Subtitle Published | "+utf8(row["depubdate"])+" |\n")
        f.write("| German Subtitle Contributor(s) | "+utf8(row["decon"])+" |\n")
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
    
