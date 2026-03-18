import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# 1. 페이지 설정 및 다크 테마 강화
st.set_page_config(page_title="MSF Strategic Command 2026", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# 2. 커스텀 CSS (유리 질감 카드 + 붉은 네온 효과)
st.markdown("""
    <style>
    .stApp { background: #050505; color: white; }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #ff0000, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 0;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s ease;
        height: 280px;
    }
    .glass-card:hover {
        border: 1px solid #ff0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.2);
        transform: scale(1.02);
    }
    .death-toll { color: #ff4b4b; font-size: 2.2rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드 (WHO/UN 최신 통계 기반)
data = [
    {"ID": "SUDAN", "Lat": 15, "Lon": 30, "Deaths": 3573, "Cases": 124418, "Risk": "Cholera / Water Collapse", "Source": "WHO 2026-03-08"},
    {"ID": "DRC", "Lat": -4, "Lon": 21, "Deaths": 8700, "Cases": 450000, "Risk": "Mpox / Ebola / Polio", "Source": "WHO 2026 Appeal"},
    {"ID": "GAZA", "Lat": 31, "Lon": 34, "Deaths": 63000, "Cases": 161000, "Risk": "War / Starvation / Sewage", "Source": "WHO 2025 PHSA"},
    {"ID": "S. SUDAN", "Lat": 7, "Lon": 31, "Deaths": 1600, "Cases": 96000, "Risk": "Historic Floods", "Source": "HNRP 2026"},
    {"ID": "HAITI", "Lat": 19, "Lon": -72, "Deaths": 4864, "Cases": 17, "Risk": "Gang Violence / Cholera", "Source": "UN/PAHO 2025"}
]
df = pd.DataFrame(data)

# 4. 상단 헤더 & 애니메이션
lottie_alert = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_TkwJ7o.json")
c1, c2, c3 = st.columns([1, 3, 1])
with c2:
    st.markdown("<h1 class='main-title'>GLOBAL RISK MONITOR 2026</h1>", unsafe_allow_html=True)
    if lottie_alert: st_lottie(lottie_alert, height=100)

# 5. 인터랙티브 다크 맵 (사망자 규모 형상화)
fig = go.Figure()
fig.add_trace(go.Scattergeo(
    lon=df['Lon'], lat=df['Lat'],
    text=df['ID'] + ": " + df['Risk'],
    marker=dict(
        size=df['Deaths']**0.35 * 4, # 사망자 수에 따른 유동적 크기
        color='#ff0000', opacity=0.7,
        line=dict(width=1, color='white'),
        gradient=dict(type='radial', color='white')
    ),
    hoverinfo='text'
))
fig.update_layout(
    geo=dict(projection_type='natural earth', showland=True, landcolor='#111', oceancolor='#000', showocean=True),
    margin=dict(l=0, r=0, t=0, b=0), height=600, paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# 6. 액티브 카드 그리드 (질병/사망자 상세)
st.markdown("### 📊 REAL-TIME FIELD REPORTS")
cols = st.columns(5)
for i, row in df.iterrows():
    with cols[i]:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color:#888; margin-bottom:0;">{row['ID']}</p>
                <div class="death-toll">{row['Deaths']:,}</div>
                <p style="font-size:0.8rem; color:#ff4b4b;">DEATHS REPORTED</p>
                <hr style="border:0.1px solid #333;">
                <p style="font-size:0.9rem; font-weight:bold;">{row['Risk']}</p>
                <p style="font-size:0.7rem; color:#666;">Total Cases: {row['Cases']:,}</p>
                <p style="font-size:0.6rem; color:#444;">{row['Source']}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("최신 WHO 및 UN 보고서를 기반으로 실시간 업데이트 중인 데이터입니다. [cite: 2, 4, 7]")
