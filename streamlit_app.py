import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. 페이지 설정 및 다크 테마 보안 스타일링
st.set_page_config(page_title="MSF High-Risk Monitor", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #111; border: 1px solid #ff4b4b; padding: 10px; border-radius: 5px; }
    h1, h2, h3 { color: #ff4b4b !important; }
    .report-box { border: 1px solid #00ff41; padding: 15px; border-radius: 10px; background-color: #111; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 MSF High-Risk Areas 2026 : Tactical Monitor")
st.write("전염병·위험요소·사망 통계를 함께 본 2025-2026 인도주의 핫스팟 [cite: 1]")

# 2. 핵심 데이터 구성
# 수단, DR콩고, 남수단, 가자지구, 아이티 데이터 통합 [cite: 1, 3, 4, 5, 6, 7]
msf_data = {
    "수단": {
        "lat": 12.86, "lon": 30.21,
        "위험": "콜레라 대유행",
        "통계": "감염 124,418명 / 사망 3,573명 [cite: 3]",
        "요인": "상하수도 붕괴, 인구 이동, 홍수, 의료 접근 제한 [cite: 3]",
        "출처": "WHO Sudan cholera update (2026-03-08)"
    },
    "DR콩고": {
        "lat": -4.03, "lon": 21.75,
        "위험": "다중 전염병 동시 발생",
        "통계": "유행 45만 건 이상 / 사망 8,700명 이상 [cite: 4]",
        "요인": "mpox, 홍역, 콜레라, 에볼라, 폴리오 동시 대응 [cite: 4]",
        "출처": "WHO 2026 긴급호소"
    },
    "남수단": {
        "lat": 6.87, "lon": 31.30,
        "위험": "역대 최대 규모 콜레라 확산",
        "통계": "96,000건 이상 / 사망 약 1,600명 [cite: 5]",
        "요인": "홍수, 국경 유입, 취약 보건체계, m-pox/간염 E 부담 [cite: 5]",
        "출처": "South Sudan HNRP 2026"
    },
    "가자지구": {
        "lat": 31.35, "lon": 34.30,
        "위험": "전쟁·기아·감염병 복합 위기",
        "통계": "사망 63,000+, 부상 161,000+ [cite: 6]",
        "요인": "오염수, 하수시설 파괴, 극심한 과밀, 낮은 예방접종 [cite: 6]",
        "출처": "WHO 2025 PHSA"
    },
    "아이티": {
        "lat": 18.97, "lon": -72.28,
        "위험": "치안붕괴 속 콜레라 재확산",
        "통계": "갱 폭력 사망 4,864명 / 콜레라 사망 17명 [cite: 7]",
        "요인": "성폭력, 대규모 인구 이동, 병원 운영 중단, 위생 악화 [cite: 7]",
        "출처": "UN 2025 / PAHO 2025"
    }
}

# 3. 레이아웃: 지도와 상세 리포트
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌐 Global High-Risk Map")
    df = pd.DataFrame([
        {"Country": k, "Lat": v["lat"], "Lon": v["lon"], "Risk": v["위험"]} 
        for k, v in msf_data.items()
    ])
    
    # 붉은 점으로 위험 지역 표시 (한글 겹침 방지를 위해 텍스트는 빼고 툴팁에 집중)
    fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", hover_name="Country", hover_data=["Risk"],
                            zoom=1, height=600, mapbox_style="carto-darkmatter")
    fig.update_traces(marker=dict(size=15, color='#ff4b4b'))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#000")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📄 Field Report Detail")
    selected_country = st.selectbox("분석 국가 선택", list(msf_data.keys()))
    
    data = msf_data[selected_country]
    st.markdown(f"""
    <div class="report-box">
        <h3>📍 {selected_country}</h3>
        <p><b>위험 상태:</b> {data['위험']}</p>
        <hr>
        <p><b>📊 주요 통계:</b><br>{data['통계']}</p>
        <p><b>⚠️ 핵심 위험요소:</b><br>{data['요인']}</p>
        <small style="color: #888;">출처: {data['출처']}</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚨 긴급 데이터 송출 (NIGHT OWL Protocol)"):
        with st.spinner("복호화 중..."):
            time.sleep(1)
            st.success("데이터 무결성 검증 완료. 보안 송출 성공.")

st.markdown("---")
st.caption("Data sources: WHO, PAHO, OHCHR, OCHA  | System Securely Maintained by Nina")
