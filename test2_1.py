{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMuWgm48oziN5l+gNZxzJ/Y"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "51rMG4d7KmXr"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "\n",
        "def get_all_news():\n",
        "    all_news_df = pd.DataFrame()\n",
        "    pressDt = {'MBC': '214', '연합뉴스': '422', 'KBS': '056', 'JTBC': '437'}\n",
        "    for press, code in pressDt.items():\n",
        "        url = f'https://media.naver.com/press/{code}/ranking?/type=popular'\n",
        "\n",
        "        response = requests.get(url)\n",
        "        soup = BeautifulSoup(response.text, 'html.parser')\n",
        "\n",
        "        data = []\n",
        "        for item in soup.select('li.as_thumb'):\n",
        "            rank = item.select_one('em.list_ranking_num').text\n",
        "            title = item.select_one('strong.list_title').text\n",
        "            link = item.select_one('a._es_pc_link')['href']\n",
        "            views = item.select_one('span.list_view').text\n",
        "            data.append({'순위': int(rank), '제목': title, '조회수': views, '언론사': press, '링크': link})\n",
        "\n",
        "        df = pd.DataFrame(data)\n",
        "        df['조회수'] = df['조회수'].str.replace('\\n조회수\\n', '').str.replace('\\n', '').str.replace(',', '').str.strip().astype(int)\n",
        "        all_news_df = pd.concat([all_news_df, df])\n",
        "\n",
        "    return all_news_df\n",
        "\n",
        "\n",
        "def sort_news(df_news):\n",
        "    specific_press = st.radio('특정 언론사만 보겠습니까?', ('Y', 'N'))\n",
        "\n",
        "    if specific_press == 'Y':\n",
        "        selected_press = st.selectbox('보고싶은 언론사를 선택해주세요', (\"MBC\", \"JTBC\", \"KBS\", \"연합뉴스\"))\n",
        "        df_filtered = df_news[df_news['언론사'] == selected_press]\n",
        "        if df_filtered.empty:\n",
        "            st.write(f\"{selected_press}에 대한 뉴스가 없습니다.\")\n",
        "            return\n",
        "    else:\n",
        "        df_filtered = df_news\n",
        "\n",
        "    criteria = st.selectbox('정렬할 기준을 선택해주세요', (\"조회수\", \"언론사\", \"순위\"))\n",
        "\n",
        "    if criteria == '조회수':\n",
        "        sorted_df = df_filtered.sort_values(by='조회수', ascending=False)\n",
        "    elif criteria == '언론사':\n",
        "        sorted_df = df_filtered.sort_values(by=['언론사', '순위'])\n",
        "    elif criteria == '순위':\n",
        "        sorted_df = df_filtered.sort_values(by='순위')\n",
        "    return sorted_df\n",
        "\n",
        "# 뉴스 데이터 가져오기\n",
        "df_news = get_all_news()\n",
        "\n",
        "\n",
        "# Streamlit 앱 시작\n",
        "st.title(\"뉴스 뷰어\")  # 앱 제목 설정\n",
        "\n",
        "# 정렬 기준 선택 (이미 sort_news 함수 안으로 이동)\n",
        "\n",
        "# 데이터프레임 정렬 및 표시\n",
        "sorted_df = sort_news(df_news.copy())  # sort_news 함수 호출하여 정렬\n",
        "if sorted_df is not None:\n",
        "    # 링크를 클릭 가능하게 만드는 함수\n",
        "    def make_clickable(val):\n",
        "        return f'<a target=\"_blank\" href=\"{val}\">링크</a>'\n",
        "\n",
        "    # 스타일 적용 및 인덱스 재설정\n",
        "    df_styled = sorted_df.reset_index(drop=True).style.format({'링크': make_clickable})\n",
        "    df_styled = df_styled.set_properties(**{'text-align': 'left'})\n",
        "    df_styled = df_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])\n",
        "    st.write(df_styled, unsafe_allow_html=True)  # Streamlit에 데이터프레임 표시"
      ]
    }
  ]
}