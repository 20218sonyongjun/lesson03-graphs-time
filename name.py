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
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 영화의 관객 유입 패턴과 흥행 주기를 파악할 수 있습니다.")

st.divider()

# ==========================================
# [구역 2] 흥행 상위 5개 영화 일일 관객수 비교
# ==========================================
st.header("2. 흥행 상위 5편 관객수 추이 비교")

# 1. 영화별 전체 누적 '일관객' 합계 계산 후 상위 5개 추출
top_5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index

# 2. 상위 5개 영화 데이터만 필터링
top_5_df = df[df['영화명'].isin(top_5_movies)]

# 3. 플롯리 선 그래프 생성 (색상으로 영화 구분)
fig2 = px.line(
    top_5_df, 
    x='날짜', 
    y='일관객', 
    color='영화명', 
    title="기간 내 관객수 합계 TOP 5 영화의 일일 관객수 변화"
)

# 마우스 오버 시 정보 설정
fig2.update_traces(
    hovertemplate="<b>%{data.name}</b><br><b>날짜:</b> %{x}<br><b>일관객:</b> %{y:,}명<extra></extra>"
)

# 그래프 출력 
st.plotly_chart(fig2, use_container_width=True)

# 인사이트 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 최고 흥행작들의 관객 동원력 차이와, 같은 시기에 개봉한 경쟁작들이 서로 어떻게 영향을 주고받았는지 비교할 수 있습니다.")

st.divider()

# ==========================================
# [구역 3] 날짜별 일관객 합계 (영역 그래프)
# ==========================================
st.header("3. 극장가 전체 일관객 합계 추이")

# 1. 날짜별로 그날의 TOP 10 일관객 합계 구하기
daily_total_df = df.groupby('날짜')['일관객'].sum().reset_index()

# 2. 합계가 가장 큰 상위 3일 찾기
top_3_days = daily_total_df.nlargest(3, '일관객')

# 3. 플롯리 영역 그래프 생성
fig3 = px.area(
    daily_total_df, 
    x='날짜', 
    y='일관객', 
    title="날짜별 TOP 10 영화 일관객 합계 변화 (최다 관객 동원일 표시)"
)

# 4. 관객수가 가장 많았던 3일에 어노테이션(텍스트 마커) 추가
for index, row in top_3_days.iterrows():
    date_str = row['날짜'].strftime('%Y-%m-%d')
    fig3.add_annotation(
        x=row['날짜'],
        y=row['일관객'],
        text=f"🏆 {date_str}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        font=dict(size=12, color="red", weight="bold"),
        ax=0,
        ay=-40
    )

# 마우스 오버 시 정보 설정
fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x}<br><b>일관객 총합:</b> %{y:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 인사이트 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 1년 중 극장가에 관객이 가장 많이 몰리는 특정 시즌(명절, 연휴 등)이나 대작 개봉으로 인한 시장 전체의 파이 변화를 확인할 수 있습니다.")

st.divider()

# ==========================================
# [구역 4] 총 관객수 TOP 10 영화 (가로 막대그래프)
# ==========================================
st.header("4. 기간 내 최다 관객 동원 영화 TOP 10")

# 1. 영화별 총 일관객 합계 및 10위권 진입 날수 계산
top10_movies_summary = df.groupby('영화명').agg(
    총관객수=('일관객', 'sum'),
    진입일수=('날짜', 'count')
).reset_index()

# 2. 총관객수 기준 상위 10개 영화 선택
top10_movies_summary = top10_movies_summary.nlargest(10, '총관객수')

# 3. 관객이 많은 영화가 위에 오도록 정렬
top10_movies_summary = top10_movies_summary.sort_values(by='총관객수', ascending=True)

# 4. 가로 막대그래프 생성
fig4 = px.bar(
    top10_movies_summary,
    x='총관객수',
    y='영화명',
    orientation='h',
    custom_data=['진입일수'],
    title="기간 내 일관객 합계 TOP 10 영화"
)

# 5. 마우스 오버 시 정보 설정
fig4.update_traces(
    hovertemplate="<b>영화명:</b> %{y}<br><b>총 관객수:</b> %{x:,}명<br><b>10위권 진입 날수:</b> %{customdata[0]}일<extra></extra>"
)

fig4.update_layout(yaxis_title="영화명", xaxis_title="총 관객수 (명)")

# 그래프 출력
st.plotly_chart(fig4, use_container_width=True)

# 인사이트 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 기간 내 가장 많은 선택을 받은 대흥행작 목록과 함께, 단기간 폭발적인 관객을 모았는지 혹은 장기 흥행(롱런)을 이루어냈는지를 진입 날수를 통해 비교할 수 있습니다.")

st.divider()

# ==========================================
# [구역 5] 월x요일별 일관객 합계 히트맵
# ==========================================
st.header("5. 월×요일별 관객수 분포 (히트맵)")

# 1. 날짜에서 '월'과 '요일' 추출
heatmap_df = df.copy()
heatmap_df['월'] = heatmap_df['날짜'].dt.month.astype(str) + "월"
# day_name()으로 요일을 구한 뒤 한글로 매핑
weekday_map = {
    'Monday': '월요일', 'Tuesday': '화요일', 'Wednesday': '수요일',
    'Thursday': '목요일', 'Friday': '금요일', 'Saturday': '토요일', 'Sunday': '일요일'
}
heatmap_df['요일'] = heatmap_df['날짜'].dt.day_name().map(weekday_map)

# 2. 월 및 요일 정렬 순서 지정
month_order = [f"{i}월" for i in range(1, 13)]
weekday_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

# 3. 월×요일별 일관객 합계 피벗 테이블 생성
pivot_df = heatmap_df.pivot_table(
    index='월', 
    columns='요일', 
    values='일관객', 
    aggfunc='sum'
).reindex(index=month_order, columns=weekday_order)

# 4. 히트맵 생성 (Blues 색상 팔레트: 수치가 클수록 진한 색)
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="요일", y="월", color="관객수 합계"),
    x=weekday_order,
    y=month_order,
    color_continuous_scale="Blues",
    title="월별·요일별 극장 관객수 합계 분포"
)

# 마우스 오버 시 정보 설정
fig5.update_traces(
    hovertemplate="<b>%{y} %{x}</b><br><b>관객수 합계:</b> %{z:,}명<extra></extra>"
)

# 그래프 레이아웃 설정
fig5.update_layout(xaxis_title="요일", yaxis_title="월")

# 그래프 출력
st.plotly_chart(fig5, use_container_width=True)

# 인사이트 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 연중 어떤 달의 어떤 요일에 극장 관객 집중도가 가장 높은지(예: 여름 성수기 주말, 명절 연휴 등) 직관적으로 파악할 수 있습니다.")

st.divider()

# ==========================================
# [구역 6] 새로운 그래프 추가를 위한 자리
# ==========================================
st.header("6. (여기에 다음 그래프 제목을 입력하세요)")
st.write("앞으로 이 아래에 새로운 데이터 분석 그래프와 코드를 추가해 나가면 됩니다.")
