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

# 세션 상태 초기화 처리
def get_input(key, default_value=0.0):
    if key not in st.session_state:
        st.session_state[key] = default_value
    return st.session_state[key]

def set_input(key, value):
    st.session_state[key] = value

# 전체 재료 입력 탭
st.header("모든 재료 입력")
input_method = st.radio("재료 입력 방식 선택", ["전체 재료 입력", "레시피별 재료 입력"])

if input_method == "전체 재료 입력":
    with st.expander("전체 재료 입력"):
        # 공통 재료를 한번에 입력할 수 있는 필드
        seed = get_input("seed", 0.0)
        dol = get_input("dol", 0.0)
        dol2 = get_input("dol2", 0.0)
        potion = get_input("potion", 0.0)
        boss_potion = get_input("boss_potion", 0.0)
        boss_base = get_input("boss_base", 0.0)
        hisop = get_input("hisop", 0.0)
        twilight_essence = get_input("twilight_essence", 0.0)
        spell_essence = get_input("spell_essence", 0.0)
        recipe = get_input("recipe", 0.0)
        small_exp = get_input("small_exp", 0.0)
        mana_crystal = get_input("mana_crystal", 0.0)
        high_small_exp = get_input("high_small_exp", 0.0)

        # 재료값 입력
        seed = st.number_input("쥬니퍼베리 씨앗의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=seed)
        dol = st.number_input("현자의 돌의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=dol)
        dol2 = st.number_input("최상급 아이템 결정의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=dol2)
        potion = st.number_input("소형 재물 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=potion)
        boss_potion = st.number_input("고급 보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=boss_potion)
        boss_base = st.number_input("보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=boss_base)
        hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=hisop)
        twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=twilight_essence)
        spell_essence = st.number_input("상급 주문의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=spell_essence)
        recipe = st.number_input("고농축 레시피 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=recipe)
        small_exp = st.number_input("소형 경험 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=small_exp)
        mana_crystal = st.number_input("마력결정 1개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=mana_crystal)
        high_small_exp = st.number_input("소형 고농축 경험 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=high_small_exp)

        # 값을 세션 상태에 저장
        if st.button("저장"):
            set_input("seed", seed)
            set_input("dol", dol)
            set_input("dol2", dol2)
            set_input("potion", potion)
            set_input("boss_potion", boss_potion)
            set_input("boss_base", boss_base)
            set_input("hisop", hisop)
            set_input("twilight_essence", twilight_essence)
            set_input("spell_essence", spell_essence)
            set_input("recipe", recipe)
            set_input("small_exp", small_exp)
            set_input("mana_crystal", mana_crystal)
            set_input("high_small_exp", high_small_exp)

            st.success("재료 값이 저장되었습니다!")

        # 재료 값을 기반으로 각각의 비약 이익 계산

        # 1. 소형 재물 획득의 비약 계산
        money_small_potion = potion * 6 - (seed * 30 + dol + dol2 * 2)
        total_small_potion = money_small_potion * 100

        # 2. 고급 보스킬러의 비약 계산
        money_boss_potion = boss_potion * 2 - (boss_base + hisop * 60 + twilight_essence + spell_essence)
        total_boss_potion = money_boss_potion * 50

        # 3. 고농축 소형 경험 획득의 비약 계산
        total_material_cost_high_exp = recipe + small_exp * 4 + hisop * 60 + twilight_essence * 2 + mana_crystal * 1000
        money_high_small_exp = (high_small_exp * 4) - total_material_cost_high_exp
        total_high_small_exp = money_high_small_exp * 100

        st.subheader("계산된 결과")

        # 결과 출력
        st.write(f"1. 소형 재물 획득의 비약")
        st.write(f"피로도 5당 이익: {format_money(money_small_potion)}")
        st.write(f"피로도 500 소진 시 총 이익: {format_money(total_small_potion)}")

        st.write(f"2. 고급 보스킬러의 비약")
        st.write(f"피로도 10당 이익: {format_money(money_boss_potion)}")
        st.write(f"피로도 500 소진 시 총 이익: {format_money(total_boss_potion)}")

        st.write(f"3. 고농축 소형 경험 획득의 비약")
        st.write(f"피로도 5당 이익: {format_money(money_high_small_exp)}")
        st.write(f"피로도 500 소진 시 총 이익: {format_money(total_high_small_exp)}")

elif input_method == "레시피별 재료 입력":
    # 레시피 선택
    recipe_choice = st.selectbox("레시피를 선택하세요", ["소형 재물 획득의 비약", "고급 보스킬러의 비약", "고농축 소형 경험 획득의 비약"])

    if recipe_choice == "소형 재물 획득의 비약":
        # 소형 재물 획득의 비약 입력
        seed = get_input("seed", 0.0)
        dol = get_input("dol", 0.0)
        dol2 = get_input("dol2", 0.0)
        potion = get_input("potion", 0.0)

        st.subheader("소형 재물 획득의 비약")
        potion = st.number_input("소형 재물 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=potion)
        seed = st.number_input("쥬니퍼베리 씨앗의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=seed)
        dol = st.number_input("현자의 돌의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=dol)
        dol2 = st.number_input("최상급 아이템 결정의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=dol2)

        if st.button("소형 재물 획득 비약 계산하기"):
            # 소형 재물 획득 비약 계산
            money_per_fatigue = potion * 6 - (seed * 30 + dol + dol2 * 2)
            total_money = money_per_fatigue * 100
            st.write(f"피로도 5당 이익: {format_money(money_per_fatigue)}")
            st.write(f"피로도 500 소진 시 총 이익: {format_money(total_money)}")

    elif recipe_choice == "고급 보스킬러의 비약":
        # 고급 보스킬러의 비약 입력
        boss_potion = get_input("boss_potion", 0.0)
        boss_base = get_input("boss_base", 0.0)
        hisop = get_input("hisop", 0.0)
        twilight_essence = get_input("twilight_essence", 0.0)
        spell_essence = get_input("spell_essence", 0.0)

        st.subheader("고급 보스킬러의 비약")
        boss_potion = st.number_input("고급 보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=boss_potion)
        boss_base = st.number_input("보스킬러의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=boss_base)
        hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=hisop)
        twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=twilight_essence)
        spell_essence = st.number_input("상급 주문의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=spell_essence)

        if st.button("고급 보스킬러의 비약 계산하기"):
            # 고급 보스킬러의 비약 계산
            money_per_fatigue = boss_potion * 2 - (boss_base + hisop * 60 + twilight_essence + spell_essence)
            total_money = money_per_fatigue * 50
            st.write(f"피로도 10당 이익: {format_money(money_per_fatigue)}")
            st.write(f"피로도 500 소진 시 총 이익: {format_money(total_money)}")

    elif recipe_choice == "고농축 소형 경험 획득의 비약":
        # 고농축 소형 경험 획득의 비약 입력
        recipe = get_input("recipe", 0.0)
        high_small_exp = get_input("high_small_exp", 0.0)
        small_exp = get_input("small_exp", 0.0)
        hisop = get_input("hisop", 0.0)
        twilight_essence = get_input("twilight_essence", 0.0)
        mana_crystal = get_input("mana_crystal", 0.0)

        st.subheader("고농축 소형 경험 획득의 비약")
        recipe = st.number_input("고농축 레시피 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=recipe)
        high_small_exp = st.number_input("소형 고농축 경험 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=high_small_exp)
        small_exp = st.number_input("소형 경험 획득의 비약 한 병의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=small_exp)
        hisop = st.number_input("히솝 꽃 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=hisop)
        twilight_essence = st.number_input("영롱한 황혼의 정수 한 개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=twilight_essence)
        mana_crystal = st.number_input("마력결정 1개의 가격 (단위: 만 메소)", min_value=0.0, step=0.1, value=mana_crystal)

        if st.button("고농축 소형 경험 획득의 비약 계산하기"):
            # 고농축 소형 경험 획득의 비약 계산
            total_material_cost = recipe + small_exp * 4 + hisop * 60 + twilight_essence * 2 + mana_crystal * 1000
            money_per_fatigue = high_small_exp * 4 - total_material_cost
            total_money = money_per_fatigue * 100
            st.write(f"피로도 5당 이익: {format_money(money_per_fatigue)}")
            st.write(f"피로도 500 소진 시 총 이익: {format_money(total_money)}")

# 이익 계산 결과 하단 출력
if input_method == "전체 재료 입력":
    st.subheader("전체 이익 계산 결과")
    st.write(f"소형 재물 획득의 비약: {format_money(total_small_potion)}")
    st.write(f"고급 보스킬러의 비약: {format_money(total_boss_potion)}")
    st.write(f"고농축 소형 경험 획득의 비약: {format_money(total_high_small_exp)}")
