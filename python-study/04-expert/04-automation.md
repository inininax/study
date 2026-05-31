# 04. 자동화 스크립트

## 🎯 학습 목표
- 파일 시스템 작업을 자동화한다
- 웹 스크래핑을 한다
- 시스템 작업을 자동화한다
- 작업 스케줄링을 한다

## 1. 파일 시스템 자동화

### 1.1 파일 정리
```python
from pathlib import Path
import shutil

def organize_by_extension(directory):
    """확장자별로 파일 분류"""
    src = Path(directory)

    for file in src.iterdir():
        if not file.is_file():
            continue

        ext = file.suffix.lstrip(".").lower() or "no_ext"
        dest_dir = src / ext
        dest_dir.mkdir(exist_ok=True)
        shutil.move(str(file), str(dest_dir / file.name))

# 사용
organize_by_extension("/Users/me/Downloads")
```

### 1.2 중복 파일 찾기
```python
import hashlib
from pathlib import Path
from collections import defaultdict

def find_duplicates(directory):
    hashes = defaultdict(list)

    for file in Path(directory).rglob("*"):
        if not file.is_file():
            continue

        h = hashlib.sha256(file.read_bytes()).hexdigest()
        hashes[h].append(file)

    return {h: files for h, files in hashes.items() if len(files) > 1}

duplicates = find_duplicates("/path/to/dir")
for h, files in duplicates.items():
    print(f"중복: {[str(f) for f in files]}")
```

### 1.3 파일 백업
```python
import shutil
from datetime import datetime
from pathlib import Path

def backup(src, dest):
    src_path = Path(src)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{src_path.name}_{timestamp}"
    backup_path = Path(dest) / backup_name

    if src_path.is_dir():
        shutil.make_archive(str(backup_path), "zip", str(src_path))
    else:
        shutil.copy2(src_path, backup_path)

    print(f"백업 완료: {backup_path}")

backup("/important/data", "/backups")
```

### 1.4 파일 이름 일괄 변경
```python
from pathlib import Path

def rename_with_prefix(directory, prefix):
    for i, file in enumerate(sorted(Path(directory).glob("*.jpg")), 1):
        new_name = f"{prefix}_{i:03d}{file.suffix}"
        file.rename(file.parent / new_name)
        print(f"{file.name} → {new_name}")

# IMG_001.jpg, IMG_002.jpg, ...
rename_with_prefix("/photos", "IMG")
```

### 1.5 파일 감시 (watchdog)
```bash
pip install watchdog
```

```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"새 파일: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"수정: {event.src_path}")

    def on_deleted(self, event):
        print(f"삭제: {event.src_path}")

observer = Observer()
observer.schedule(MyHandler(), "/path/to/watch", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

## 2. 웹 스크래핑

### 2.1 requests + BeautifulSoup
```bash
pip install requests beautifulsoup4 lxml
```

```python
import requests
from bs4 import BeautifulSoup

def scrape_titles(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # 다양한 셀렉터
    titles = soup.find_all("h2", class_="title")
    return [t.get_text(strip=True) for t in titles]

# CSS 셀렉터
def scrape_links(url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    return [a["href"] for a in soup.select("a.article-link")]

# 더 복잡한 예
def scrape_news(url):
    soup = BeautifulSoup(requests.get(url).text, "lxml")

    articles = []
    for article in soup.select("article"):
        title = article.select_one("h2").get_text(strip=True)
        date = article.select_one(".date").get_text(strip=True)
        link = article.select_one("a")["href"]
        articles.append({"title": title, "date": date, "link": link})

    return articles
```

### 2.2 세션 사용 (쿠키 유지)
```python
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# 로그인
session.post("https://example.com/login", data={
    "username": "user",
    "password": "pass",
})

# 이후 요청은 로그인 상태 유지
response = session.get("https://example.com/protected")
```

### 2.3 비동기 스크래핑
```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()

async def scrape_many(urls):
    async with aiohttp.ClientSession() as session:
        htmls = await asyncio.gather(*[fetch(session, u) for u in urls])

    results = []
    for html in htmls:
        soup = BeautifulSoup(html, "lxml")
        title = soup.title.string if soup.title else ""
        results.append(title)
    return results

urls = [f"https://example.com/page/{i}" for i in range(1, 11)]
results = asyncio.run(scrape_many(urls))
```

### 2.4 동적 페이지 (Playwright)
JavaScript 가 필요한 페이지.

```bash
pip install playwright
playwright install
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")

    # JS 실행 후 대기
    page.wait_for_selector(".dynamic-content")

    # 데이터 추출
    title = page.text_content("h1")
    links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")

    # 스크린샷
    page.screenshot(path="screenshot.png")

    browser.close()
```

### 2.5 스크래핑 매너
- ✅ `robots.txt` 확인
- ✅ 적절한 `User-Agent` 설정
- ✅ 요청 사이 `time.sleep()` (서버 부하 방지)
- ✅ 캐시 활용 (같은 URL 반복 요청 X)
- ❌ API 가 있다면 API 사용

## 3. API 자동화

### 3.1 REST API 호출
```python
import requests

# GET
response = requests.get(
    "https://api.example.com/users",
    params={"page": 1, "limit": 10},
    headers={"Authorization": "Bearer TOKEN"},
)
data = response.json()

# POST (JSON)
response = requests.post(
    "https://api.example.com/users",
    json={"name": "Alice", "email": "a@x.com"},
)

# 에러 처리
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP 에러: {e}")
except requests.exceptions.Timeout:
    print("타임아웃")
except requests.exceptions.RequestException as e:
    print(f"요청 실패: {e}")
```

### 3.2 GitHub API 예시
```python
import requests

def get_repo_stars(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers={
        "Authorization": "Bearer YOUR_TOKEN",
        "Accept": "application/vnd.github.v3+json",
    })
    response.raise_for_status()
    return response.json()["stargazers_count"]

stars = get_repo_stars("python", "cpython")
print(f"⭐ {stars:,}")
```

## 4. 시스템 자동화

### 4.1 외부 명령 실행 (subprocess)
```python
import subprocess

# 간단 실행
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)

# 셸 명령 (조심해서!)
result = subprocess.run("ls *.py | wc -l", shell=True, capture_output=True, text=True)

# 에러 시 예외
subprocess.run(["false"], check=True)  # CalledProcessError

# 실시간 출력
process = subprocess.Popen(
    ["ping", "-c", "5", "google.com"],
    stdout=subprocess.PIPE,
    text=True,
)
for line in process.stdout:
    print(line, end="")
```

### 4.2 환경 변수
```python
import os

# 읽기
db_url = os.environ.get("DATABASE_URL", "sqlite:///default.db")

# 쓰기
os.environ["MY_VAR"] = "value"

# 한 번에 (subprocess 와 함께)
subprocess.run(
    ["./script.sh"],
    env={**os.environ, "DEBUG": "1"},
)
```

### 4.3 .env 파일
```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()  # .env 로드

db_url = os.environ.get("DATABASE_URL")
api_key = os.environ.get("API_KEY")
```

## 5. 이메일 자동화

### 5.1 SMTP 로 메일 보내기
```python
import smtplib
from email.message import EmailMessage

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = "me@example.com"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("me@example.com", "app_password")
        server.send_message(msg)

send_email("alice@example.com", "안녕하세요", "테스트 메일입니다.")
```

### 5.2 첨부 파일
```python
from email.message import EmailMessage
from pathlib import Path

msg = EmailMessage()
msg["From"] = "me@example.com"
msg["To"] = "you@example.com"
msg["Subject"] = "보고서"
msg.set_content("보고서를 첨부합니다.")

# 첨부
file = Path("report.pdf")
msg.add_attachment(
    file.read_bytes(),
    maintype="application",
    subtype="pdf",
    filename=file.name,
)
```

## 6. 스케줄링

### 6.1 schedule 라이브러리 (간단)
```bash
pip install schedule
```

```python
import schedule
import time

def job():
    print("매분 실행")

def daily_report():
    print("매일 9시 실행")

schedule.every(1).minutes.do(job)
schedule.every().day.at("09:00").do(daily_report)
schedule.every().monday.at("10:30").do(lambda: print("월요일!"))

while True:
    schedule.run_pending()
    time.sleep(1)
```

### 6.2 APScheduler (강력)
```bash
pip install apscheduler
```

```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", minutes=5)
def every_5_min():
    print("5분마다")

@scheduler.scheduled_job("cron", hour=9, minute=0)
def daily_9am():
    print("매일 9시")

scheduler.start()
```

### 6.3 cron / 작업 스케줄러
시스템 레벨로 더 안정적.

```bash
# crontab -e
0 9 * * * /usr/bin/python3 /path/to/script.py
```

## 7. PDF / 엑셀 자동화

### 7.1 PDF 처리
```bash
pip install pypdf reportlab
```

```python
# PDF 읽기
from pypdf import PdfReader

reader = PdfReader("document.pdf")
print(f"페이지 수: {len(reader.pages)}")
for page in reader.pages:
    print(page.extract_text())

# PDF 합치기
from pypdf import PdfMerger
merger = PdfMerger()
merger.append("a.pdf")
merger.append("b.pdf")
merger.write("merged.pdf")
merger.close()

# PDF 생성 (reportlab)
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf")
c.drawString(100, 750, "Hello, PDF!")
c.save()
```

### 7.2 Excel 자동화
```bash
pip install openpyxl
```

```python
from openpyxl import Workbook, load_workbook

# 새 파일
wb = Workbook()
ws = wb.active
ws.title = "Data"

ws["A1"] = "이름"
ws["B1"] = "점수"
ws.append(["Alice", 95])
ws.append(["Bob", 87])

wb.save("scores.xlsx")

# 읽기
wb = load_workbook("scores.xlsx")
ws = wb["Data"]

for row in ws.iter_rows(values_only=True):
    print(row)
```

## 8. 실전 예제

### 예제 1: 다운로드 폴더 자동 정리
```python
from pathlib import Path
import shutil

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".md"],
    "videos": [".mp4", ".avi", ".mkv", ".mov"],
    "audio": [".mp3", ".wav", ".flac"],
    "archives": [".zip", ".tar", ".gz", ".rar"],
    "code": [".py", ".js", ".html", ".css", ".java"],
}

def organize(downloads):
    src = Path(downloads)

    # 카테고리별 폴더 생성
    for cat in CATEGORIES:
        (src / cat).mkdir(exist_ok=True)
    (src / "misc").mkdir(exist_ok=True)

    # 파일 분류
    for file in src.iterdir():
        if file.is_dir():
            continue

        ext = file.suffix.lower()
        for cat, exts in CATEGORIES.items():
            if ext in exts:
                shutil.move(str(file), str(src / cat / file.name))
                break
        else:
            shutil.move(str(file), str(src / "misc" / file.name))

organize("~/Downloads")
```

### 예제 2: 웹사이트 모니터링
```python
import requests
import time
from datetime import datetime

def check_site(url):
    try:
        r = requests.get(url, timeout=10)
        return r.status_code == 200
    except:
        return False

def monitor(urls, interval=300):
    while True:
        timestamp = datetime.now().isoformat()
        for url in urls:
            status = "✅" if check_site(url) else "❌"
            print(f"[{timestamp}] {status} {url}")
        time.sleep(interval)

monitor(["https://google.com", "https://github.com"])
```

### 예제 3: 일일 보고서
```python
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage

def generate_report():
    # 데이터 수집
    df = pd.read_csv("sales.csv")
    today = datetime.now().date()
    today_sales = df[pd.to_datetime(df["date"]).dt.date == today]

    # 보고서
    report = f"""
일일 매출 보고서 - {today}

총 매출: {today_sales['amount'].sum():,.0f}원
거래 건수: {len(today_sales)}
평균 거래액: {today_sales['amount'].mean():,.0f}원
"""

    # 이메일
    msg = EmailMessage()
    msg["From"] = "report@example.com"
    msg["To"] = "boss@example.com"
    msg["Subject"] = f"일일 보고서 {today}"
    msg.set_content(report)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("...", "...")
        server.send_message(msg)

    print("보고서 발송 완료")

# crontab 으로 매일 18:00 실행
```

## 📝 연습 문제

### 문제 1: 파일 정리
다운로드 폴더의 파일을 확장자별 폴더로 분류하세요.

### 문제 2: 웹 스크래퍼
뉴스 사이트에서 헤드라인 10개를 추출해 JSON 으로 저장하세요.

### 문제 3: 자동 백업
지정된 디렉토리를 매일 자정에 ZIP 으로 백업하는 스크립트를 작성하세요.

### 문제 4: 이미지 리사이즈
폴더 안 모든 이미지를 800px 이하로 리사이즈하세요. (Pillow 사용)

### 문제 5: 시간표 알림
오늘의 일정 (YAML/JSON) 을 매일 아침 9시에 이메일로 보내는 스크립트를 작성하세요.

## ✅ 체크리스트
- [ ] pathlib 으로 파일을 다룬다
- [ ] requests 로 HTTP 요청을 한다
- [ ] BeautifulSoup 으로 HTML 을 파싱한다
- [ ] subprocess 로 외부 명령을 실행한다
- [ ] schedule 또는 cron 으로 작업을 예약한다
- [ ] 이메일을 자동 발송할 수 있다

## 🔗 다음 챕터
👉 [05. 베스트 프랙티스와 코드 스타일](./05-best-practices.md)
