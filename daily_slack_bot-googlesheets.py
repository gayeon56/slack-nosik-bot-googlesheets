import os
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 환경변수에서 Slack 토큰과 채널 ID 불러오기
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]

# Google Sheets API 인증 설정
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# credentials.json 파일로 인증
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 시트 열기
sheet = client.open("노식 슬랙봇 메시지").sheet1

# A열 메시지 불러오기 (1행은 헤더이므로 제외)
messages = sheet.col_values(1)[1:]

# 슬랙 클라이언트 초기화
slack_client = WebClient(token=SLACK_TOKEN)

def send_random_message():
    if not messages:
        print("⚠️ 메시지 없음")
        return

    message = random.choice(messages)
    try:
        slack_client.chat_postMessage(channel=CHANNEL_ID, text=message)
        print(f"✅ 메시지 전송됨: {message}")
    except SlackApiError as e:
        print(f"❌ 슬랙 오류 발생: {e.response['error']}")

# 실행
send_random_message()
