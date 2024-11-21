from pymongo import MongoClient
import re
from datetime import datetime
import matplotlib.pyplot as plt

def fetcher_from_mongoDB(url, db_name, collection_name):
    client = MongoClient(url)
    db = client[db_name]
    collection = db[collection_name]

    # 데이터 읽기
    documents = collection.find()

    # 데이터 문자열로 변환
    formatted_documents = []
    for doc in documents:
        # 타임스탬프 변환
        if '@timestamp' in doc:
            timestamp_str = doc['@timestamp']
            timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            doc['@timestamp'] = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        data = str(doc)
        # 필터링
        data = re.sub(r",","\n",data)
        data = re.sub(r"'","",data)
        data = re.sub(r"{","",data)
        data = re.sub(r"}","",data)
        formatted_documents.append(doc)

    # 데이터 반환
    return formatted_documents

def group_data_by_hour(documents):
    hourly_data = {}
    for doc in documents:
        if '@timestamp' in doc:
            timestamp = doc['@timestamp']
            hour = timestamp[:13]  # 'YYYY-MM-DD HH' 형식으로 자르기
            if hour not in hourly_data:
                hourly_data[hour] = 0
            hourly_data[hour] += 1
    return hourly_data

def plot_hourly_data(hourly_data):
    hours = list(hourly_data.keys())
    counts = list(hourly_data.values())

    plt.figure(figsize=(10, 5))
    plt.plot(hours, counts, marker='o')
    plt.xlabel('Hour')
    plt.ylabel('Number of Documents')
    plt.title('Number of Documents per Hour')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#####################
####   테스트   #####
#####################
# 변수 설정
filter_data = fetcher_from_mongoDB("mongodb+srv://test:1234@cluster0.hqxzgtw.mongodb.net/network_catcher_database?retryWrites=true&w=majority&appName=Cluster0","network_catcher_database","traffic")

# 시간별 데이터 그룹화
hourly_data = group_data_by_hour(filter_data)

# 데이터 출력 테스트
for hour, count in hourly_data.items():
    print(f"{hour}: {count}")
print("Total : ", len(filter_data))

# 그래프 가시화
plot_hourly_data(hourly_data)