from time import time
from bs4 import BeautifulSoup as bs
import requests
import openpyxl
from multiprocessing.dummy import Pool
import time

def to_xlsx(page):
    resdict = get_html(page)
    write_wb = openpyxl.Workbook()
    write_sheet = write_wb.active
    # 表头信息
    cxcel_title = [
        '片名',
        '种类',
        '地区/时长',
        '上映日期',
        '评分',
        '导演',
        '剧情简介',
        '演员',
        '电影海报'
    ]
    # 表头写入Excel中
    write_sheet.append(cxcel_title)
    
    # 循环写入旧Excel数据
    for row in resdict:
        # 行信息
        title_0 = resdict[row][0]
        title_1 = resdict[row][1]
        title_2 = resdict[row][2]
        title_3 = resdict[row][3]
        title_4 = resdict[row][4]        
        title_5 = resdict[row][5]
        title_6 = resdict[row][6]
        title_7 = resdict[row][7]
        title_8 = '见testjpg文件夹'
        excel_row = [
            title_0,
            title_1,
            title_2,
            title_3,
            title_4,
            title_5,
            title_6,
            title_7,
            title_8
        ]
        # 写入Excel中
        write_sheet.append(excel_row)
    write_wb.save(f'./testxlsx/第{page}页.xlsx')
    print(f'第{page}页写入xlsx文件完成！') 

def get_detail(link):
    bs_ = bs(requests.get(link).content, 'html.parser')
    dire = bs_.find(class_ = 'directors el-row').p.text 
    show = bs_.find(class_ = 'drama').p.text
    actor = ' '
    bs_list = bs_.find_all(class_ = 'actor el-col el-col-4')
    acto_len = 6 if bs_list.__len__()>=6 else bs_list.__len__()
    for j in range(0,acto_len):
        acto = bs_list[j].p.text
        actor += acto
        actor += ', '
    return dire, show, actor

def get_html(page):
    # url = "https://ssr1.scrape.center/"
    url = f"https://ssr1.scrape.center/page/{page}"
    resp = requests.get(url)
    bs_resp = bs(resp.content, features='html.parser')
    
    resdict = {}
    movie_title, movie_caro, movie_score, movie_area = [], [], [], []
    movie_time, movie_dire, movie_show, movie_acto = [], [], [], []
    
    testbs2 = bs_resp.find_all(class_ = "categories")
    testbs4 = bs_resp.find_all(class_ = "score m-t-md m-b-n-sm")
    testbs1 = bs_resp.find_all(class_ =  "m-b-sm")
    testbs5 = bs_resp.find_all(class_ =  "cover")
    testbs3 = bs_resp.find_all(class_ = "m-v-sm info") 
    
    for i in range(0,10):
            movie_title.append(testbs1[i].text)#标题

            #================导演、剧情简介、前六名演员
            movie_link = f'{"/".join(url.split(f"/")[:-2])}/detail/{ page * 10 - 10 + i + 1 }'
            dire, show, actor = get_detail(movie_link)
            movie_dire.append(dire)
            movie_show.append(show.replace(' ',''))
            movie_acto.append(actor[:-2])
            #================导演、剧情简介、前六名演员
            
            #===============封面
            cover_link = testbs5[i]['src']
            cover_content = requests.get(cover_link).content
            with open(f'./testjpg/{movie_title[i]}.jpg', 'wb') as f:
                f.write(cover_content)
            #===============封面    
               
            movie_caro.append(('/').join(testbs2[i].text.strip().split('\n\n')))#种类
            
            movie_score.append(float(testbs4[i].text))#评分  
            
            movie_area.append(testbs3[i*2].text)#地区/时长
            movie_time.append(testbs3[i*2+1].text)#上映日期        
    
    for i in range(0,10):    
        resdict[i] = (movie_title[i],movie_caro[i],movie_area[i],movie_time[i],
                      movie_score[i],movie_dire[i],movie_show[i],movie_acto[i])

    return resdict

def main():
    t_ = time.time()
    pool = Pool(10)
    pool.map(to_xlsx,[ _ for _ in range(1,11)])
    pool.close()
    pool.join()
    print(time.time() - t_)
if __name__ == '__main__':
    main()
