from datetime import datetime

# 원본 타임스탬프 문자열
timestamp_str = "2024-10-05T09:10:32.719053-0700"

# 1. 문자열을 datetime 객체로 변환
timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f%z")

# 2. datetime 객체를 원하는 형식의 문자열로 변환
# 예: "YYYY-MM-DD HH:MM:SS"
formatted_timestamp = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")

print(formatted_timestamp)