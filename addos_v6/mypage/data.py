from pymongo import MongoClient
import json

def get_traffic_data_to_json():
    client = MongoClient('mongodb+srv://test:1234@cluster0.hqxzgtw.mongodb.net/network_catcher_database?retryWrites=true&w=majority&appName=Cluster0","network_catcher_database","traffic')
    db = client['network_catcher_database']
    collection = db['traffic']
    
    # 데이터 가져오기
    data = list(collection.find({}, {'_id': 0, '@timestamp': 1, 'proto': 1}))  
    # JSON 형식으로 변환
    return json.dumps(data)


# 대시보드로 쓸 데이터 가져오기 추가
def get_traffic_data_for_dashboard():
    client = MongoClient('mongodb+srv://test:1234@cluster0.hqxzgtw.mongodb.net/network_catcher_database?retryWrites=true&w=majority&appName=Cluster0","network_catcher_database","traffic')
    db = client['network_catcher_database']
    collection = db['traffic']
    
    # 데이터 가져오기
    data = list(collection.find({}, {
        '_id': 0,
        'src_ip': 1,
        'bytes_toserver': 1,
        'state': 1,
        'reason': 1
    }))  
    # JSON 형식으로 변환
    return json.dumps(data)

# 수리카타로 쓸 데이터 가져오기 추가
def get_traffic_data_for_suricata():
    client = MongoClient('mongodb+srv://test:1234@cluster0.hqxzgtw.mongodb.net/network_catcher_database?retryWrites=true&w=majority&appName=Cluster0')
    db = client['network_catcher_database']
    collection = db['traffic']
    
    # Suricata 규칙 추천에 필요한 데이터 가져오기
    data = list(collection.find({}, {
        '_id': 0,
        'proto': 1,
        'src_ip': 1,
        'dest_port': 1
    }))
    
    # JSON 형식으로 변환
    return json.dumps(data)