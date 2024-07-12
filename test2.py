# -*- coding: utf-8 -*-
"""test2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z33IX_juXbATSq5r9hLB3BX5QqegwPB6
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_all_news():
    all_news_df = pd.DataFrame()
    pressDt = {'MBC': '214', '연합뉴스': '422', 'KBS': '056', 'JTBC': '437'}
    for press, code in pressDt.items():
        url = f'https://media.naver.com/press/{code}/ranking?/type=popular'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        data = []
        for item in soup.select('li.as_thumb'):
            rank = item.select_one('em.list_ranking_num').text
            title = item.select_one('strong.list_title').text
            link = item.select_one('a._es_pc_link')['href']
            views = item.select_one('span.list_view').text
            data.append({'순위': int(rank), '제목': title, '조회수': views, '언론사': press, '링크': link})

        df = pd.DataFrame(data)
        df['조회수'] = df['조회수'].str.replace('\n조회수\n', '').str.replace('\n', '').str.replace(',', '').str.strip().astype(int)
        all_news_df = pd.concat([all_news_df, df])

    return all_news_df


def sort_news(df_news):
    specific_press = st.radio('특정 언론사만 보겠습니까?', ('Y', 'N'))

    if specific_press == 'Y':
        selected_press = st.selectbox('보고싶은 언론사를 선택해주세요', ("MBC", "JTBC", "KBS", "연합뉴스"))
        df_filtered = df_news[df_news['언론사'] == selected_press]
        if df_filtered.empty:
            st.write(f"{selected_press}에 대한 뉴스가 없습니다.")
            return
    else:
        df_filtered = df_news

    criteria = st.selectbox('정렬할 기준을 선택해주세요', ("조회수", "언론사", "순위"))

    if criteria == '조회수':
        sorted_df = df_filtered.sort_values(by='조회수', ascending=False)
    elif criteria == '언론사':
        sorted_df = df_filtered.sort_values(by=['언론사', '순위'])
    elif criteria == '순위':
        sorted_df = df_filtered.sort_values(by='순위')
    return sorted_df

# 뉴스 데이터 가져오기
df_news = get_all_news()


# Streamlit 앱 시작
st.title("뉴스 뷰어")  # 앱 제목 설정

# 정렬 기준 선택 (이미 sort_news 함수 안으로 이동)

# 데이터프레임 정렬 및 표시
sorted_df = sort_news(df_news.copy())  # sort_news 함수 호출하여 정렬
if sorted_df is not None:
    # 링크를 클릭 가능하게 만드는 함수
    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)

    # 스타일 적용 및 인덱스 재설정
    df_styled = sorted_df.reset_index(drop=True).style.format({'링크': make_clickable})
    df_styled = df_styled.set_properties(**{'text-align': 'left'})
    df_styled = df_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    st.write(df_styled, unsafe_allow_html=True)  # Streamlit에 데이터프레임 표시