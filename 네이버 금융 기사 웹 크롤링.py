#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import re

import requests ##http요청을 보내는 모듈

import datetime
get_ipython().run_line_magic('matplotlib', 'inline')
##도표와 같은 그림, 소리, 애니메이션 과 같은 결과물들을 Rich output 이라 하고 이를 바로 이 브라우저에서 보이도록 함.

import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse
from tqdm import *
from urllib.request import urlopen


# In[3]:


base_url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS3D&section_id=101&section_id2=258&section_id3=402&date=20191129'
sec_url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS3D&section_id=101&section_id2=258&section_id3=402&date=20191202'
trd_url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS3D&section_id=101&section_id2=258&section_id3=402&date=20191203'
print(base_url)


# In[4]:


res = requests.get(base_url) ##base_url로 http요청 보내는 명령 변수로 저장
res.encoding='euc-kr' ##문자 인코딩 방식 설정


# In[5]:


res.status_code ##200은 정상적으로 정보를 가져왔음을 의미


# In[6]:


soup = BeautifulSoup(res.text, 'html.parser') ##html 태그 가져오는 도구
soup.encoding = 'euc-kr' ##네이버 금융은 인코딩 방식 영문으로 되어있음.


# In[7]:


output_raw = soup.find(name='ul', attrs ={'class':'realtimeNewsList'}) ##div에서 detailscript 부분
output_subject1 = output_raw.find_all(name='dt', attrs={'class':'articleSubject'})
output_subject2 = output_raw.find_all(name='dd', attrs={'class':'articleSubject'})


# In[8]:


lst = []
##페이지 넘어가게 하는 for문
for i in tqdm(range(1, 15)):
    page = '&page=' + str(i)
    url_page = base_url + page
    
    with urllib.request.urlopen(url_page) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
    
    
    for el in soup.find_all('dt', {'class' : 'articleSubject'}):
        lst.append(el.getText().strip().replace('\n',''))

    for el in soup.find_all('dd', {'class' : 'articleSubject'}):
        lst.append(el.getText().strip().replace('\n',''))
        

##긁어온 자료 리스트화

for i in tqdm(range(1, 10)):
    page = '&page=' + str(i)
    url_page = sec_url + page
    
    with urllib.request.urlopen(url_page) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    
    for el in soup.find_all('dt', {'class' : 'articleSubject'}):
        lst.append(el.getText().strip().replace('\n',''))

    for el in soup.find_all('dd', {'class' : 'articleSubject'}):
        lst.append(el.getText().strip().replace('\n',''))
        

for i in tqdm(range(1, 10)):
    page = '&page=' + str(i)
    url_page = trd_url + page
    
    with urllib.request.urlopen(url_page) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    
    for el in soup.find_all('dt', {'class' : 'articleSubject'}):
        lst.append(el.getText().strip().replace('\n',''))

    for el in soup.find_all('dd', {'class' : 'articleSubject'}):
        lst.append(el.getText().strip().replace('\n',''))
        

    
lst


# In[ ]:


get_ipython().system('pip install --upgrade pip')
get_ipython().system('pip install JPype1-0.6.3-cp37-cp37m-win_amd64.whl')


# In[11]:


get_ipython().system('pip install konlpy')


# In[8]:


df.to_csv('Article_titles.csv', index=False)


# In[9]:


titles = pd.read_csv('Article_titles.csv')
import konlpy


# In[10]:


from konlpy.tag import *
hannanum = Hannanum()
okt = Okt()


# In[11]:


from collections import Counter
from wordcloud import WordCloud
from nltk import tokenize
import nltk as nltk


# In[36]:


wc = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color='white', width=800, height=600).generate(' '.join(lst))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[45]:



def make_wordcloud(word_count):
 
    sentences_tag = []
    #형태소 분석하여 리스트에 넣기
    for sentence in lst:
        morph = okt.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-' * 30)
 
    print(sentences_tag)
    print('\n' * 3)
 
    noun_adj_list = []
    #명사와 형용사만 구분하여 이스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)
 
    #형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    print(tags)
 
    #wordCloud생성
    #한글꺠지는 문제 해결하기위해 font_path 지정
    wc = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color='white', width=800, height=600).generate(' '.join( noun_adj_list))
    print(dict(tags))
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
 


# In[49]:


make_wordcloud(50)


# In[ ]:


##삼성, 증권, 하나, 바이오가 눈에 띔

