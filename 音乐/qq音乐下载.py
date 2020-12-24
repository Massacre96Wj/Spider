# -*- coding: UTF-8 -*-
"""
@Author ：WangJie
@Date   ：2020/12/2 22:01 
@Desc   ：
"""
from requests_html import HTMLSession
import urllib.request, os, json
from urllib.parse import quote

class QQ_Music():
    def __init__(self):
        self.get_music_url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&w={}&format=json&platform=yqq.json'
        self.get_song_url='https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"602087500","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'
        # self.download_url='http://dl.stream.qqmusic.qq.com/'            # https://isure.stream.qqmusic.qq.com/
        self.download_url='https://isure.stream.qqmusic.qq.com/'            # https://isure.stream.qqmusic.qq.com/
        if not os.path.exists("./music"):
            os.mkdir('./music')

    def parse_url(self, url):
        session = HTMLSession()
        response = session.get(url)
        return response.content.decode()

    def get_music_list(self, keyword):
        music_dirt=json.loads(self.parse_url(self.get_music_url.format(quote(keyword))))
        music_list=music_dirt['data']['song']['list']
        # print(music_list)
        song_list=[]
        for music in music_list:
            sing_name=music['singer'][0]['name']
            song_name=music['title_hilight'].replace(r"</em>", "").replace("<em>", "")
            song_list.append({'songmid':music['mid'], 'singer':sing_name,'song_name':song_name})
            print(str(len(song_list))+'、'+sing_name+'--'+song_name)
        return song_list

    def download(self, song):
        song_dirt = json.loads(self.parse_url(self.get_song_url%song['songmid']))
        download_url = song_dirt["req_0"]["data"]["midurlinfo"][0]["purl"]
        print(download_url)
        if download_url:
            try:
                # 根据音乐url地址，用urllib.request.retrieve直接将远程数据下载到本地
                urllib.request.urlretrieve(self.download_url+download_url, './music/' + song['song_name'] + '.mp3')
                print('Successfully Download:' + song['singer']+'--'+song['song_name'] + '.mp3')
            except:
                print('Download wrong~')
if __name__ == '__main__':
    qqmusic=QQ_Music()
    while True:
        keyword = input('请输入要下载的歌曲名：')
        print('-----------歌曲《' + keyword + '》的版本列表------------')
        music_list = qqmusic.get_music_list(keyword)
        while 1:
            song_num = input('请输入要下载的歌曲序号：')
            try:
                if 1 <= int(song_num) <= 10:
                    qqmusic.download(music_list[int(song_num) - 1])
            except:
                break
        exit = input("退出输入N/n")
        if exit in ('N', 'n'):
            break

