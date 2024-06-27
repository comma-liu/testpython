from time import time
from threading import Thread
from bs4 import BeautifulSoup as bs
import requests
import openpyxl
from openpyxl import load_workbook

def main():
    # 通过requests模块的get函数获取网络资源
    url = "https://ssr1.scrape.center/"
    resp = requests.get(url)
    bs_resp = bs(resp.content, features='html.parser')
    resdict = {}
    
    testbs2 = bs_resp.find_all(attrs={"class":"categories"})
    testbs4 = bs_resp.find_all(attrs={"class":"score m-t-md m-b-n-sm"})
    for i in range(0,10):
            testbs1 = bs_resp.find_all(attrs={"href": f"/detail/{i+1}"})
            resdict[i] = [testbs1[1].h2.text]
            #print(testbs1[1].h2.text) 片名
            for j in testbs2[i].find_all("span"):            
    #           print(j.text);#种类
                resdict[i].append(j.text)
            resdict[i].append(testbs4[i].text)
            #print(testbs4[i].text)#评分   
            
    #class="m-v-sm info"信息
    testbs3 = bs_resp.find_all(attrs={"class":"m-v-sm info"}) 
    for i in range(0,20,2):
        for m in testbs3[i].find_all("span"):
    #        print(m.text)#地区
            mstr += m.text
        resdict[i].append(mstr)
        for n in testbs3[i+1].find_all("span"):
    #        print(n.text)#时间
        resdict[i].append(n.text)
    #    print("======")
    print(resdict)
    

        
    
        
"""     write_wb = openpyxl.Workbook()
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
    for row in sheet.rows:
        # 行信息
        title_1 = row[0].value
        title_2 = row[1].value
        title_3 = row[2].value
        title_4 = row[3].value
        title_5 = row[4].value
        title_6 = row[5].value
        excel_row = [
            title_1,
            title_2,
            title_3,
            title_4,
            title_5,
            title_6
        ]
        # 写入Excel中
        write_sheet.append(excel_row)
    # 生成excel文件
    write_wb.save('new_test.xlsx')
    print('写入excel完成！') """
    

if __name__ == '__main__':
    main()
