# -*- coding: UTF-8 -*-
"""
@Author ：WangJie
@Date   ：2020/11/26  21:24
@Desc   ：
"""
import json
import os
from tkinter import *
from urllib.request import urlretrieve
import jsonpath
import requests

# 功能
def get_music_name():
    '''
    搜索歌曲
    :return:
    '''

    name = entry.get()
    platfrom = var.get()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',                   # 判断请求同步异步
    }
    data = {
        'input': name,
        'filter': 'name',
        'type': platfrom,
        'page': 1,
    }
    url = "https://music.liuzhijin.cn/"
    response = requests.post(url, data=data, headers=headers)
    json_obj = response.json()
    print(type(json_obj))
    title = jsonpath.jsonpath(json_obj, '$..title')[0]
    author = jsonpath.jsonpath(json_obj, '$..author')[0]
    url = jsonpath.jsonpath(json_obj, '$..url')[0]
    print(author, title, url)
    # 下载
    song_down(url, title)

def song_down(url, title):
    os.makedirs("搜索下载的音乐", exist_ok=True)
    path = "./搜索下载的音乐/{}.mp3".format(title)
    text.insert(END, '歌曲：{},正在下载....'.format(title))
    # 文本框滑动
    text.see(END)
    # 更新
    text.update()
    # 下载
    urlretrieve(url, path)
    text.insert(END, "下载完毕：{},请试听".format(title))
    # 文本框滑动
    text.see(END)
    # 更新
    text.update()

# 界面
# 1.创建画布
root = Tk()

# 2.标题
root.title("音乐下载器")

# 3.设置大小
root.geometry('560x450+400+200')

# 4.创建标签组件
label = Label(root, text='请输入下载歌曲名称： ', font=("华文行楷", 20))
# 定位标签布局在画面上
label.grid()

# 6.创建输入框组件
entry = Entry(root, font=("隶书", 20))
entry.grid(row=0, column=1)

# 7.单选按钮组件
var = StringVar()
r1 = Radiobutton(root, text="网易云音乐", variable=var, value="netease")
r1.grid(row=1, column=0)
r2 = Radiobutton(root, text="QQ音乐", variable=var, value="qq")
r2.grid(row=1, column=1)

# 8.列表框组件创建
text = Listbox(root, font=("隶书", 16), width=50, height=15)
text.grid(row=2, columnspan=2)

# 9.下载按钮
button1 = Button(root, text='开始下载', font=("隶书", 15), command=get_music_name)
button1.grid(row=3, column=0)
button2 = Button(root, text='退出程序', font=("隶书", 15), command=root.quit)
button2.grid(row=3, column=1)

# 显示界面
root.mainloop()
