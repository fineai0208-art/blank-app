import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 (초고대비 보안 터미널)
st.set_page_config(page_title="MSF Strategic Monitor", page_icon="🚨", layout="wide")

st.markdown("""
    <style>
    /* 배경은 완전 블랙, 글씨는 순백색(#FFFFFF)으로 가독성 100% 확보 */
    .main { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Pretendard', sans-serif; }
    
    /* 제목: 피처럼 붉은 네온 레드 */
    h1 { color: #FF0000 !important; font-size: 60px !important; font-weight: 900; text-transform: uppercase; letter-spacing: -2px; }
    h2, h3 { color: #FF3333 !important; font-size: 32px !important; border-bottom: 2px solid #FF3333; }
    
    /* 메트릭 숫자: 눈부신 화이트 */
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 40px !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #FF3333 !important; font-size: 20px !important; }

    /* 리포트 카드: 대비 극대화 */
    .report-card { 
        border: 4px solid #FF0000; 
        padding: 40px; 
        border-radius: 25px; 
        background-color: #0A0A0A; 
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
    }
    .big-text { font-size: 24px !important; color: #FFFFFF !important; line-height: 1.6; }
    .highlight { color: #FF0000; font-weight: bold; font-size: 28px; }
    
    /* 셀렉트박스 글씨도 크게 */
    .stSelectbox label { font-size: 22px !important; color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 MSF TACTICAL MONITOR 2026")
st.markdown("<p style='font-size:22px; color:#AAA;'>전염병·위험요소·사망 통계 기반 인도주의 핫스팟 (Data: WHO/UN 2026)</p>", unsafe_allow_html=True)

# 2. 데이터 (지피티 제공 데이터 무결성 반영)
data = {
    "국가": ["수단", "DR콩고", "남수단", "가자지구", "아이티"],
    "위험_상태": ["콜레라 대유행", "다중 전염병 동시 발생", "사상 최대 콜레라 확산", "전쟁·기아·감염병 중첩", "치안붕괴 속 콜레라 재확산"],
    "감염_건수": [124418, 450000, 96000, 224000, 17],
    "사망자": [3573, 8700, 1600, 63000, 4881],
    "요인": [
        "상하수도 붕괴, 인구 이동, 홍수, 의료 접근 제한 ",
        "mpox, 홍역, 콜레라, 에볼라, 폴리오 동시 대응 ",
        "홍수, 국경 유입, 취약 보건체계 ",
        "오염수, 하수시설 파괴, 극심한 과밀, 낮은 예방접종 ",
        "갱 폭력, 대규모 인구 이동, 병원 운영 중단, 위생 악화 "
    ],
    "lat": [12.86, -4.03, 6.87, 31.35, 18.97],
    "lon": [30.21, 21.75, 31.30, 34.30, -72.28]
}
df = pd.DataFrame(data)

# 3. 핵심 지표 섹션
m1, m2, m3 = st.columns(3)
m1.metric("총 분석 국가", "5개국")
m2.metric("최대 사망 보고", "가자지구", "63,000+ 명 ")
m3.metric("최다 감염 유행", "DR콩고", "450,000+ 건 ")

st.markdown("<br>", unsafe_allow_html=True)

# 4. 지도 및 차트 (고대비 설정)
c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("🌐 Global Crisis Map")
    fig_map = px.scatter_mapbox(df, lat="lat", lon="lon", size="사망자", color="사망자",
                                 hover_name="국가", color_continuous_scale='Reds',
                                 zoom=1, height=600, mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#000", font_color="#FFF")
    st.plotly_chart(fig_map, use_container_width=True)

with c2:
    st.subheader("📊 Mortality Distribution")
    fig_bar = px.bar(df, x="국가", y="사망자", color="사망자", text_auto='.2s', color_continuous_scale='Reds')
    fig_bar.update_layout(template="plotly_dark", paper_bgcolor="#000", plot_bgcolor="#000", font_size=15)
    st.plotly_chart(fig_bar, use_container_width=True)

# 5. 상세 리포트 (글씨 크기 극대화)
st.markdown("<br>", unsafe_allow_html=True)
target = st.selectbox("상세 분석 국가 선택 ↓", df["국가"].unique())
info = df[df["국가"] == target].iloc[0]

st.markdown(f"""
<div class="report-card">
    <h1 style='color:#FF0000; border:none; margin-bottom:10px;'>LOCATION: {info['국가']}</h1>
    <p class="big-text"><span class="highlight">현황:</span> {info['위험_상태']}</p>
    <div style='display: flex; gap: 80px; margin: 30px 0;'>
        <div><p style='color:#FF3333; font-size:22px;'>보고된 사망자</p><p style='font-size:50px; font-weight:bold;'>{info['사망자']:,}명</p></div>
        <div><p style='color:#FF3333; font-size:22px;'>감염/유행 건수</p><p style='font-size:50px; font-weight:bold;'>{info['감염_건수']:,}건</p></div>
    </div>
    <p class="big-text"><span class="highlight">핵심 위기 요인:</span><br>{info['요인']}</p>
</div>
""", unsafe_allow_html=True)

st.caption("Nina's Tactical Intelligence Dashboard | MSF Strategic Data Integration | Attendance: 100%")
