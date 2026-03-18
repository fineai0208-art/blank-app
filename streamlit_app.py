import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MSF 고위험 지역 2026",
    page_icon="🆘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 전역 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans KR', sans-serif;
    background-color: #0f1117;
    color: #e8e8e8;
  }

  /* 헤더 */
  .msf-header {
    background: linear-gradient(135deg, #1a0a0a 0%, #1e1e2e 100%);
    border-left: 5px solid #e63946;
    padding: 28px 36px 20px;
    margin-bottom: 24px;
    border-radius: 0 8px 8px 0;
  }
  .msf-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
  }
  .msf-header .subtitle {
    font-size: 0.85rem;
    color: #9a9ab0;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.5px;
  }

  /* 국가 카드 */
  .country-card {
    background: #16213e;
    border: 1px solid #2a2a4a;
    border-left: 4px solid #e63946;
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .country-card:hover {
    border-color: #e63946;
    background: #1a2550;
    transform: translateX(4px);
  }
  .country-card h3 {
    margin: 0 0 6px 0;
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
  }
  .country-card .stats {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #e63946;
    font-weight: 600;
  }
  .country-card .risk-tag {
    font-size: 0.72rem;
    color: #9a9ab0;
    margin-top: 4px;
  }

  /* 상세 패널 */
  .detail-panel {
    background: #16213e;
    border: 1px solid #e63946;
    border-radius: 10px;
    padding: 28px;
    margin-top: 8px;
  }
  .detail-panel h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 4px 0;
  }
  .detail-panel .crisis-type {
    font-size: 0.8rem;
    color: #e63946;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 20px;
  }

  /* 통계 박스 */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
  }
  .stat-box {
    background: #0f1117;
    border-radius: 8px;
    padding: 14px 16px;
    text-align: center;
    border: 1px solid #2a2a4a;
  }
  .stat-box .number {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e63946;
    font-family: 'IBM Plex Mono', monospace;
  }
  .stat-box .label {
    font-size: 0.72rem;
    color: #9a9ab0;
    margin-top: 4px;
  }

  /* 위험요인 태그 */
  .risk-factors {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }
  .risk-tag-pill {
    background: #1e1e2e;
    border: 1px solid #3a3a5a;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #c0c0d8;
  }

  /* 출처 */
  .source-note {
    font-size: 0.72rem;
    color: #5a5a7a;
    font-family: 'IBM Plex Mono', monospace;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #2a2a4a;
  }

  /* 범례 */
  .legend-box {
    background: #16213e;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 16px;
    font-size: 0.8rem;
    color: #9a9ab0;
  }
  .legend-box span {
    color: #e63946;
    font-weight: 700;
  }

  /* Streamlit 요소 숨기기 */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# ── 데이터 ────────────────────────────────────────────────────────────────────
COUNTRIES = {
    "수단": {
        "en": "Sudan",
        "lat": 15.5,
        "lon": 32.5,
        "crisis": "콜레라 대유행",
        "stats": [
            {"number": "124,418명", "label": "감염자 수"},
            {"number": "3,573명",   "label": "사망자 수"},
            {"number": "2.87%",    "label": "치명률"},
        ],
        "risks": ["상하수도 붕괴", "대규모 인구 이동", "홍수", "의료 접근 제한"],
        "desc": "수단은 2024년 8월 이후 대규모 콜레라 유행이 지속되고 있습니다. 내전으로 인한 인프라 붕괴와 의료 시스템 마비가 상황을 악화시키고 있으며, 홍수와 인구 이동이 전파 속도를 높이고 있습니다.",
        "source": "WHO Sudan Cholera Update (2026-03-08) | 기간: 2024.8 ~ 2026.3",
        "color": "#e63946",
        "icon": "💊",
    },
    "DR콩고": {
        "en": "DRC",
        "lat": -4.0,
        "lon": 21.8,
        "crisis": "다중 전염병 동시 발생",
        "stats": [
            {"number": "450,000+", "label": "유행 질환 건수"},
            {"number": "8,700+명", "label": "사망자 수"},
            {"number": "5종",      "label": "동시 대응 질병"},
        ],
        "risks": ["콜레라", "mpox", "홍역", "에볼라", "폴리오"],
        "desc": "DR콩고는 WHO 2026 긴급호소 대상국으로, 콜레라·mpox·홍역·에볼라·폴리오 등 5개 이상의 전염병이 동시에 유행 중입니다. 분쟁, 극도의 빈곤, 보건 인프라 부재가 복합적으로 작용하고 있습니다.",
        "source": "WHO DRC Health Emergency Appeal 2026",
        "color": "#e63946",
        "icon": "🦠",
    },
    "남수단": {
        "en": "South Sudan",
        "lat": 6.9,
        "lon": 31.3,
        "crisis": "사상 최대 콜레라 확산",
        "stats": [
            {"number": "96,000+건", "label": "콜레라 케이스"},
            {"number": "~1,600명", "label": "사망자 수"},
            {"number": "역대 최대", "label": "규모"},
        ],
        "risks": ["홍수", "국경 유입", "취약 보건체계", "m-pox 동시 부담", "간염 E"],
        "desc": "남수단은 2025년 11월 말 기준 역대 최대 규모의 콜레라 유행을 겪고 있습니다. 홍수로 인한 인프라 피해와 국경을 통한 지속적 유입, 극도로 취약한 보건 시스템이 상황을 심화시키고 있습니다.",
        "source": "South Sudan HNRP 2026 | 기준: 2025년 11월 말",
        "color": "#e63946",
        "icon": "🌊",
    },
    "가자지구": {
        "en": "Gaza",
        "lat": 31.5,
        "lon": 34.47,
        "crisis": "전쟁·기아·감염병 위험 중첩",
        "stats": [
            {"number": "63,000+명", "label": "사망자 수"},
            {"number": "161,000+명","label": "부상자 수"},
            {"number": "극심",      "label": "기아 위기"},
        ],
        "risks": ["오염수", "하수시설 파괴", "극심한 과밀", "폐기물 축적", "낮은 예방접종률"],
        "desc": "가자지구는 지속되는 군사 충돌로 인해 의료 인프라가 거의 전멸 상태입니다. 기아, 오염수, 파괴된 하수 시스템이 감염병 대규모 확산의 직접적 위험 요인으로 작용하고 있습니다.",
        "source": "WHO Gaza PHSA (2025-09-10) | WHO EMHJ Gaza Infectious Risk Review (2025)",
        "color": "#e63946",
        "icon": "⚔️",
    },
    "아이티": {
        "en": "Haiti",
        "lat": 18.97,
        "lon": -72.3,
        "crisis": "치안붕괴 속 콜레라 재확산",
        "stats": [
            {"number": "4,864명", "label": "갱 폭력 사망 (2024.10~2025.6)"},
            {"number": "17명",    "label": "콜레라 사망 (재확산)"},
            {"number": "복합위기","label": "보건·치안 동시"},
        ],
        "risks": ["갱 폭력", "성폭력", "대규모 인구 이동", "병원 운영 중단", "불안정한 식수·위생"],
        "desc": "아이티는 갱단의 수도권 장악으로 치안이 완전히 붕괴된 가운데, 2025년 페티옹빌에서 콜레라가 재확산되고 있습니다. 병원 운영 중단과 의료진 위협으로 인도주의 접근이 극도로 어렵습니다.",
        "source": "UN 2025 / PAHO Haiti Cholera Story (2025-11) / OHCHR Haiti Violence Update (2025-07)",
        "color": "#e63946",
        "icon": "🚨",
    },
}


# ── 세션 상태 ─────────────────────────────────────────────────────────────────
if "selected" not in st.session_state:
    st.session_state.selected = None


# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="msf-header">
  <h1>🆘 MSF 활동 고위험 지역 2026</h1>
  <div class="subtitle">전염병 · 위험요소 · 사망 통계 | 출처: WHO / PAHO / OHCHR / OCHA</div>
</div>
""", unsafe_allow_html=True)


# ── 레이아웃: 지도(좌) + 사이드패널(우) ───────────────────────────────────────
col_map, col_panel = st.columns([3, 2], gap="large")

# ──────────────────── 지도 ────────────────────────────────────────────────────
with col_map:
    st.markdown("""
    <div class="legend-box">
      <span>● 빨간 마커</span> = MSF 의료 개입 필요성이 큰 복합위기 지역 &nbsp;|&nbsp;
      마커를 클릭하면 상세 정보가 오른쪽에 표시됩니다.
    </div>
    """, unsafe_allow_html=True)

    # Folium 지도 생성
    m = folium.Map(
        location=[10, 20],
        zoom_start=2,
        tiles="CartoDB dark_matter",
        prefer_canvas=True,
    )

    for name, info in COUNTRIES.items():
        # 커스텀 마커 HTML
        marker_html = f"""
        <div style="
          background:#e63946;
          border-radius:50%;
          width:36px; height:36px;
          display:flex; align-items:center; justify-content:center;
          font-size:16px;
          box-shadow: 0 0 12px rgba(230,57,70,0.8);
          border: 2px solid #fff;
          cursor:pointer;
        ">{info['icon']}</div>
        """
        icon = folium.DivIcon(html=marker_html, icon_size=(36, 36), icon_anchor=(18, 18))

        # 팝업
        popup_html = f"""
        <div style="font-family:sans-serif; background:#16213e; color:#fff; padding:14px; border-radius:8px; min-width:200px; border:1px solid #e63946;">
          <b style="font-size:1rem; color:#fff;">{name}</b><br>
          <span style="color:#e63946; font-size:0.8rem;">{info['crisis']}</span><br><br>
          {''.join(f'<span style="font-size:0.82rem; color:#ccc;">• {s["label"]}: <b style=color:#e63946>{s["number"]}</b></span><br>' for s in info['stats'])}
        </div>
        """
        popup = folium.Popup(folium.IFrame(popup_html, width=230, height=160), max_width=250)

        folium.Marker(
            location=[info["lat"], info["lon"]],
            popup=popup,
            tooltip=f"<b style='color:#e63946'>{name}</b> — {info['crisis']}",
            icon=icon,
        ).add_to(m)

    # 펄스 원 (강조)
    for name, info in COUNTRIES.items():
        folium.CircleMarker(
            location=[info["lat"], info["lon"]],
            radius=20,
            color="#e63946",
            weight=1,
            fill=True,
            fill_color="#e63946",
            fill_opacity=0.08,
        ).add_to(m)

    map_data = st_folium(m, width="100%", height=460, returned_objects=["last_object_clicked_tooltip"])

    # 지도 클릭으로 선택
    if map_data and map_data.get("last_object_clicked_tooltip"):
        tooltip_text = map_data["last_object_clicked_tooltip"]
        for name in COUNTRIES:
            if name in tooltip_text:
                st.session_state.selected = name
                break


# ──────────────────── 사이드 패널 ────────────────────────────────────────────
with col_panel:
    st.markdown("### 국가 선택")

    for name, info in COUNTRIES.items():
        stats_short = info["stats"][0]["number"] + " / " + info["stats"][1]["number"]
        if st.button(
            f"{info['icon']}  {name}  |  {info['crisis']}",
            key=f"btn_{name}",
            use_container_width=True,
        ):
            st.session_state.selected = name

    # 상세 정보 표시
    sel = st.session_state.selected
    if sel:
        info = COUNTRIES[sel]
        st.markdown("---")

        st.markdown(f"""
        <div class="detail-panel">
          <h2>{info['icon']} {sel}</h2>
          <div class="crisis-type">⚠ {info['crisis']}</div>

          <div class="stat-grid">
            {''.join(f'<div class="stat-box"><div class="number">{s["number"]}</div><div class="label">{s["label"]}</div></div>' for s in info['stats'])}
          </div>

          <p style="font-size:0.88rem; color:#c0c0d8; line-height:1.65; margin-bottom:16px;">{info['desc']}</p>

          <div style="font-size:0.78rem; color:#9a9ab0; font-weight:600; margin-bottom:8px; letter-spacing:0.5px;">주요 위험요인</div>
          <div class="risk-factors">
            {''.join(f'<span class="risk-tag-pill">{r}</span>' for r in info['risks'])}
          </div>

          <div class="source-note">📎 {info['source']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#16213e; border:1px dashed #2a2a4a; border-radius:10px; padding:32px; text-align:center; color:#5a5a7a; margin-top:8px;">
          ← 지도의 마커 또는 위 버튼을 클릭하면<br>상세 정보가 표시됩니다
        </div>
        """, unsafe_allow_html=True)


# ── 하단 출처 ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size:0.72rem; color:#5a5a7a; font-family:'IBM Plex Mono',monospace; line-height:1.7;">
📎 출처 요약: WHO Sudan Cholera Update (2026-03-08) &nbsp;|&nbsp; WHO DRC Health Emergency Appeal 2026 &nbsp;|&nbsp;
South Sudan HNRP 2026 &nbsp;|&nbsp; WHO Gaza PHSA (2025-09-10) &nbsp;|&nbsp;
WHO EMHJ Gaza Infectious Risk Review (2025) &nbsp;|&nbsp; PAHO Haiti Cholera Story (2025-11) &nbsp;|&nbsp;
OHCHR Haiti Violence Update (2025-07)
</div>
""", unsafe_allow_html=True)
