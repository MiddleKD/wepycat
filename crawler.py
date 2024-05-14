import time, re, os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import convert_to_webp

driver = None
def load_driver():
    global driver
    driver = webdriver.Chrome()
    print("Loaded Chrome driver.")

def kill_driver():
    driver.quit()
    print("Chrome driver Killed")

def scroll_down(driver, scroll_pause_time=0.5):
    # 현재 페이지 높이 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 현재 스크롤 위치에서 일정 부분 내리기
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(scroll_pause_time)

        # 새로운 페이지 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 페이지 높이가 변하지 않거나, 스크롤바가 아래까지 내려갔으면 스크롤 다운 종료
        if new_height == last_height or driver.execute_script("return window.innerHeight + window.pageYOffset >= document.body.offsetHeight"):
            break

        # 페이지 높이 업데이트
        last_height = new_height

def crawl_website(url, wait_time=10, scroll_pause_time=0.5):
    # Chrome 드라이버 초기화
    driver.get(url)

    # 페이지 로딩 대기
    wait = WebDriverWait(driver, wait_time)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # 페이지 맨 아래까지 스크롤 다운
    scroll_down(driver, scroll_pause_time)

    # 페이지 소스 코드 가져오기
    page_source = driver.page_source

    if "If you want this website to be available under your own domain - activate the Premium Plan." in page_source:
        print("Occured premium locking")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "body > p:nth-child(5) > a").click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        scroll_down(driver, scroll_pause_time)
        page_source = driver.page_source
    
    return page_source

def download_single(url:str, file_path):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36',
        'Referer': 'https://www.google.com/',  # 이전 페이지의 주소를 여기에 추가
        'X-Requested-With': 'XMLHttpRequest',  # AJAX 요청 여부를 나타내는 헤더
        'Accept-Language': 'en-US,en;q=0.9',  # 사용자가 선호하는 언어 설정
        'Connection': 'keep-alive',  # 서버와의 연결 유지 설정
    }

    response = requests.get(url, headers=headers)

    with open(file_path, 'wb') as f:
        f.write(response.content)

def download_file(url:str, root_http:str):

    try:
        if not url.startswith("http"):
            file_path = "." + url
            url = root_http + url
        else:
            http_pattern = r'^http.*\.com'
            match_str = re.search(http_pattern, url)[0]
            file_path = "." + url.replace(match_str, "")
        
        file_name = os.path.basename(file_path)
        dir_name = os.path.dirname(file_path)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.134 Safari/537.36',
            'Referer': 'https://www.google.com/',  # 이전 페이지의 주소를 여기에 추가
            'X-Requested-With': 'XMLHttpRequest',  # AJAX 요청 여부를 나타내는 헤더
            'Accept-Language': 'en-US,en;q=0.9',  # 사용자가 선호하는 언어 설정
            'Connection': 'keep-alive',  # 서버와의 연결 유지 설정
        }
        
        if os.path.exists(file_path):
            return file_path[1:]
        
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code != 200:
            raise Exception("Crawl Blocked")
        
        os.makedirs(dir_name, exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        ext = os.path.splitext(url)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            webp_file_path = file_path.replace(ext, ".webp")
            if os.path.exists(webp_file_path):
                return file_path[1:]
            
            convert_to_webp(response.content, output_path=webp_file_path, input_type="binary")
        
        return file_path[1:]

    except Exception as e:
        print(e, " occured while processing ", file_name)
        return url
