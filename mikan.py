import urllib.request
import urllib.parse
import re
import sqlite3
import time
import uuid

global_sql_conn = sqlite3.connect('anime.db')
global_sql_conn.text_factory = str


def init_db():
    global global_sql_conn
    c = global_sql_conn.cursor()

    c.execute('''CREATE TABLE MIKAN
           (MIKANID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           SEASON         TEXT,
           COVERURL        TEXT,
           BGMID            INT,
           BGMSTAR      FLOAT);''')

    # c.execute('''CREATE TABLE REQUESTCACHE
    #        (URL TEXT PRIMARY KEY     NOT NULL,
    #        CONTENT           TEXT,
    #        TIME         LONG);''')

    global_sql_conn.commit()


def my_request(url):
    global global_sql_conn
    cur = global_sql_conn.cursor()
    cur.execute('SELECT CONTENT FROM REQUESTCACHE WHERE URL = \'' + url + '\'')
    rows = cur.fetchall()
    if len(rows) > 0:
        # return rows[0][0]
        fname = rows[0][0]
        with open('./cache/' + fname, "r", encoding='utf-8') as f:
            content = f.read()
            f.close()
        return content
    else:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"}
        req = urllib.request.Request(url=url, headers=headers, method="GET")
        response = urllib.request.urlopen(req)
        content = response.read().decode("utf-8")
        now = time.time()
        fid = uuid.uuid3(uuid.NAMESPACE_URL, url)

        with open('./cache/' + str(fid), "w", encoding='utf-8') as f:
            f.write(content)
            f.close()

        cur.execute('INSERT INTO REQUESTCACHE (URL,CONTENT,TIME) VALUES (\'' + url + '\',\'' + str(fid) + '\',' + str(now) + ')')
        global_sql_conn.commit()
        return content


def get_bgmid(mikanid):
    # global global_sql_conn
    # cur = global_sql_conn.cursor()
    # cur.execute('SELECT BGMID FROM MIKAN WHERE MIKANID=' + mikanid)
    # rows = cur.fetchall()
    # if len(rows) == 0:

    url = "https://mikanani.me/Home/Bangumi/" + str(mikanid)
    content = my_request(url)
    # <a class="w-other-c" target="_blank" href="http://bgm.tv/subject/341163">http://bgm.tv/subject/341163</a>
    pattern = re.compile(
        '<a class="w-other-c" target="_blank" href="http(s*?)://bgm.tv/subject/(.*?)">http(s*?)://bgm.tv/subject/(.*?)</a>'
    )
    items = re.findall(pattern, content)
    bgmid = items[0][1]
    return bgmid


def dec(a):
    aa = a.replace(';', '').replace('&#x', '\\u').encode('utf-8').decode('unicode_escape')
    return aa


def insert_from_mikan(year, season):
    # season = "冬"
    # print(urllib.parse.quote(season))
    global  global_sql_conn
    cur = global_sql_conn.cursor()

    url = "https://mikanani.me/Home/BangumiCoverFlowByDayOfWeek" \
          + "?year=" + str(year) \
          + "&seasonStr=" + urllib.parse.quote(season)
    content = my_request(url)

    # < ahref = "/Home/Bangumi/2681" target = "_blank" class ="an-text" title="影之诗F" > 影之诗F < / a >
    pattern = re.compile(
        '<a href="/Home/Bangumi/(.*?)" target="_blank" class="an-text" title="(.*?)">(.*?)</a>',
        re.S)

    items = re.findall(pattern, content)
    print(len(items))
    for item in items:
        id = item[0]
        name = dec(item[1])
        # bgmid = get_bgmid(id)
        # exec = 'INSERT OR IGNORE INTO MIKAN (MIKANID,BGMID,NAME) VALUES('+id+','+bgmid+',\''+ name +'\')'
        exec = 'INSERT OR REPLACE INTO MIKAN (MIKANID,NAME,SEASON) VALUES(' +id+ ','+'\''+ name +'\',\''+ str(year) +(season) +'\')'
        print(exec)
        cur.execute(exec)
        global_sql_conn.commit()


if __name__ == '__main__':
    init_db()
    insert_from_mikan(2023, "冬")
