# 파일: flight_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time

def get_flight_count():
    # 1. 브라우저 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # 2. 드라이버 실행 및 페이지 접속
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    url = "https://www.airport.kr/ap_ko/869/subview.do"
    driver.get(url)
    time.sleep(2)

    # 3. 날짜 선택
    today = datetime.now()
    weekday_map = {'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목', 'Fri': '금', 'Sat': '토', 'Sun': '일'}
    weekday_kor = weekday_map[today.strftime('%a')]
    today_str = today.strftime(f"%Y.%m.%d ({weekday_kor})")

    date_select = Select(driver.find_element(By.ID, "daySel"))
    date_select.select_by_visible_text(today_str)

    # 4. 터미널 T2 선택
    terminal_select = Select(driver.find_element(By.ID, "termId"))
    terminal_select.select_by_visible_text("T2")

    # 5. 시간 선택
    Select(driver.find_element(By.ID, "fromTime")).select_by_visible_text("00:00")
    Select(driver.find_element(By.ID, "toTime")).select_by_visible_text("23:59")

    time.sleep(1)

    # 6. 검색 버튼 클릭 (JS 실행)
    try:
        # 버튼 존재 먼저 확인
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.button.col9 > button.btn-search"))
        )
        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button.col9 > button.btn-search"))
        )
        driver.execute_script("arguments[0].click();", search_btn)
        time.sleep(3)
    except Exception as e:
        print("❌ 검색 버튼 클릭 실패:", e)
        driver.save_screenshot("search_button_error.png")
        driver.quit()
        raise e  # 스트림릿에도 에러 보여지게 함


    # 7. 스크롤 다운 (더 많은 항공편 로딩)
    body = driver.find_element(By.TAG_NAME, "body")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(30):
        body.send_keys(Keys.END)
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 8. HTML 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")
    flight_blocks = soup.select("button.toggle")

    # 9. 중복 제거 (출발시간, 목적지, 게이트 기준)
    unique_flights = set()
    for block in flight_blocks:
        try:
            dep_time = block.select_one("div.time > strong").text.strip()
            destination = block.select_one("div.location > em").text.strip()
            gate = block.select_one("div.enter > em").text.strip()
            flight_key = (dep_time, destination, gate)
            unique_flights.add(flight_key)
        except:
            continue

    driver.quit()
    return len(flight_blocks), len(unique_flights)