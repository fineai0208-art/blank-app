import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# 1. 페이지 설정 (블랙 & 레드 보안 컨셉)
st.set_page_config(page_title="MSF Strategic Monitor", page_icon="🚨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #e0e0e0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    h1 { color: #ff4b4b !important; font-size: 45px !important; text-shadow: 2px 2px #000; }
    h2, h3 { color: #ff4b4b !important; }
    .stSelectbox label { font-size: 20px !important; color: #00ff41 !important; }
    .report-card { border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background-color: #111; line-height: 1.6; }
    .stat-text { font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 MSF Tactical Crisis Monitor 2026")
st.write("2025-2026 인도주의 위기 지역: 전염병·치안·사망 복합 데이터 분석")

# 2. 데이터 구성 [cite: 1, 2]
data = {
    "국가": ["수단", "DR콩고", "남수단", "가자지구", "아이티"],
    "감염_질환건수": [124418, 450000, 96000, 224000, 17], # 가자는 부상+사망 합산 추정치 포함 [cite: 3, 4, 5, 6, 7]
    "사망자": [3573, 8700, 1600, 63000, 4881], # 아이티는 갱폭력+콜레라 합산 [cite: 3, 4, 5, 6, 7]
    "위험유형": ["콜레라 대유행", "다중 전염병", "최대 규모 콜레라", "전쟁·기아 복합", "치안·보건 붕괴"],
    "핵심요인": [
        "상하수도 붕괴, 인구 이동, 홍수 [cite: 3]",
        "mpox, 홍역, 에볼라 동시 대응 [cite: 4]",
        "홍수, 국경 유입, 취약 보건체계 [cite: 5]",
        "오염수, 하수시설 파괴, 극심한 과밀 [cite: 6]",
        "갱 폭력, 병원 운영 중단, 위생 악화 [cite: 7]"
    ],
    "lat": [12.86, -4.03, 6.87, 31.35, 18.97],
    "lon": [30.21, 21.75, 31.30, 34.30, -72.28]
}
df = pd.DataFrame(data)

# 3. 메인 대시보드 레이아웃
row1_col1, row1_col2 = st.columns([1.5, 1])

with row1_col1:
    st.subheader("🌐 Global Crisis Hotspots (Live Map)")
    fig_map = px.scatter_mapbox(df, lat="lat", lon="lon", size="사망자", color="사망자",
                                 hover_name="국가", hover_data=["위험유형", "사망자"],
                                 color_continuous_scale=px.colors.sequential.Reds,
                                 zoom=1, height=500, mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#000")
    st.plotly_chart(fig_map, use_container_width=True)

with row1_col2:
    st.subheader("📊 Mortality Comparison (사망자 비교)")
    fig_bar = px.bar(df, x="국가", y="사망자", color="국가", text_auto='.2s',
                      title="국가별 보고된 총 사망자 수 (2025-2026)",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_bar.update_layout(showlegend=False, template="plotly_dark", paper_bgcolor="#000")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.subheader("📈 Infection & Disease Cases (질환 규모)")
    fig_pie = px.pie(df, values='감염_질환건수', names='국가', hole=0.4,
                      title="지역별 질환/유행 규모 비중",
                      color_discrete_sequence=px.colors.sequential.RdBu)
    fig_pie.update_layout(template="plotly_dark", paper_bgcolor="#000")
    st.plotly_chart(fig_pie, use_container_width=True)

with row2_col2:
    st.subheader("📑 Focused Intelligence Report")
    target = st.selectbox("분석 대상 국가 선택", df["국가"].unique())
    info = df[df["국가"] == target].iloc[0]
    
    st.markdown(f"""
    <div class="report-card">
        <h2 style='margin-top:0;'>📍 {info['국가']} 분석 리포트</h2>
        <p class="stat-text"><b>🚨 위기 유형:</b> {info['위험유형']}</p>
        <p class="stat-text"><b>📉 피해 규모:</b> 사망 {info['사망자']:,}명 / 질환건수 {info['감염_질환건수']:,}건</p>
        <p class="stat-text"><b>⚠️ 위험 요인:</b> {info['핵심요인']}</p>
        <hr style='border-color: #444;'>
        <p style='color: #888; font-size: 14px;'>Data Source: WHO, UN, OCHA based on 2026 intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Nina's Tactical Dashboard | MSF Strategic Data Integration | Filtering Noise, Saving Lives.")
