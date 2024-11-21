from pymongo import MongoClient

# MongoDB Atlas 클러스터에 연결
client = MongoClient("mongodb+srv://test:1234@cluster0.hqxzgtw.mongodb.net/network_catcher_database?retryWrites=true&w=majority&appName=Cluster0")

# 데이터베이스 선택
db = client["network_catcher_database"]

# 컬렉션 선택
collection = db["traffic"]

# 데이터 읽기
documents = collection.find()

# 데이터 출력 예시
for document in documents:
    print(document)
