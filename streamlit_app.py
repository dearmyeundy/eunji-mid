import streamlit as st

st.set_page_config(layout="wide")

# --- 0. 세션 상태 초기화 및 데이터 정의 ---
if 'page' not in st.session_state:
    st.session_state.page = 'start'
if 'temp_score' not in st.session_state: 
    st.session_state.temp_score = 0
if 'value_score' not in st.session_state: 
    st.session_state.value_score = 0
if 'user_color' not in st.session_state: 
    st.session_state.user_color = None
if 'user_color_name' not in st.session_state: 
    st.session_state.user_color_name = "미선택"

# --- 데이터 정의 ---
COLOR_OPTIONS = {
    "따뜻한 노랑": "#FFD700", "맑은 하늘색": "#87CEEB", "깊은 갈색": "#8B4513",
    "밝은 코랄": "#FFA07A", "차분한 네이비": "#000080", "선명한 마젠타": "#FF00FF"
}

PALETTES = {
    "Spring": [["#FFE4B5", "미색"], ["#FFA07A", "코랄"], ["#FFD700", "골드"], ["#90EE90", "밝은 초록"]],
    "Autumn": [["#D2B48C", "베이지"], ["#B8860B", "골든 브라운"], ["#800000", "버건디"], ["#556B2F", "짙은 올리브"]],
    "Summer": [["#ADD8E6", "하늘색"], ["#B0C4DE", "연회색"], ["#E6E6FA", "라벤더"], ["#AFEEEE", "아쿠아"]],
    "Winter": [["#000000", "리얼 블랙"], ["#C0C0C0", "실버"], ["#FF00FF", "푸시아"], ["#4169E1", "로열 블루"]]
}

TONE_INFO = {
    "Spring": {"sci": "빛의 **긴 파장(Red/Yellow)** 영역 반사율이 높으며, 높은 **명도/채도**가 특징입니다. 디지털 자료의 활기를 높이는 데 적합합니다.",
               "psy": "생기발랄, 활기찬, 친근한 인상을 주어 학생 참여형 수업이나 긍정적 분위기 조성에 적합합니다.",
               "tips": "✅ **[미술/기술]** 활동적이고 밝은 PPT 디자인, 창의적 표현을 장려하는 포스터 제작 시 활용."},
    "Autumn": {"sci": "자연색에 가까우며 **낮은 채도**가 특징입니다. 중간 파장대(황색, 적갈색)를 안정적으로 반사합니다. 빛의 흡수율이 높아 안정적입니다.",
               "psy": "안정감, 신뢰, 전문적인 인상을 주어 발표 자료나 역사, 인문학 자료의 진중한 분위기 조성에 유용합니다.",
               "tips": "✅ **[사회/기술]** 역사 자료, 보고서, 발표 자료의 배경색으로 활용하여 신뢰감을 높임."},
    "Summer": {"sci": "차가운 파장대(청색 계열)를 기반으로 **명도가 높고 채도가 낮은**(부드러운) 톤입니다. 빛의 확산성(부드러움)이 높습니다.",
               "psy": "부드러움, 지적임, 청량감을 주어 학습 자료의 배경색이나 집중을 위한 환경 조성에 좋습니다.",
               "tips": "✅ **[과학/정보]** 복잡한 차트나 그래프의 보조 색상으로 활용하여 눈의 피로도를 낮춤."},
    "Winter": {"sci": "매우 **높은 채도**나 **매우 낮은 명도**의 극명한 대비가 특징입니다. 대비 효과를 통해 정보 전달력이 높습니다.",
               "psy": "카리스마, 세련됨, 강한 집중력을 유발하여 강조 색상이나 주의 집중 자료에 효과적입니다.",
               "tips": "✅ **[미술/정보]** 중요한 정보나 경고, 대비가 필요한 차트(Chart) 제작 시 흑백/고채도 대비를 활용하여 시선을 집중시킴."}
}


# --- 선택 영역 렌더링 함수 (버튼 일체감 강화) ---
def render_choice_block(key, label, color_code, score_effect, next_page):
    # 배경색에 따라 텍스트 색상을 자동으로 설정
    rgb_int = [int(color_code[i:i+2], 16) for i in (1, 3, 5)]
    text_color = 'black' if sum(rgb_int) > 380 else 'white'
    
    # 1. 시각적 영역 마크다운
    st.markdown(
        f"""
        <div style="
            background-color: {color_code}; 
            padding: 15px; 
            border-radius: 10px 10px 0 0; 
            color: {text_color}; 
            text-align: center; 
            margin-bottom: -15px; 
            border: 2px solid {text_color};
            border-bottom: none;
            height: 100%;
        ">
            <b>{label}</b>
        </div>
        """, unsafe_allow_html=True
    )
    
    # 2. 버튼 클릭 시 상태 변경 및 rerun
    if st.button("선택", key=key, use_container_width=True):
        if score_effect == 1:
            st.session_state.temp_score += 1
        elif score_effect == -1:
            st.session_state.temp_score -= 1
        elif score_effect == 2: 
            st.session_state.value_score += 1
        elif score_effect == -2: 
            st.session_state.value_score -= 1
            
        st.session_state.page = next_page
        st.rerun()
        
# === 1. 시작 페이지 ===
def start_page():
    st.title("👨‍🏫 교사 연수 자료: 퍼스널 컬러 진단 인터렉티브 학습자료")
    st.markdown("### 본 웹페이지는 교사의 자기 진단 및 수업 자료 개발 역량 강화를 위한 연수 도구입니다.")
    st.markdown("---")
    
    st.markdown("#### ✅ 학습 목표:")
    st.markdown("- 자신의 퍼스널 컬러 톤(4계절)을 진단하고, 선호 색깔에 대해 알아봅니다.")
    st.markdown("- 진단 결과를 바탕으로 **과학적 근거**(파장, 코드)와 **심리적 효과**를 분석합니다.")
    st.markdown("- **인터렉티브 활동지** 개발을 위한 **streamlit 활용 아이디어**을 착안합니다.")
    
    if st.button("진단 시작", key="btn_start", use_container_width=True):
        st.session_state.page = 'q1'
        st.session_state.temp_score = 0
        st.session_state.value_score = 0
        st.session_state.user_color = None
        st.session_state.user_color_name = "미선택"
        st.rerun()

# --- 2. 질문 페이지 (Q1: 온도) ---
def question_1():
    st.header("질문 1. 주얼리 색상 선호도는? (온도 진단)")
    st.info("[해설]: 이는 색의 온도(Warm/Cool)를 판별하는 가장 기본적인 질문입니다. 금속의 반사율 차이가 피부톤에 미치는 영향을 간접적으로 확인합니다.")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q1_a", "A. 따뜻하고 부드러운 골드 💍", "#FFD700", 1, 'q2') 

    with col_b:
        render_choice_block("q1_b", "B. 차갑고 깨끗한 실버 💎", "#C0C0C0", -1, 'q2') 

# --- 3. 질문 페이지 (Q2: 명도/채도) ---
def question_2():
    st.header("질문 2. 옷장 내 색감 선호도는? (명도/채도 진단)")
    st.info("[해설]: **명도(밝기)**와 **채도(선명도)**를 종합적으로 판단하여 Light/Mute 혹은 Vivid/Deep 톤 성향을 파악합니다.")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q2_a", "A. 밝고 화사하거나 부드럽고 연한 색상", "#F8F8FF", 2, 'q3') 

    with col_b:
        render_choice_block("q2_b", "B. 선명하고 강렬하거나 어둡고 깊은 색상", "#000080", -2, 'q3') 

# === 4. 질문 페이지 (Q3: 온도) ---
def question_3():
    st.header("질문 3. 끌리는 옷의 **블랙** 색감은? (온도 진단)")
    st.info("[해설]: 순수한 무채색으로 보이지만, 미묘한 노란빛(Warm) 또는 푸른빛(Cool)의 차이는 톤을 판별하는 중요한 요소입니다.")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q3_a", "A. 노란빛이 섞인 듯한 부드러운 웜 블랙", "#333333", 1, 'q4') 

    with col_b:
        render_choice_block("q3_b", "B. 새까맣고 강렬한 리얼 블랙", "#000000", -1, 'q4') 

# === 5. 질문 페이지 (Q4: 명도/채도) ---
def question_4():
    st.header("질문 4. 파우치 속 립스틱 색상은? (명도/채도 진단)")
    st.info("[해설]: 인위적인 색조 화장품을 통해 개인이 선호하는 색의 채도(선명함) 경향을 확인합니다.")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q4_a", "A. 맑고 투명하거나 채도가 낮은 색상", "#F7A3A6", 2, 'q5') 

    with col_b:
        render_choice_block("q4_b", "B. 아주 진하거나 채도가 높은 선명한 색상", "#B3172E", -2, 'q5') 

# === 6. 질문 페이지 (Q5: 선호 색상 선택) ---
def question_5():
    st.header("질문 5. 당신이 현재 가장 선호하는 컬러 하나를 선택해 주세요.")
    st.info("[해설]: 이 색상은 교육 자료 개발이나 개인적인 식습관 등에서 활용할 수 있는 심리적 선호색입니다.")
    st.markdown("---")

    options_list = list(COLOR_OPTIONS.items())
    cols = st.columns(3)
    
    for i, (name, hex_code) in enumerate(options_list):
        col = cols[i % 3]
        with col:
            # 시각적 영역 마크다운
            st.markdown(
                f"""
                <div style="
                    background-color: {hex_code}; 
                    height: 50px; 
                    border-radius: 10px;
                    border: 1px solid black;
                    margin-bottom: -15px; 
                "></div>
                """, unsafe_allow_html=True
            )
            
            # 버튼 클릭 시 선택 완료
            if st.button(f"선택: {name}", key=f"color_pick_{i}", use_container_width=True):
                st.session_state.user_color = hex_code
                st.session_state.user_color_name = name
                st.session_state.page = 'result'
                st.rerun()

# === 7. 결과 페이지 (4계절 진단 및 학습 자료 제공) ---
def result_page():
    temp_s = st.session_state.temp_score
    value_s = st.session_state.value_score
    user_color = st.session_state.user_color
    user_color_name = st.session_state.user_color_name

    # 4계절 진단 로직
    if temp_s > 0: 
        if value_s >= 0:
            result_title = "🌸 봄 웜톤 (Spring Warm)"
            bg_color = "#FFF0DB"
            text_color_main = "#FF8C00"
            palette_data = PALETTES["Spring"]
            result_type = "Spring"
        else:
            result_title = "🍂 가을 웜톤 (Autumn Warm)"
            bg_color = "#E6D0B4"
            text_color_main = "#8B4513"
            palette_data = PALETTES["Autumn"]
            result_type = "Autumn"
    else: 
        if value_s >= 0:
            result_title = "🧊 여름 쿨톤 (Summer Cool)"
            bg_color = "#E0FFFF"
            text_color_main = "#4682B4"
            palette_data = PALETTES["Summer"]
            result_type = "Summer"
        else:
            result_title = "❄️ 겨울 쿨톤 (Winter Cool)"
            bg_color = "#B0C4DE"
            text_color_main = "#000080"
            palette_data = PALETTES["Winter"]
            result_type = "Winter"
    
    user_recommendation = f"진단된 **{result_type} 톤**과 선호 색상을 결합하여 효과적인 교수 학습 환경을 디자인하세요."

    # HTML/Markdown을 이용한 시각적 변화 (결과 요약)
    st.markdown(
        f"""
        <div style="background-color: {bg_color}; padding: 30px; border-radius: 15px; text-align: center;">
            <h1 style="color: {text_color_main};">{result_title} 진단 결과</h1>
            <p style="font-size: 1.2em; color: #333333;">{user_recommendation}</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("---")
    
    # --- 탭 구성 (교사 연수 자료의 핵심) ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 톤 결과 분석", "🔬 과학적 근거", "🧠 색채 심리 응용", "📚 수업 활용 팁"])

    with tab1: # 톤 결과 분석 탭
        st.header(f"자세한 분석: {result_title}")
        st.info(f"**진단 요약:** 색의 온도({temp_s}점), 명도/채도({value_s}점)를 기반으로 도출된 톤입니다. ")
        
        st.subheader("나의 선호색과 베스트 팔레트")
        cols = st.columns(len(palette_data) + 1)
        
        # 1. 선호 색상 출력 (가장 첫 번째 열)
        cols[0].markdown(
            f"""
            <div style="background-color: {user_color}; height: 80px; border-radius: 10px; border: 3px solid {text_color_main}; margin-bottom: 5px;"></div>
            <p style="text-align: center; font-size: 0.9em; color: black;">
                선호색: {user_color_name}<br>
                코드: {user_color} 
            </p>
            """, unsafe_allow_html=True
        )

        # 2. 추천 컬러 팔레트 출력 (두 번째 열부터)
        for i, (hex_code, name) in enumerate(palette_data):
            cols[i + 1].markdown(
                f"""
                <div style="background-color: {hex_code}; height: 80px; border-radius: 10px; margin-bottom: 5px;"></div>
                <p style="text-align: center; font-size: 0.9em; color: black;">
                    {name}<br>
                    ({hex_code})
                </p>
                """, unsafe_allow_html=True
            )

    with tab2: # 과학적 근거 탭
        st.header("색채의 과학: 빛, 파장, 코드 (과학/정보 연계)")
        st.info(f"**주요 파장 영역:** {TONE_INFO[result_type]['sci']}")
        st.markdown("---")
        
        st.subheader("추천 색상의 정보 인코딩")
        st.markdown("색은 디지털(RGB/HEX)과 인쇄(CMYK) 환경에서 다르게 인코딩됩니다. 교육 자료 제작 시 이를 고려해야 합니다.")
        
        # 첫 번째 추천 색상의 코드 분석
        hex_code = palette_data[0][0]
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)
        
        col_codes = st.columns(3)
        col_codes[0].metric("HEX 코드", hex_code)
        col_codes[1].metric("RGB 코드", f"({r}, {g}, {b})")
        col_codes[2].metric("색의 3속성", f"온도: {'웜' if temp_s > 0 else '쿨'}, 명도/채도: {'고/저' if value_s >= 0 else '중/고'}")

    with tab3: # 색채 심리 응용 탭
        st.header("색채 심리: 학습 환경에 미치는 영향 (미술/심리 연계)")
        st.markdown(f"**{result_type} 톤이 주는 심리적 인상:** {TONE_INFO[result_type]['psy']}")
        st.markdown("---")
        st.info("💡 **교실 환경 색상 활용 팁:** 높은 채도는 활기를 주지만 산만함을, 낮은 채도는 집중력을 높이지만 따분함을 줄 수 있습니다. 이 톤의 색상을 어떻게 조화시켜 학습 효율을 높일지 고민해 보세요.")

    with tab4: # 수업 활용 팁 탭
        st.header("수업 활용 아이디어 (기술/가정, 기타 교과 연계)")
        st.markdown(f"**{result_type} 톤**을 활용하여 교사가 시도할 수 있는 구체적인 수업 아이디어입니다.")
        st.success(f"{TONE_INFO[result_type]['tips']}")
        st.markdown("---")
        st.info("💡 **디지털 자료 제작 팁:** 이 톤의 색상을 활용하여 PPT 템플릿을 제작하거나, 웹사이트(Streamlit) 배경색으로 사용하여 특정 정서적 분위기를 연출해 볼 수 있습니다.")

    st.markdown("---")
    if st.button("다시 진단하기", key="btn_restart", use_container_width=True):
        st.session_state.page = 'start'
        st.session_state.temp_score = 0
        st.session_state.value_score = 0
        st.session_state.user_color = None
        st.session_state.user_color_name = "미선택"
        st.rerun()


# === 8. 페이지 흐름 제어 ===
if st.session_state.page == 'start':
    start_page()
elif st.session_state.page == 'q1':
    question_1()
elif st.session_state.page == 'q2':
    question_2()
elif st.session_state.page == 'q3':
    question_3()
elif st.session_state.page == 'q4':
    question_4()
elif st.session_state.page == 'q5':
    question_5()
elif st.session_state.page == 'result':
    result_page()