import streamlit as st

# Streamlit 앱 제목 변경
st.title("연금술 제작 이익 계산기")
st.write("원하는 비약을 선택하고 재료 가격을 입력하세요. 계산 결과가 아래에 표시됩니다!")

# 숫자 단위 변경 함수
def format_money(value):
    if value >= 10000:  # 1억 메소 이상
        return f"{value / 10000:.2f}억 메소"
    else:
        return f"{value:.0f}만 메소"

# 세션 상태 초기화 처리 (초기화되면 기존에 입력한 값 유지)
def get_input(key, default_value=0.0):
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]

def set_input(key, value):
    st.session_state[key] = value

# 사용자에게 비약 선택 요청
option = st.selectbox(
    "계산하려는 비약을 선택하세요:",
    ("소형 재물 획득의 비약", "고급 보스킬러의 비약", "고농축 소형 경험 획득의 비약")
)

# 소형 재물 획득의 비약
if option == "소형 재물 획득의 비약":
    st.header("소형 재물 획득의 비약 계산")

    seed = get_input("seed", 0.0)
    dol = get_input("dol", 0.0)
    dol2 = get_input("dol2", 0.0)
    potion = get_input("potion", 0.0)

    seed = st.number_input("쥬니퍼베리 씨앗의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=seed)
    dol = st.number_input("현자의 돌의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=dol)
    dol2 = st.number_input("최상급 아이템 결정의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=dol2)
    potion = st.number_input("소형 재물 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=potion)

    if st.button("계산"):
        set_input("seed", seed)
        set_input("dol", dol)
        set_input("dol2", dol2)
        set_input("potion", potion)

        money_per_fatigue = potion * 6 - (seed * 30 + dol + dol2 * 2)
        total_money = money_per_fatigue * 100
        st.success(f"피로도 5당 이익: {format_money(money_per_fatigue)}")
        st.success(f"피로도 500 소진 시 총 이익: {format_money(total_money)}")

# 고급 보스킬러의 비약
elif option == "고급 보스킬러의 비약":
    st.header("고급 보스킬러의 비약 계산")

    boss_potion = get_input("boss_potion", 0.0)
    boss_base = get_input("boss_base", 0.0)
    hisop = get_input("hisop", 0.0)
    twilight_essence = get_input("twilight_essence", 0.0)
    spell_essence = get_input("spell_essence", 0.0)

    boss_potion = st.number_input("고급 보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=boss_potion)
    boss_base = st.number_input("보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=boss_base)
    hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=hisop)
    twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=twilight_essence)
    spell_essence = st.number_input("상급 주문의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=spell_essence)

    if st.button("계산"):
        set_input("boss_potion", boss_potion)
        set_input("boss_base", boss_base)
        set_input("hisop", hisop)
        set_input("twilight_essence", twilight_essence)
        set_input("spell_essence", spell_essence)

        boss_material_cost = boss_base + hisop * 60 + twilight_essence + spell_essence
        profit_per_10_fatigue = boss_potion * 2 - boss_material_cost
        total_boss_profit = profit_per_10_fatigue * 50
        st.success(f"피로도 10당 이익: {format_money(profit_per_10_fatigue)}")
        st.success(f"피로도 500 소진 시 총 이익: {format_money(total_boss_profit)}")

# 고농축 소형 경험 획득의 비약
elif option == "고농축 소형 경험 획득의 비약":
    st.header("고농축 소형 경험 획득의 비약 계산")

    recipe = get_input("recipe", 0.0)
    small_exp = get_input("small_exp", 0.0)
    hisop = get_input("hisop", 0.0)
    twilight_essence = get_input("twilight_essence", 0.0)
    mana_crystal = get_input("mana_crystal", 0.0)

    recipe = st.number_input("고농축 레시피 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=recipe)
    small_exp = st.number_input("소형 경험 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=small_exp)
    hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=hisop)
    twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=twilight_essence)
    mana_crystal = st.number_input("마력결정 1개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=mana_crystal)

    if st.button("계산"):
        set_input("recipe", recipe)
        set_input("small_exp", small_exp)
        set_input("hisop", hisop)
        set_input("twilight_essence", twilight_essence)
        set_input("mana_crystal", mana_crystal)

        total_material_cost = recipe + small_exp * 4 + hisop * 60 + twilight_essence * 2 + mana_crystal * 1000
        profit_per_5_fatigue = (small_exp * 4) - total_material_cost
        total_exp_profit = profit_per_5_fatigue * 100
        st.success(f"피로도 5당 이익: {format_money(profit_per_5_fatigue)}")
        st.success(f"피로도 500 소진 시 총 이익: {format_money(total_exp_profit)}")
