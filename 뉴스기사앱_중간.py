# -*- coding: utf-8 -*-
"""뉴스기사앱_중간

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eWmG1Wz2fUf_ufubf3dQX2W0zcKCzgbr
"""

# 필요한 함수들 먼저 import 하기

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 뉴스데이터 가져오고 필터링
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


def page1():
    st.title("뉴스 뷰어 - 필터 선택")
    
    # 세션 상태 초기화
    if 'specific_press' not in st.session_state:
        st.session_state['specific_press'] = 'N'
    if 'selected_press' not in st.session_state:
        st.session_state['selected_press'] = "MBC"
    if 'criteria' not in st.session_state:
        st.session_state['criteria'] = "조회수"

    st.session_state['specific_press'] = st.radio('특정 언론사만 보겠습니까?', ('Y', 'N'), key='press_radio')

    if st.session_state['specific_press'] == 'Y':
        st.session_state['selected_press'] = st.selectbox('보고싶은 언론사를 선택해주세요',
                                ("MBC", "JTBC", "KBS", "연합뉴스",
                                 "MBN", "SBS", "SBS_Biz", "TV조선",
                                 "YTN", "뉴스1", "뉴시스", "연합뉴스TV",
                                 "채널A", "한국경제TV"), key='press_select')

    st.session_state['criteria'] = st.selectbox('정렬할 기준을 선택해주세요', ("조회수", "언론사", "순위"), key='criteria_select')


def page2():
    st.title("뉴스 뷰어 - 결과")

    # 세션 상태에서 선택된 값 가져오기
    specific_press = st.session_state['specific_press']
    selected_press = st.session_state['selected_press']
    criteria = st.session_state['criteria']

    # 뉴스 데이터 필터링 및 정렬
    df_filtered = df_news.copy()
    if specific_press == 'Y':
        df_filtered = df_filtered[df_filtered['언론사'] == selected_press]
    if criteria == '조회수':
        df_filtered = df_filtered.sort_values(by='조회수', ascending=False)
    elif criteria == '언론사':
        df_filtered = df_filtered.sort_values(by=['언론사', '순위'])
    elif criteria == '순위':
        df_filtered = df_filtered.sort_values(by='순위')

    # 페이지네이션
    page_size = 20
    page_number = st.number_input("페이지 번호", min_value=1, step=1, value=1)
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    df_page = df_filtered.iloc[start_index:end_index]

    # 링크를 클릭 가능하게 만드는 함수
    def make_clickable(val):
        return f'<a target="_blank" href="{val}">링크</a>'

    # 스타일 적용 및 인덱스 재설정
    df_styled = df_page.reset_index(drop=True).style.format({'링크': make_clickable})
    df_styled = df_styled.set_properties(**{'text-align': 'left'})
    df_styled = df_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    st.write(df_styled, unsafe_allow_html=True)  # Streamlit에 데이터프레임 표시

    # 링크를 버튼처럼 보이도록 스타일링
    for idx, (index, row) in enumerate(df_page.iterrows()):
        st.write(f"{row['순위']}. {row['제목']} ({row['언론사']}, 조회수: {row['조회수']})")
        st.markdown(f'<a href="{row["링크"]}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">기사 보기</a>', unsafe_allow_html=True)


# 앱 실행 및 페이지 관리
if 'page' not in st.session_state:
    st.session_state['page'] = "필터 선택"

page = st.sidebar.radio("페이지 선택", ("필터 선택", "뉴스 보기"))
st.session_state['page'] = page

if st.session_state['page'] == "필터 선택":
    page1()
elif st.session_state['page'] == "뉴스 보기":
    page2()
