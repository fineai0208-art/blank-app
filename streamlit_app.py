import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="MSF 2026 High-Risk Areas", layout="wide")

# 스타일링 (CSS)
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: white; }
    .stMetric { background-color: #2d2d2d; padding: 15px; border-radius: 10px; border-left: 5px solid #ff0000; }
    h1, h2, h3 { color: #ff0000 !important; font-family: 'Helvetica Neue', sans-serif; }
    .report-text { font-size: 1.1rem; line-height: 1.6; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# 1. 데이터 준비
data = {
    "Country": ["Sudan", "DRC", "South Sudan", "Gaza", "Haiti"],
    "Lat": [12.8628, -4.0383, 6.8770, 31.3547, 18.9712],
    "Lon": [30.2176, 21.7587, 31.3070, 34.3088, -72.2852],
    "Crisis_Type": ["Cholera Outbreak", "Multi-Epidemic", "Historic Cholera", "War & Disease", "Violence & Cholera"],
    "Stats": [
        "124,418 cases / 3,573 deaths",
        "450,000+ cases / 8,700+ deaths",
        "96,000+ cases / 1,600 deaths",
        "63,000+ deaths / 161,000+ injuries",
        "4,864 violence deaths / 17 recent cholera deaths"
    ],
    "Risk_Factors": [
        "Water system collapse, displacement, floods",
        "Mpox, measles, cholera, ebola, polio",
        "Floods, border influx, weak health system",
        "Starvation, sewage destruction, overcrowding",
        "Gang violence, hospital closures, unstable water"
    ],
    "Sources": ["WHO 2026-03-08", "WHO 2026 Appeal", "HNRP 2026", "WHO 2025 PHSA", "UN/PAHO 2025"]
}

df = pd.DataFrame(data)

# 헤더 섹션
st.title("🚨 MSF High-Risk Areas 2026")
st.subheader("Global Humanitarian Hotspots: Disease & Conflict Analytics")
st.markdown("---")

# 2. 인터랙티브 지도 생성 (Plotly)
fig = go.Figure()

# 지도 위에 마커 추가
fig.add_trace(go.Scattergeo(
    lon = df['Lon'],
    lat = df['Lat'],
    text = df['Country'] + "<br>" + df['Crisis_Type'],
    hoverinfo = 'text',
    mode = 'markers',
    marker = dict(
        size = 18,
        color = 'red',
        opacity = 0.8,
        symbol = 'circle',
        line = dict(width=2, color='white'),
        gradient = dict(type='radial', color='white')
    )
))

# 지도 레이아웃 설정 (다크 모드)
fig.update_layout(
    geo = dict(
        scope='world',
        projection_type='natural earth',
        showland=True,
        landcolor="rgb(40, 40, 40)",
        subunitcolor="rgb(100, 100, 100)",
        countrycolor="rgb(100, 100, 100)",
        showlakes=False,
        bgcolor="rgba(0,0,0,0)"
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
)

# 지도 출력
st.plotly_chart(fig, use_container_width=True)

# 3. 상세 정보 대시보드 (클릭/선택 연동)
st.markdown("### 🔍 상세 지역 분석 (Select Country)")
selected_country = st.selectbox("분석할 지역을 선택하세요:", df['Country'])

# 선택된 국가 데이터 추출
country_info = df[df['Country'] == selected_country].iloc[0]

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"## {country_info['Country']}")
    st.markdown(f"**Crisis Status:** `{country_info['Crisis_Type']}`")
    st.metric(label="Critical Statistics", value=country_info['Stats'].split('/')[0], delta="Extreme Risk")
    st.write(f"**Secondary Stats:** {country_info['Stats'].split('/')[-1]}")

with col2:
    st.info(f"**Main Risk Factors:**\n\n {country_info['Risk_Factors']}")
    st.caption(f"Source: {country_info['Sources']}")

# 하단 통계 요약 테이블
st.markdown("---")
st.markdown("### 📊 Overall Statistics Summary")
st.table(df[['Country', 'Crisis_Type', 'Stats']])
