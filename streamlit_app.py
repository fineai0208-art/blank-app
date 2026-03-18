import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# 1. 페이지 설정 (블랙 앤 네온 그린 보안 터미널 컨셉)
st.set_page_config(page_title="PROJECT NIGHT OWL v2.0", page_icon="🦉", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #00ff41 !important; border-bottom: 1px solid #00ff41; padding-bottom: 10px; }
    .stButton>button { background-color: #7b2cbf; color: white; border-radius: 5px; width: 100%; border: 1px solid #9d4edd; font-weight: bold; }
    .stButton>button:hover { background-color: #9d4edd; box-shadow: 0 0 10px #9d4edd; }
    .stAlert { background-color: #1a1a1a; color: white; border: 1px solid #00ff41; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #888888; font-family: 'Courier New'; font-weight: bold; }
    .stTabs [data-baseweb="tab"]:hover { color: #00ff41; }
    .stTabs [aria-selected="true"] { color: #00ff41 !important; border-bottom-color: #00ff41 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦉 PROJECT NIGHT OWL :: Tactical MSF Terminal v2.0")
st.caption("MSF Patent-Pending Security Protocol v2.0 (Air-gap 격리 상태) | Filtering Noise, Focusing on Life.")

# 2. 시스템 보안 상태 패널 (v2.0 강화)
col_s1, col_s2, col_s3 = st.columns(3)
col_s1.error("🔴 Dead Man's Switch: ARMED (활성화)")
col_s2.warning("🟡 Air-Gap Status: ISOLATED (격리됨)")
col_s3.success("🟢 Steganography: ENCRYPTED (암호화 완료)")

st.markdown("<br>", unsafe_allow_html=True)

# 3. 데이터 및 로직 (지피티 제공 데이터 통합)
# [지피티 인포그래픽 기반 좌표 및 통계 데이터]
paris_data = {
    '수단 (Sudan)': {
        'coords': [12.8628, 30.2176], # 가상 좌표
        'summary': '콜레라 대유행 (감염 124,418명 / 사망 3,573명)',
        'analysis': '상하수도 붕괴, 인구 이동, 홍수, 의료 접근 제한 복합 위기.',
        'threat_icon': '💊'
    },
    'DR콩고 (DRC)': {
        'coords': [-4.0383, 21.7587],
        'summary': '다중 전염병 동시 발생 (유행 45만 건 / 사망 8,700명)',
        'analysis': 'mpox, 홍역, 콜레라, 에볼라, 폴리오 동시 대응 상황.',
        'threat_icon': '💧'
    },
    '남수단 (South Sudan)': {
        'coords': [6.8770, 31.3070],
        'summary': '사상 최대 콜레라 확산 (감염 96,000건 / 사망 1,600명)',
        'analysis': '홍수, 국경 유입, 취약 보건체계로 인한 역대급 유행.',
        'threat_icon': '🌊'
    },
    '가자지구 (Gaza)': {
        'coords': [31.3547, 34.3088],
        'summary': '전쟁·기아·감염병 중첩 (사망 63,000+, 부상 161,000+)',
        'analysis': '오염수, 하수 파괴, 극심한 과밀, 폐기물 축적, 낮은 예방접종율.',
        'threat_icon': '💣'
    },
    '아이티 (Haiti)': {
        'coords': [18.9712, -72.2852],
        'summary': '치안붕괴 속 콜레라 재확산 (갱 폭력 사망 4,864명 / 콜레라 사망 17명)',
        'analysis': '보건 및 치안의 복합 위기로 의료 개입 필요성 극대화.',
        'threat_icon': '⚔️'
    }
}

# 4. 레이아웃 (좌: 작전 지도, 우: 전술 통찰)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🗺️ Operation Map (작전 지도)")
    st.write("요원들의 실시간 위치 및 고위험 핫스팟 데이터를 모니터링합니다.")
    
    # 조교님이 깔아준 Pandas/Plotly 기능을 데이터 연동으로 활용 (v2.4 환경 호환)
    # 지피티가 제공한 5개 고위험 지역 데이터프레임화
    map_data = pd.DataFrame({
        '구역': list(paris_data.keys()),
        '위도': [v['coords'][0] for v in paris_data.values()],
        '경도': [v['coords'][1] for v in paris_data.values()],
        '상태': ['고위험'] * 5, # 지피티가 준 고위험 5개 지역
        '상황': [v['summary'] for v in paris_data.values()]
    })
    
    # [제미나이 한글 겹침 해결 완료] 시크한 어두운 테마의 지도 (Plotly)
    # 한글 데이터를 Mapbox text 대신hover data로 연동하여 겹침 문제 근본적 해결
    fig = px.scatter_mapbox(map_data, lat='위도', lon='경도', text='구역',
                            title="NIGHT OWL 보안 네트워크 - 고위험 활동 지역", zoom=1, mapbox_style="carto-darkmatter")
    # Marker 색상을 네온 그린에서 레드(고위험)로 변경하여 긴장감 조성
    fig.update_traces(marker=dict(size=14, color='#ff0000'), textposition="top right") 
    fig.update_layout(paper_bgcolor='#000000', font_color='#00ff41', margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    
    # 선택 박스 (v2.4 환경 호환) - 니나님이 분석하고 싶은 구역 선택
    selected_district = st.selectbox("어디의 데이터를 분석할까요?", list(paris_data.keys()))
    
    if st.button("🚀 Run Logical Analysis (논리 분석 가동)"):
        with st.spinner("에어갭 격리 서버에서 데이터 복호화 및 분석 중..."):
            time.sleep(1.5)
            st.success("분석 완료! (NINA 특허 에어갭 기술 기반 무결성 검증 완료)")
            st.snow() # 성공 세리머니!

with col2:
    st.subheader("👁️ Tactical Insights (전술 통찰)")
    st.write("선택된 분쟁지역의 심층 보안 및 의료 데이터 분석 결과입니다.")
    
    # 선택된 구역의 지피티/인포그래픽 기반 데이터를 가져와서 시각적으로 표시
    district_info = paris_data[selected_district]
    
    # 정보 표시 (세련된 CSS 테두리 활용, 한글 안 겹침)
    st.markdown(f"""
        <div style='border: 1px solid #00ff41; padding: 20px; border-radius: 10px; background-color: #1a1a1a; margin-top: 10px;'>
            <div style='font-size: 24px; color: #ff0000;'>{district_info['threat_icon']} {selected_district} 고위험 상황 요약</div>
            <p style='color: white; font-size: 18px; margin-top: 10px;'>{district_info['summary']}</p>
            <h4 style='color: #00ff41; margin-top: 20px;'>🧠 시크한 논리 분석 (By Nina)</h4>
            <p style='color: white; font-size: 16px;'>{district_info['analysis']}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Nina's Tactical Lab | v2.0 | [v1.0] Acknowledging Data Integrity. Special thanks to the AI partner for logic support. Ensuring logic in complex crises. | C'est la vie!")
