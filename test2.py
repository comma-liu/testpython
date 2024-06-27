from time import time
from threading import Thread

import requests


class DownloadHanlder(Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        filename = self.url[self.url.rfind('/') + 1:]
        resp = requests.get(self.url)
        with open('/Users/Hao/Downloads/' + filename, 'wb') as f:
            f.write(resp.content)


def main():
    # 通过requests模块的get函数获取网络资源
    resp = requests.get(
        'http://api.tianapi.com/meinv/?key=772a81a51ae5c780251b1f98ea431b84&num=10')
    # 将服务器返回的JSON格式的数据解析为字典
    data_model = resp.json()
    #print(type(data_model))
    with open('test2.json', 'wb') as f:
        for i in data_model:
            f.write(f"{i}: {data_model[i]}\n".encode("utf-8"))
    try:
        for mm_dict in data_model['newslist']:
            url = mm_dict['picUrl']
        # 通过多线程的方式实现图片下载
        DownloadHanlder(url).start()
    except:
        return


if __name__ == '__main__':
    main()
