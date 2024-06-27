from time import time
from threading import Thread
from bs4 import BeautifulSoup as bs
import requests
import openpyxl
from openpyxl import load_workbook


def to_xlsx(filename, page):
    resdict = get_html(f"https://ssr1.scrape.center/page/{page}")
    write_wb = openpyxl.Workbook()
    write_sheet = write_wb.active
    print('开始写入excel')
    # 表头信息
    cxcel_title = [
        '片名',
        '种类',
        '地区',
        '时间',
        '评分',
    ]
    # 表头写入Excel中
    write_sheet.append(cxcel_title)
    # 循环写入旧Excel数据
    for row in resdict:
        # 行信息
        title_1 = resdict[row][0]
        title_2 = resdict[row][1]
        title_3 = resdict[row][2]
        title_4 = resdict[row][3]
        title_5 = resdict[row][4]
        excel_row = [
            title_1,
            title_2,
            title_3,
            title_4,
            title_5,
        ]
        # 写入Excel中
        write_sheet.append(excel_row)
    # 生成excel文件

    write_wb.save(filename)
    print('写入excel完成！') 


def get_html(url):
    # url = "https://ssr1.scrape.center/"
    resp = requests.get(url)
    bs_resp = bs(resp.content, features='html.parser')
    resdict = {}
    movie_title = []
    movie_caro = []
    movie_score = []
    movie_area = []
    movie_time = []
    
    testbs2 = bs_resp.find_all(attrs={"class":"categories"})
    testbs4 = bs_resp.find_all(attrs={"class":"score m-t-md m-b-n-sm"})
    for i in range(0,10):
            testbs1 = bs_resp.find_all(attrs={"href": f"/detail/{i+1}"})
            movie_title.append(testbs1[1].h2.text)
            caro = ' '
            for j in testbs2[i].find_all("span"):            
                caro += j.text
                caro += ' '
            movie_caro.append(caro)
            movie_score.append(float(testbs4[i].text))         

    testbs3 = bs_resp.find_all(attrs={"class":"m-v-sm info"}) 
    for i in range(0,20,2):
        area = ' '
        time = ' '
        for m in testbs3[i].find_all("span"):
            area += m.text
            area += ' '
        movie_area.append(area)
        for n in testbs3[i+1].find_all("span"):

             time += n.text
             time += ' '
        movie_time.append(time)
    for i in range(0,10):    
        resdict[i] = (movie_title[i],movie_caro[i],movie_area[i],movie_time[i],movie_score[i])

    return resdict

def main():
    #to_xlsx('第一页.xlsx',1)  
    #to_xlsx('第二页.xlsx',2)  
    resp = requests.get("https://ssr1.scrape.center/page/2")
    bs_resp = bs(resp.content, features='html.parser')
    print(bs_resp)

if __name__ == '__main__':
    main()
