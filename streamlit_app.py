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
            border-radius: 10px 10px 0 0; /* 상단만 둥글게 */
            color: {text_color}; 
            text-align: center; 
            margin-bottom: -15px; /* 버튼과 마크다운 영역을 겹치게 하여 일체감 강화 */
            border: 2px solid {text_color};
            border-bottom: none;
            height: 100%;
        ">
            <b>{label}</b>
        </div>
        """, unsafe_allow_html=True
    )
    
    # 2. 버튼 클릭 시 상태 변경 및 rerun
    # 버튼 라벨을 '선택' 한 단어로 최소화하고, use_container_width=True로 폭을 맞춥니다.
    if st.button("선택", key=key, use_container_width=True):
        if score_effect == 1:
            st.session_state.temp_score += 1
        elif score_effect == -1:
            st.session_state.temp_score -= 1
        elif score_effect == 2: # 명도/채도 +1
            st.session_state.value_score += 1
        elif score_effect == -2: # 명도/채도 -1
            st.session_state.value_score -= 1
            
        st.session_state.page = next_page
        st.rerun()

# === 1. 시작 페이지 ===
def start_page():
    st.title("💖 4계절 퍼스널 컬러 & 색상 추천 진단")
    st.markdown("### 5가지 질문에 답하고, 나에게 가장 잘 맞는 컬러와 선호 컬러 기반 추천을 받아보세요!")
    st.markdown("---")
    
    if st.button("진단 시작하기!", key="btn_start", use_container_width=True):
        st.session_state.page = 'q1'
        st.session_state.temp_score = 0
        st.session_state.value_score = 0
        st.session_state.user_color = None
        st.session_state.user_color_name = "미선택"
        st.rerun()

# --- 2. 질문 페이지 (Q1: 온도) ---
def question_1():
    st.header("질문 1. 평소 당신이 선호하는 주얼리(액세서리) 색상은? (온도 진단)")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q1_a", "A. 따뜻하고 부드러운 골드 💍", "#FFD700", 1, 'q2') # 웜톤 +1

    with col_b:
        render_choice_block("q1_b", "B. 차갑고 깨끗한 실버 💎", "#C0C0C0", -1, 'q2') # 쿨톤 -1

# --- 3. 질문 페이지 (Q2: 명도/채도) ---
def question_2():
    st.header("질문 2. 평소 당신의 옷장에서 가장 많은 색감은? (명도/채도 진단)")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q2_a", "A. 밝고 화사하거나 부드럽고 연한 색상", "#F8F8FF", 2, 'q3') # 라이트/뮤트 +1

    with col_b:
        render_choice_block("q2_b", "B. 선명하고 강렬하거나 어둡고 깊은 색상", "#000080", -2, 'q3') # 딥/비비드 -1

# === 4. 질문 페이지 (Q3: 온도) ---
def question_3():
    st.header("질문 3. 당신이 끌리는 옷의 **블랙** 색감은? (온도 진단)")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q3_a", "A. 노란빛이 섞인 듯한 부드러운 웜 블랙", "#333333", 1, 'q4') # 웜톤 +1

    with col_b:
        render_choice_block("q3_b", "B. 새까맣고 강렬한 리얼 블랙", "#000000", -1, 'q4') # 쿨톤 -1

# === 5. 질문 페이지 (Q4: 명도/채도) ---
def question_4():
    st.header("질문 4. 당신의 파우치 속 립스틱 색상은? (명도/채도 진단)")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        render_choice_block("q4_a", "A. 맑고 투명하거나 채도가 낮은 색상", "#F7A3A6", 2, 'q5') # 라이트/뮤트 +1

    with col_b:
        render_choice_block("q4_b", "B. 아주 진하거나 채도가 높은 선명한 색상", "#B3172E", -2, 'q5') # 딥/비비드 -1

# === 6. 질문 페이지 (Q5: 선호 색상 선택) ---
def question_5():
    st.header("질문 5. 당신이 현재 가장 선호하는 컬러 하나를 선택해 주세요.")
    st.markdown("---")

    options_list = list(COLOR_OPTIONS.items())
    cols = st.columns(3)
    
    for i, (name, hex_code) in enumerate(options_list):
        col = cols[i % 3]
        with col:
            # st.markdown으로 색상과 이름 표시 (선택 영역)
            st.markdown(
                f"""
                <div style="
                    background-color: {hex_code}; 
                    height: 50px; 
                    border-radius: 10px;
                    border: 1px solid black;
                    margin-bottom: -15px; /* 버튼과 밀착 */
                "></div>
                """, unsafe_allow_html=True
            )
            
            # 버튼 클릭 시 선택 완료
            if st.button(f"선택: {name}", key=f"color_pick_{i}", use_container_width=True):
                st.session_state.user_color = hex_code
                st.session_state.user_color_name = name
                st.session_state.page = 'result'
                st.rerun()

# === 7. 결과 페이지 (4계절 진단 및 선호 색상 기반 추천) ---
def result_page():
    temp_s = st.session_state.temp_score
    value_s = st.session_state.value_score
    user_color = st.session_state.user_color
    user_color_name = st.session_state.user_color_name

    # 4계절 진단 로직
    if temp_s > 0: # 웜톤
        if value_s >= 0:
            result_title = "🌸 봄 웜톤 (Spring Warm)"
            bg_color = "#FFF0DB"
            text_color_main = "#FF8C00"
            palette_data = PALETTES["Spring"]
        else:
            result_title = "🍂 가을 웜톤 (Autumn Warm)"
            bg_color = "#E6D0B4"
            text_color_main = "#8B4513"
            palette_data = PALETTES["Autumn"]
    else: # 쿨톤
        if value_s >= 0:
            result_title = "🧊 여름 쿨톤 (Summer Cool)"
            bg_color = "#E0FFFF"
            text_color_main = "#4682B4"
            palette_data = PALETTES["Summer"]
        else:
            result_title = "❄️ 겨울 쿨톤 (Winter Cool)"
            bg_color = "#B0C4DE"
            text_color_main = "#000080"
            palette_data = PALETTES["Winter"]
    
    user_recommendation = "퍼스널 컬러를 바탕으로 선호 색상을 활용하여 더욱 매력적인 스타일링을 연출해 보세요!"

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
    
    # --- 추천 팔레트 및 선호 색상 (선호 색상이 제일 앞으로) ---
    st.subheader("✨ 나의 선호 색상과 추천 컬러 팔레트")
    
    cols = st.columns(len(palette_data) + 1)
    
    # 1. 선호 색상 출력 (가장 첫 번째 열)
    cols[0].markdown(
        f"""
        <div style="background-color: {user_color}; height: 80px; border-radius: 10px; border: 3px solid {text_color_main}; margin-bottom: 5px;"></div>
        <p style="text-align: center; font-size: 0.9em; color: black;">
            나의 선호색<br>
            ({user_color_name})<br>
            ({user_color}) 
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