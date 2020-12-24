import scrapy
import json
from qq_music.items import QqMusicItem
from scrapy import Request


class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'
    allowed_domains = ['y.qq.com']

    start_urls = [
        'https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22singerList%22%3A%7B%22module%22%3A%22Music.SingerListServer' \
        '%22%2C%22method%22%3A%22get_singer_list%22%2C%22param%22%3A%7B%22area%22%3A-100%2C%22sex%22%3A-100%2C%22genr' \
        'e%22%3A-100%2C%22index%22%3A-100%2C%22sin%22%3A{num}%2C%22cur_page%22%3A{id}%7D%7D%7D']  # 其实爬取地址
    song_down = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&ci' \
                'd=205361747&songmid={songmid}&filename=C400{songmid}.m4a&guid=9082027038'  # 歌曲下载地址
    song_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?singermid={singer_mid}&order=listen&num={sum}'  # 歌曲列表
    lrc_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid={musicid}'  # 歌词列表
    discuss_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?cid=205360772&reqtype=2&biztype=1&topid=' \
                  '{song_id}&cmd=8&pagenum=0&pagesize=25'  # 歌曲评论

    # 构造请求，爬取的页数。
    def start_requests(self):
        for i in range(1, self.settings.get('MAX_PAGE') + 1):  # 在配置信息里获取爬取页数
            yield Request(self.start_urls[0].format(num=80 * (i - 1), id=i), callback=self.parse_user)

    def parse_user(self, response):
        """
        依次爬取歌手榜的用户信息
        singer_mid：用户mid
        singer_name：用户名称
        返回爬取用户热歌信息。
        :param response:
        :return:
        """
        singer_list = json.loads(response.text).get('singerList').get('data').get('singerlist')  # 获取歌手列表
        for singer in singer_list:
            singer_mid = singer.get('singer_mid')  # 歌手mid
            singer_name = singer.get('singer_name')  # 歌手名字
            yield Request(self.song_url.format(singer_mid=singer_mid, sum=self.settings.get('SONGER_NUM')),
                          callback=self.parse_song, meta={'singer_name': singer_name})  # 爬取歌手的热歌

    def parse_song(self, response):
        """
        爬取歌手下面的热歌
        歌曲id是获取评论用的
        歌曲mid是获取歌曲下载地址用的
        :param response:
        :return:
        """
        songer_list = json.loads(response.text).get('data').get('list')
        for songer_info in songer_list:
            music = QqMusicItem()
            singer_name = response.meta.get('singer_name')  # 歌手名字
            song_name = songer_info.get('musicData').get('songname')  # 歌曲名字
            music['singer_name'] = singer_name
            music['song_name'] = song_name
            song_id = songer_info.get('musicData').get('songid')  # 歌曲id
            music['id'] = song_id
            song_mid = songer_info.get('musicData').get('songmid')  # 歌曲mid
            musicid = songer_info.get('musicData').get('songid')  # 歌曲列表

            yield Request(url=self.discuss_url.format(song_id=song_id), callback=self.parse_comment,
                          meta={'music': music, 'musicid': musicid, 'song_mid': song_mid})

    def parse_comment(self, response):
        """
        歌曲的评论
        :param response:
        :return:
        """
        comments = json.loads(response.text).get('hot_comment').get('commentlist')  # 爬取一页的热评
        if comments:
            comments = [{'comment_name': comment.get('nick'), 'comment_text': comment.get('rootcommentcontent')} for
                        comment in comments]
        else:
            comments = 'null'
        music = response.meta.get('music')
        music['comment'] = comments
        musicid = response.meta.get('musicid')  # 传递需要的参数
        song_mid = response.meta.get('song_mid')
        yield Request(url=self.lrc_url.format(musicid=musicid), callback=self.parse_lrc,
                      meta={'music': music, 'song_mid': song_mid})

    def parse_lrc(self, response):
        """
        爬取歌曲的歌词
        :param response:
        :return:
        """
        music = response.meta.get('music')
        music['lrc'] = response.text
        song_mid = response.meta.get('song_mid')
        yield Request(url=self.song_down.format(songmid=song_mid), callback=self.parse_url,
                      meta={'music': music, 'songmid': song_mid})

    def parse_url(self, response):
        """
        解析歌曲下载地址的url
        :param response:
        :return:
        """
        song_text = json.loads(response.text)
        song_mid = response.meta.get('songmid')
        vkey = song_text['data']['items'][0]['vkey']  # 加密的参数
        music = response.meta.get('music')
        if vkey:
            music['song_url'] = 'http://dl.stream.qqmusic.qq.com/C400' + song_mid + '.m4a?vkey=' + \
                                vkey + '&guid=9082027038&uin=0&fromtag=66'
        else:
            music['song_url'] = 'null'
        yield music
