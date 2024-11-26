import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Streamlit UI 시작
st.title("유망한 21세 이하 축구 선수 크롤러")
st.write("Sofascore에서 데이터를 크롤링하고 잠재력을 분석합니다.")

# 사용자 입력
position = st.text_input("포지션 입력 (예: 공격수)", "")
max_age = st.slider("최대 나이 설정", 15, 21, 21)
start_crawl = st.button("크롤링 시작")

# 크롤링 함수
def fetch_player_profiles(position, max_age):
    st.info("크롤링을 시작합니다. 잠시만 기다려주세요...")

    # ChromeDriver 설정 (헤드리스 모드)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # UI 없이 실행
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 문제 방지
    chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 문제 방지
    chrome_options.add_argument("--disable-gpu")  # GPU 사용 안함
    chrome_options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 설정

    # WebDriverManager로 경로를 자동으로 설정하는 대신, chromedriver 경로를 직접 지정
    chromedriver_path = "/usr/local/bin/chromedriver"  # 예시로 경로를 지정, 실제 경로 확인 필요

    # ChromeDriver 경로를 명시적으로 지정하여 WebDriver 실행
    driver = webdriver.Chrome(
        service=Service(chromedriver_path),  # chromedriver 경로를 명시적으로 설정
        options=chrome_options
    )

    try:
        # Sofascore 페이지 열기
        url = "https://www.sofascore.com"
        driver.get(url)
        time.sleep(5)  # 페이지 로드 대기

        # 크롤링 로직 (예: 선수 정보 가져오기 - 위치는 Sofascore의 구조에 따라 수정 필요)
        players_data = []
        for i in range(1, 11):  # 예: 첫 10개의 선수만
            player_name = f"Player {i}"  # Sofascore에서 실제 요소를 크롤링하도록 수정
            age = 18 + i  # Sofascore에서 실제 요소를 크롤링하도록 수정
            team = "Team X"  # Sofascore에서 실제 요소를 크롤링하도록 수정
            nationality = "Country Y"  # Sofascore에서 실제 요소를 크롤링하도록 수정
            potential = 100 + i * 2  # 잠재력 계산 로직 (예시)

            if age <= max_age:
                players_data.append({
                    "이름": player_name,
                    "나이": age,
                    "소속팀": team,
                    "국적": nationality,
                    "잠재력": potential,
                })

        st.success("크롤링이 완료되었습니다.")
        return pd.DataFrame(players_data)
    finally:
        driver.quit()

# 버튼이 눌렸을 때 크롤링 실행
if start_crawl and position:
    df = fetch_player_profiles(position, max_age)
    st.dataframe(df)

    # 엑셀 파일 다운로드 링크 생성
    @st.cache_data
    def convert_df_to_excel(df):
        return df.to_csv(index=False).encode('utf-8')

    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="엑셀 파일 다운로드",
        data=excel_data,
        file_name="u21_players.csv",
        mime="text/csv",
    )
