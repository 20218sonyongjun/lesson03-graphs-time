import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감", layout="wide")

st.title("영화 데이터 그래프 도감 1 - 시간")

# 데이터 불러오기 및 전처리 함수 (캐싱하여 속도 향상)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 8자리 숫자(예: 20230101)로 된 '날짜' 열을 실제 datetime 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

# 데이터 로드
df = load_data()

st.divider()

# ==========================================
# [구역 1] 영화별 일일 관객수 변화 (선 그래프)
# ==========================================
st.header("1. 영화별 일일 관객수 추이")

# 영화 선택 드롭다운
movie_list = df['영화명'].unique()
selected_movie = st.selectbox("그래프로 확인할 영화를 선택하세요:", movie_list)

# 선택한 영화 데이터 필터링
filtered_df = df[df['영화명'] == selected_movie]

# 플롯리 선 그래프 생성
fig1 = px.line(
    filtered_df, 
    x='날짜', 
    y='일관객', 
    title=f"'{selected_movie}' 일별 관객수 변화"
)

# 마우스 오버(Hover) 시 보여줄 정보 설정
fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x}<br><b>일관객:</b> %{y:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 인사이트 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** (이 영화의 관객 수가 가장 높았던 시기나 감소 추세 등의 분석을 이곳에 적어주세요.)")

st.divider()

# ==========================================
# [구역 2] 새로운 그래프 추가를 위한 자리
# ==========================================
st.header("2. (여기에 다음 그래프 제목을 입력하세요)")
st.write("앞으로 이 아래에 새로운 데이터 분석 그래프와 코드를 추가해 나가면 됩니다.")

# 빈 인사이트 문구 자리 
# st.info("💡 **이 그래프로 알 수 있는 것:** ")

st.divider()
