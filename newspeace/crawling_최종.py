import warnings
warnings.filterwarnings('ignore')
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import db_info
db = db_info.DATABASES['default']

# 기사를 크롤링하는 함수
def crawling(category, start_time):
    items = []
    i = 1
    while i >= 1:
    # while 3 > i:  # test용 반복 (반복 횟수를 줄였음)
        url = f'https://news.daum.net/breakingnews/{category}?page={i+1}'   # i번째 페이지

        response = requests.get(url)  
        dom = BeautifulSoup(response.text, 'html.parser')
        elements = dom.select('#mArticle > div.box_etc > ul > li')
        stop_check = False  # 크롤링 중단 여부 체크

        for j, element in enumerate(elements):
            link = element.select_one('.cont_thumb > .tit_thumb > .link_txt').get('href')
            time = element.select_one('.cont_thumb > .tit_thumb > .info_news > .info_time').text
            # 기준 시간(start_time) 이후에 작성된 기사인 경우
            if time >= start_time:
                    items.append({
                    'category': category,
                    'title': element.select_one('.cont_thumb > .tit_thumb > .link_txt').text,
                    'link': link,
                    'img': detail(link)[1],
                    'detail': detail(link)[0],
                    'create_dt' : datetime.now()
                    })
            # 기준 시간(start_time) 이전에 작성된 기사인 경우
            else:
                stop_check = True
                break
        if stop_check:
            break
        i += 1
        
    df = pd.DataFrame(items)

    return df



# 해당 링크에 들어가서 기사 본문 가져오는 함수
def detail(url):
    response = requests.get(url)
    dom = BeautifulSoup(response.text, 'html.parser')
    elements = dom.select('#mArticle > div.news_view.fs_type1 > div.article_view > section')[0]
    element = elements.find_all(attrs={'dmcf-ptype':'general'})
  
    detail = ''
    for i in element:
        detail += i.text + ' '

    try:
        img = elements.select_one('figure > p > img').get('src')
    except:
        try:
            img = elements.find('iframe').get('poster')
        except:
            img = None

    return detail, img



category_list = ['society', 'politics', 'economic', 'foreign', 'culture', 'entertain', 'sports', 'digital']
one_hour_ago =  datetime.now() - timedelta(hours=1)
one_hour_ago = one_hour_ago.strftime("%H:%M")

result_df = pd.DataFrame()
for category in category_list:
    result_df = pd.concat([result_df, crawling(category, one_hour_ago)])



result_df_1 = result_df.reset_index(drop=True)
result_df_2 = result_df_1[['category', 'title', 'detail', 'link', 'img', 'create_dt']]

# category 필드 한글 변경
category_map = {'society' : '사회', 'politics' : '정치', 'economic' : '경제', 'foreign' : '외국',
                'culture' : '문화', 'entertain' : '여가', 'sports' : '스포츠', 'digital' : '전자'}
result_df_2.category = result_df_2.category.map(category_map)

# MYSQL 연결
password = db['PASSWORD']
con = create_engine(f"mysql+pymysql://admin:{password}@joon-sql-db-1.cvtb5zj20jzi.ap-northeast-2.rds.amazonaws.com:3306/joon_db")

# db에 데이터 저장
result_df_2.to_sql('news_article', con, if_exists='append', index=False)


# db에 데이터 삭제

# 현재 시간으로부터 12시간-> 2일 전의 시간 계산
current_datetime = datetime.now()
time_to_delete = current_datetime - timedelta(days=2)
print(current_datetime)


# connection = con.connect()
with con.connect() as connection:
    query = text("DELETE FROM news_article WHERE CREATE_DT < :time_to_delete")
    result = connection.execute(query, {"time_to_delete" : time_to_delete})
    connection.commit()
    
# 실험 결과, 서버와 crontab active 와는 연관이 따로 없어보임. -> 따로 켜주고 끄고 해야될듯.
# mysql db에 잘 들어가는거 서버에서 확인함.


# conn = pymysql.connect(
#    host='joon-sql-db-1.cvtb5zj20jzi.ap-northeast-2.rds.amazonaws.com',
#    user='admin',
#    password='admin12345', 
#    database= 'joon_db', 
#    charset='utf8')

    
# # 데이터프레임을 json 파일로 저장하기
# result_df.to_json('crawling_result.json', orient='records', force_ascii=False, indent=4)
# # 데이터프레임을 csv 파일로 저장하기
# result_df.to_csv('crawling_result.csv', index=False)