import streamlit as st
import pandas as pd

# 데이터 불러오기
file_path = 'D:\2024\Python\cafe.xlsx'
cafe_data = pd.read_excel(file_path)

# order_date를 datetime형식으로 변환
cafe_data['order_date'] = pd.to_datetime(cafe_data['order_date'], errors='coerce')

# 결측값 제거
cafe_data = cafe_data.dropna(subset=['order_date'])

# 연도와 월 컬럼 추가
cafe_data['year'] = cafe_data['order_date'].dt.year
cafe_data['month'] = cafe_data['order_date'].dt.month

# Streamlit 대시보드 설정
st.title('카페 매출 대시보드')

# 기본 화면과 카테고리별 매출 화면 전환을 위한 변수 설정
view = st.sidebar.selectbox('보기 선택', ['기본 화면', '카테고리별 매출 계산'])

if view == '기본 화면':
    # 기본 화면: 연도와 제품 선택
    selected_year = st.sidebar.selectbox('연도 선택', sorted(cafe_data['year'].dropna().astype(int).unique()))
    selected_product = st.sidebar.selectbox('제품 선택', sorted(cafe_data['item'].unique()))

    # 선택된 연도와 제품에 따라 데이터 필터링
    filtered_data = cafe_data[(cafe_data['year'] == selected_year) & (cafe_data['item'] == selected_product)]

    # 월별 매출 데이터 계산
    monthly_sales = filtered_data.groupby('month')['price'].sum().reset_index()
    monthly_sales['month'] = monthly_sales['month'].astype(int)  # 월 데이터를 정수형으로 변환

    # 매출 표 출력
    st.write(f'{selected_year}년 {selected_product} 매출 데이터')
    st.write(filtered_data)

    # 막대 그래프 그리기
    st.write(f'{selected_year}년 {selected_product} 월별 매출')
    st.bar_chart(monthly_sales.set_index('month'))

else:
    # 카테고리별 매출 계산 화면
    st.subheader('카테고리별 매출 계산')
    
    # 전체 기간 동안의 카테고리별 매출 데이터
    total_category_sales = cafe_data.groupby('category')['price'].sum().reset_index().sort_values(by='price', ascending=False)
    st.write('전체 기간 카테고리별 매출')
    st.write(total_category_sales)
    
    # 기간별 매출 계산 입력란
    start_date = st.date_input('시작 날짜', pd.to_datetime('2017-01-01'))
    end_date = st.date_input('종료 날짜', pd.to_datetime('2017-12-31'))

    if st.button('기간별 카테고리 매출 계산'):
        period_data = cafe_data[(cafe_data['order_date'] >= pd.to_datetime(start_date)) & 
                                (cafe_data['order_date'] <= pd.to_datetime(end_date))]

        if not period_data.empty:
            category_sales = period_data.groupby('category')['price'].sum().reset_index().sort_values(by='price', ascending=False)
            st.write(f'{start_date}부터 {end_date}까지 카테고리별 매출')
            st.write(category_sales)

            most_sold_item = category_sales.iloc[0]['category']
            least_sold_item = category_sales.iloc[-1]['category']
            st.write(f'해당 기간에는 가장 많이 팔린 카테고리는 {most_sold_item}이며, 가장 적게 팔린 카테고리는 {least_sold_item}입니다.')
        else:
            st.write('해당 기간에 판매된 데이터가 없습니다.')
