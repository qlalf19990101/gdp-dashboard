# -*- coding: utf-8 -*-
"""test2_1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z33IX_juXbATSq5r9hLB3BX5QqegwPB6
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from streamlit_elements import elements, mui, html


def get_all_news():
    all_news_df = pd.DataFrame()
    pressDt = {'MBC': '214', '연합뉴스': '422', 'KBS': '056', 'JTBC': '437', 
               'MBN': '057', 'SBS': '055', 'SBS_Biz': '374', 'TV조선': '448', 
               'YTN': '052', '뉴스1': '421', '뉴시스': '003', '연합뉴스TV': '422', 
               '채널A': '449', '한국경제TV': '215'} 
    for press, code in pressDt.items():
        url = f'https://media.naver.com/press/{code}/ranking?/type=popular'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        data = []
        for item in soup.select('li.as_thumb'):
            rank = item.select_one('em.list_ranking_num').text
            title = item.select_one('strong.list_title').text
            link = item.select_one('a._es_pc_link')['href']
            views_element = item.select_one('span.list_view')
            views = views_element.text if views_element else ""  # 조회수 정보가 없으면 빈 문자열 사용
            data.append({'순위': int(rank), '제목': title, '조회수': views, '언론사': press, '링크': link})

        df = pd.DataFrame(data)
        df['조회수'] = df['조회수'].apply(lambda x: int(x.replace('\n조회수\n', '').replace('\n', '').replace(',', '').strip()) if x != "" else 0)
        all_news_df = pd.concat([all_news_df, df])

    return all_news_df

# 페이지네이션 설정 (st_aggrid 사용하지 않음)
def paginate_dataframe(df, page_size=20):
    num_rows = len(df)
    if num_rows == 0:
        st.write("데이터가 없습니다.")
        return
    
    num_pages = (num_rows + page_size - 1) // page_size
    page_number = st.slider("페이지 선택", 1, num_pages) - 1

    start_index = page_number * page_size
    end_index = (page_number + 1) * page_size
    st.dataframe(df.iloc[start_index:end_index])

def sort_news(df_news):
    specific_press = st.radio('특정 언론사만 보겠습니까?', ('Y', 'N'))

    if specific_press == 'Y':
        selected_press = st.selectbox('보고싶은 언론사를 선택해주세요', 
                                      ("MBC", "JTBC", "KBS", "연합뉴스", 
                                       "MBN", "SBS", "SBS_Biz", "TV조선", 
                                       "YTN", "뉴스1", "뉴시스", "연합뉴스TV", 
                                       "채널A", "한국경제TV")) 
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

"""
if sorted_df is not None:
    # 링크를 클릭 가능하게 만드는 함수
    def make_clickable(val):
        return f'<a target="_blank" href="{val}">링크</a>'

    # 스타일 적용 및 인덱스 재설정
    df_styled = sorted_df.reset_index(drop=True).style.format({'링크': make_clickable})
    df_styled = df_styled.set_properties(**{'text-align': 'left'})
    df_styled = df_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    st.write(df_styled, unsafe_allow_html=True)  # Streamlit에 데이터프레임 표시

    # 링크를 버튼으로 변경
    for idx, (index, row) in enumerate(sorted_df.iterrows()):
        st.write(f"{row['순위']}. {row['제목']} ({row['언론사']}, 조회수: {row['조회수']})")
        if st.button("기사 보기", key=f"button_{idx}"):
"""

if sorted_df is not None:
    # 링크를 클릭 가능하게 만드는 함수
    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)

    # 스타일 적용 및 인덱스 재설정
    df_styled = sorted_df.reset_index(drop=True).style.format({'링크': make_clickable}) 
    df_styled = df_styled.set_properties(**{'text-align': 'left'})
    df_styled = df_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    
    # 페이지네이션 적용 (수동 구현)
    paginate_dataframe(sorted_df)
