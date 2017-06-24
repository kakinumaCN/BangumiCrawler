# -*- coding: utf-8 -*-
import urllib2
import re
import json
import time

class BangumiUser:

    def __init__(self):
        self.id = -1
        self.name = "name"
        self.timeline = []

if __name__ == '__main__':
    bgmId = 0
    userName = ''
    # timeline
    for bgmId in range(1,2):
        url = "http://bangumi.tv/user/" + str(bgmId) + "/timeline"
        print url
        # time.sleep(1)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content = response.read()
        # print content.decode("utf-8").encode("UTF-8")

        pattern = re.compile('<div id="timeline">(.*?)<div id="tmlPager">', re.S)
        items = re.findall(pattern, content)

        timelinePattern = re.compile('<h4 class="Header">(.*?)</ul>',re.S)
        timelineItmes = re.findall(timelinePattern,items[0])

        count = 0
        for item in timelineItmes:
            print count
            timelineContent = str(item).decode("utf-8").encode("UTF-8")
            count +=1
            lastTime = ""
            i = 0
            while True:
                if timelineContent[i] == '<':
                    break
                else:
                    lastTime += timelineContent[i]
                i += 1
            print lastTime
