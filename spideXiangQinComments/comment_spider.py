import re
import json
import time
import requests

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "comment.mobilem.360.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"
}
def comment_spider(param, file_name):
    base_url = "http://comment.mobilem.360.cn/comment/getComments?c=message&a=getmessage&&count=50"
    start = 0
    for i in range(1, 50):
        print("第{}页".format(i))
        url = base_url + param + "&start=" + str(start)
        r = requests.get(url, headers=headers)
        data = re.findall("{\"errno\"(.*)\);}catch\(e\){}", r.text)
        # 转为 Json 格式
        jdata = json.loads("{\"errno\"" + data[0])
        for message in jdata["data"]["messages"]:
            content = message["content"]
            # print(content)
            with open(file_name + ".txt", "a", encoding="utf-8") as f:
                f.write(content)
        start = start + 50
        time.sleep(2)

if __name__ == '__main__':
    bh = "&callback=jQuery17205354720451350314_1607248252542&baike=%E7%99%BE%E5%90%88%E7%BD%91+Android&"
    sjjy = "&callback=jQuery172013964937506690367_1607248176074&baike=%E4%B8%96%E7%BA%AA%E4%BD%B3%E7%BC%98android&"
    yy = "&callback=jQuery17209751470530428477_1607248309032&baike=%E6%9C%89%E7%BC%98%E5%A9%9A%E6%81%8B+Android&"
    # comment_spider(bh, "bh")
    # comment_spider(sjjy, "sjjy")
    comment_spider(yy, "yy")
