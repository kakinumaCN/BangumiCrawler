# -*- coding: utf-8 -*-
import urllib2
import re
import json
# 1看过 http://bangumi.tv/anime/list/kakinuma/collect
#     http://bangumi.tv/anime/list/kakinuma/collect?page=2

# http://bangumi.tv/anime/list/kakinuma/collect?orderby=rate
# http://bangumi.tv/anime/list/kakinuma/collect?orderby=rate&page=2

# 2搁置 http://bangumi.tv/anime/list/kakinuma/on_hold
# 3抛弃 http://bangumi.tv/anime/list/kakinuma/dropped
# 4在看 http://bangumi.tv/anime/list/kakinuma/do

class Bangumi:

    def __init__(self):
        self.id = -1
        self.star = -1
        self.status = -1
        self.name = "name"

if __name__ == '__main__':
    bgmlist = []
    countCollect = 0
    starCountCollect = 0
    starCollect = 0.0
    userName = 'everpcpc'

    # page 1
    url = "http://bangumi.tv/anime/list/" + userName + "/collect?orderby=rate"
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    pattern = re.compile('<li id="item_(.*?)" class=".*?">.*?<h3>.*?<a href="/subject/.*?" class="l">(.*?)</a>.*?</h3>.*?<p class="collectInfo">(.*?)</p>.*?</li>', re.S)
    pageCountPattern = re.compile('&nbsp;/&nbsp;(.*?)&nbsp;', re.S)
    items = re.findall(pattern, content)
    pageCount = re.findall(pageCountPattern, content)
    print "page1 start"
    for item in items:
        bgm = Bangumi()
        bgm.id = item[0]
        bgm.name = item[1]
        isStar = re.search('class="sstars', item[2])
        if isStar:
            starPattern = re.compile('<span class="sstars(.*?) starsinfo">.*?')
            stars = re.findall(starPattern, item[2])
            bgm.star = stars[0]
            starCountCollect += 1
            starCollect += float(stars[0])
        else:
            bgm.star = -1
        bgmlist.append({'status': bgm.status, 'star': bgm.star, 'id': bgm.id, 'name': bgm.name})
        print bgm.name
        countCollect += 1
    print "page1 end"
    print countCollect

    # page 2 ~ ?
    for pageNum in range(2, int(pageCount[0]) + 1):
        url = "http://bangumi.tv/anime/list/" + userName + "/collect?orderby=rate&page=" + str(pageNum)
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print e.code
        content = response.read().decode("utf-8")
        pattern = re.compile('<li id="item_(.*?)" class=".*?">.*?<h3>.*?<a href="/subject/.*?" class="l">(.*?)</a>.*?</h3>.*?<p class="collectInfo">(.*?)</p>.*?</li>', re.S)
        items = re.findall(pattern, content)
        print "page" + str(pageNum) + "start"
        for item in items:
            bgm = Bangumi()
            bgm.id = item[0]
            bgm.name = item[1]
            isStar = re.search('class="sstars', item[2])
            if isStar:
                starPattern = re.compile('<span class="sstars(.*?) starsinfo">.*?')
                stars = re.findall(starPattern, item[2])
                bgm.star = stars[0]
                starCountCollect += 1
                starCollect += float(stars[0])
            else:
                bgm.star = -1
            bgmlist.append({'status': bgm.status, 'star': bgm.star, 'id': bgm.id, 'name': bgm.name})
            countCollect += 1
        print "page" + str(pageNum) + "end"
        print countCollect
    fp = open('my.json', 'w+')
    json.dump(bgmlist, fp)
    print countCollect
    print starCountCollect
    print starCollect
    print starCollect/starCountCollect

# todo 1 页面的有效性检验  2 写成json  3 ajax交互 4 bug-e.g.魔豆传奇