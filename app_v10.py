
import streamlit as st

# ✅ 모험가별 모래양 데이터 (Lv -> 모래양)
모래양_DB = {
    "용소녀": {"100": 55125},
    "피기": {"90": 16990, "60": 9555},
    "판다": {"60": 9555, "90": 15900},
    "곰": {"60": 12740},
    "오공": {"2": 0},
    "가가린": {"2": 0},
    "레오나르도": {"60": 15925},
    "라파엘": {"60": 15925}
}

# ✅ 공생합 조합 데이터
공생합_조합 = [
    {
        "조합명": "A조합",
        "모험가들": {"피기": 60, "판다": 60, "곰": 60, "오공": 0, "가가린": 0, "레오나르도": 60, "라파엘": 60},
        "모래소모량": 69070,
        "공생합": 210
    },
    {
        "조합명": "B조합",
        "모험가들": {"피기": 90, "판다": 60, "곰": 60, "오공": 0, "가가린": 0, "레오나르도": 60, "라파엘": 60},
        "모래소모량": 76510,
        "공생합": 195
    },
    {
        "조합명": "C조합",
        "모험가들": {"피기": 60, "판다": 60, "곰": 60, "오공": 0, "가가린": 0, "레오나르도": 0, "라파엘": 0},
        "모래소모량": 31850,
        "공생합": 175
    }
]

모험가_목록 = ['피기', '판다', '곰', '오공', '가가린', '레오나르도', '라파엘']

st.title("🌾 모험가 모래양 계산기")
st.markdown("""
- 모험가를 선택하고 레벨을 입력하면 추천 모험가 Lv이 계산됩니다.
- 용소녀는 Lv 100 고정입니다.
""")

사용자_Lv = {}
총모래양 = 0

st.subheader("1️⃣ 모험가 선택 및 레벨 입력")
cols = st.columns(4)
for i, 모험가 in enumerate(모험가_목록):
    with cols[i % 4]:
        사용 = st.checkbox(f"{모험가} 사용", key=f"chk_{모험가}")
        if 사용:
            lv = st.number_input(f"{모험가} Lv", min_value=2, max_value=100, step=1, key=f"lv_{모험가}")
        else:
            lv = 0
        사용자_Lv[모험가] = lv

제출 = st.button("모래양 계산 및 최적 조합 추천", use_container_width=True)

if 제출:
    총모래양 = 모래양_DB['용소녀']['100']
    for 모험가, lv in 사용자_Lv.items():
        if lv > 0:
            총모래양 += 모래양_DB[모험가].get(str(lv), 0)

    st.subheader("3️⃣ 총 모래양 결과")
    st.success(f"총 모래양: {총모래양:,}개")

    후보 = []
    for 조합 in 공생합_조합:
        조합_모험가들 = 조합['모험가들']
        조합_소모량 = 조합['모래소모량']

        조건_위배 = False
        for 모험가, lv in 사용자_Lv.items():
            if lv == 0 and 조합_모험가들.get(모험가, 0) > 0:
                조건_위배 = True
                break

        if 조건_위배:
            continue

        if 조합_소모량 <= (총모래양 - 모래양_DB['용소녀']['100']):
            후보.append(조합)

    if 후보:
        최적 = max(후보, key=lambda x: x['공생합'])
        st.subheader("3️⃣ 추천 조합")
        st.markdown(f"✅ 필요한 모래양: **{최적['모래소모량']:,}개**")
        headers = "".join([f"<th>{모험가}</th>" for 모험가 in 최적["모험가들"]])
        rows = "".join([f"<td>Lv {lv}</td>" for lv in 최적["모험가들"].values()])
        st.markdown(f"""
        <table style='width:100%; text-align:left;'>
            <tr>{headers}</tr>
            <tr>{rows}</tr>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.warning("조건을 만족하는 공생합 조합이 없습니다.")

    if len(후보) >= 2:
        정렬된_후보 = sorted(후보, key=lambda x: (-x['공생합'], x['모래소모량']))
        차선 = 정렬된_후보[1]
        st.subheader("4️⃣ 다음 추천 조합")
        st.markdown(f"✅ 필요한 모래양: **{차선['모래소모량']:,}개**")
        headers = "".join([f"<th>{모험가}</th>" for 모험가 in 차선["모험가들"]])
        rows = "".join([f"<td>Lv {lv}</td>" for lv in 차선["모험가들"].values()])
        st.markdown(f"""
        <table style='width:100%; text-align:left;'>
            <tr>{headers}</tr>
            <tr>{rows}</tr>
        </table>
        """, unsafe_allow_html=True)

        st.subheader("5️⃣ 📅 예상 재분배 가능 시점")
        조석_난이도 = st.number_input("조석 소탕 난이도 (1 ~ 100)", min_value=1, max_value=100, value=50, step=1)
        차이 = max(0, 차선['모래소모량'] - 최적['모래소모량'])
        if 조석_난이도 > 0:
            예상_일수 = (차이 // (조석_난이도 * 5)) + (1 if 차이 % (조석_난이도 * 5) > 0 else 0)
            st.success(f"현재 조석 소탕 난이도 기준으로 약 {예상_일수}일 뒤에 재분배 가능합니다.")
    