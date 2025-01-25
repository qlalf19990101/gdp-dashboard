import streamlit as st

# Streamlit 앱 제목
st.title("비약 이익 계산기")
st.write("원하는 비약을 선택하고 재료 가격을 입력하세요. 계산 결과가 아래에 표시됩니다!")

# 숫자 단위 변경 함수
def format_money(value):
    if value >= 10000:  # 1억 메소 이상
        return f"{value / 10000:.2f}억 메소"
    else:
        return f"{value:.0f}만 메소"

# 사용자에게 비약 선택 요청
option = st.selectbox(
    "계산하려는 비약을 선택하세요:",
    ("소형 재물 획득의 비약", "고급 보스킬러의 비약", "고농축 소형 경험 획득의 비약")
)

# 사용자 입력과 계산
if option == "소형 재물 획득의 비약":
    st.header("소형 재물 획득의 비약 계산")

    seed = st.number_input("쥬니퍼베리 씨앗의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    dol = st.number_input("현자의 돌의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    dol2 = st.number_input("최상급 아이템 결정의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    potion = st.number_input("소형 재물 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)

    if st.button("계산"):
        money_per_fatigue = potion * 6 - (seed * 30 + dol + dol2 * 2)
        total_money = money_per_fatigue * 100
        st.success(f"피로도 5당 이익: {format_money(money_per_fatigue)}")
        st.success(f"피로도 500 소진 시 총 이익: {format_money(total_money)}")

elif option == "고급 보스킬러의 비약":
    st.header("고급 보스킬러의 비약 계산")

    boss_potion = st.number_input("고급 보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    boss_base = st.number_input("보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    spell_essence = st.number_input("상급 주문의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)

    if st.button("계산"):
        boss_material_cost = boss_base + hisop * 60 + twilight_essence + spell_essence
        profit_per_10_fatigue = boss_potion * 2 - boss_material_cost
        total_boss_profit = profit_per_10_fatigue * 50
        st.success(f"피로도 10당 이익: {format_money(profit_per_10_fatigue)}")
        st.success(f"피로도 500 소진 시 총 이익: {format_money(total_boss_profit)}")

elif option == "고농축 소형 경험 획득의 비약":
    st.header("고농축 소형 경험 획득의 비약 계산")

    recipe = st.number_input("고농축 레시피 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    small_exp = st.number_input("소형 경험 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)
    mana_crystal = st.number_input("마력결정 1개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1)

    if st.button("계산"):
        total_material_cost = recipe + small_exp * 4 + hisop * 60 + twilight_essence * 2 + mana_crystal * 1000
        profit_per_5_fatigue = (small_exp * 4) - total_material_cost
        total_exp_profit = profit_per_5_fatigue * 100
        st.success(f"피로도 5당 이익: {format_money(profit_per_5_fatigue)}")
        st.success(f"피로도 500 소진 시 총 이익: {format_money(total_exp_profit)}")
