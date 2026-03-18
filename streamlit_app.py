import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정 (강렬한 다크 & 시네마틱 레드 컨셉)
st.set_page_config(page_title="MSF Strategic Intelligence", page_icon="🚨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #080808; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    h1 { color: #ff1f1f !important; font-size: 50px !important; font-weight: 800; border-left: 10px solid #ff1f1f; padding-left: 20px; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .report-card { border: 2px solid #ff1f1f; padding: 30px; border-radius: 20px; background: linear-gradient(145deg, #111, #050505); box-shadow: 0 10px 30px rgba(255,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚨 MSF STRATEGIC MONITOR 2026")
st.write("전염병·위험요소·사망 통계를 함께 본 2025-2026 인도주의 핫스팟 인포그래픽")

# 2. 데이터 고도화 
# [cite: 3, 4, 5, 6, 7]
data = {
    "국가": ["수단", "DR콩고", "남수단", "가자지구", "아이티"],
    "위험_상태": ["콜레라 대유행", "다중 전염병 동시 발생", "사상 최대 콜레라 확산", "전쟁·기아·감염병 중첩", "치안붕괴 속 콜레라 재확산"],
    "감염_건수": [124418, 450000, 96000, 224000, 17], # [cite: 3, 4, 5, 6, 7]
    "사망자": [3573, 8700, 1600, 63000, 4881], # [cite: 3, 4, 5, 6, 7]
    "위험요소": [
        "상하수도 붕괴, 인구 이동, 홍수, 의료 접근 제한", # [cite: 3]
        "mpox, 홍역, 콜레라, 에볼라, 폴리오 동시 대응", # [cite: 4]
        "홍수, 국경 유입, 취약 보건체계, m-pox 부담", # [cite: 5]
        "오염수, 하수시설 파괴, 극심한 과밀, 낮은 예방접종", # [cite: 6]
        "갱 폭력, 대규모 인구 이동, 병원 운영 중단, 위생 악화" # [cite: 7]
    ],
    "lat": [12.86, -4.03, 6.87, 31.35, 18.97],
    "lon": [30.21, 21.75, 31.30, 34.30, -72.28]
}
df = pd.DataFrame(data)

# 3. 최상단 핵심 지표 (Key Metrics)
st.subheader("📌 Global Crisis Summary")
m1, m2, m3, m4 = st.columns(4)
m1.metric("총 분석 국가", "5개국")
m2.metric("최대 피해 지역", "가자지구", "63,000+ 사망") # [cite: 6]
m3.metric("최다 감염 지역", "DR콩고", "45만 건 이상") # [cite: 4]
m4.metric("주요 위협", "콜레라(Sudan/Haiti/South Sudan)") # [cite: 3, 5, 7]

st.markdown("<br>", unsafe_allow_html=True)

# 4. 시각화 섹션
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("🗺️ Tactical High-Risk Map")
    fig_map = px.scatter_mapbox(df, lat="lat", lon="lon", size="사망자", color="사망자",
                                 hover_name="국가", hover_data=["위험_상태"],
                                 color_continuous_scale='Reds', zoom=1, height=600,
                                 mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#000")
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("📊 Data Visualization")
    tab1, tab2 = st.tabs(["사망자 분포", "질환 규모"])
    
    with tab1:
        # 사망자 수 비교 막대 그래프
        fig_bar = px.bar(df, x="국가", y="사망자", color="사망자",
                          text_auto='.2s', color_continuous_scale='Reds')
        fig_bar.update_layout(template="plotly_dark", paper_bgcolor="#111", plot_bgcolor="#111")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with tab2:
        # 감염 건수 비중 파이 차트
        fig_pie = px.pie(df, values='감염_건수', names='국가', hole=0.5,
                          color_discrete_sequence=px.colors.sequential.YlOrRd_r)
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor="#111")
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 5. 상세 리포트 섹션
st.subheader("📑 Focused Humanitarian Intelligence")
target = st.selectbox("심층 분석 대상 국가 선택", df["국가"].unique())
info = df[df["국가"] == target].iloc[0]

st.markdown(f"""
<div class="report-card">
    <h2 style='margin-top:0; border:none;'>📍 {info['국가']} 위기 분석 리포트</h2>
    <p style='font-size: 22px;'><b>🚨 현황:</b> {info['위험_상태']}</p>
    <div style='display: flex; gap: 50px; margin: 20px 0;'>
        <div><p style='font-size: 18px; color: #ff4b4b;'><b>💀 보고된 사망자</b></p><p style='font-size: 30px;'>{info['사망자']:,} 명</p></div>
        <div><p style='font-size: 18px; color: #ff4b4b;'><b>🏥 감염/유행 건수</b></p><p style='font-size: 30px;'>{info['감염_건수']:,} 건</p></div>
    </div>
    <p style='font-size: 20px; line-height: 1.8;'><b>⚠️ 핵심 위기 요인:</b><br>{info['위험요소']}</p>
    <p style='color: #666; font-size: 14px; margin-top: 20px;'>출처: WHO, PAHO, OHCHR, OCHA 및 최신 위기 분석 데이터 기반 [cite: 2]</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Nina's Tactical Intelligence Dashboard | MSF Strategic Data Integration | 4-Year Attendance Integrity Verified.")
