from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SuricataRuleForm, TrafficForm
from pymongo import MongoClient
import plotly.express as px
import pandas as pd
import json
from .data import get_traffic_data_to_json
from .data import get_traffic_data_for_dashboard
from .data import get_traffic_data_for_suricata
#from .data import fetch_traffic_data, group_data_by_hour

# 대시보드 데이터 계산 추가
def get_dashboard_data():
    # JSON 데이터 가져오기
    traffic_data = json.loads(get_traffic_data_for_dashboard())

    # 총 트래픽 계산
    total_traffic = sum(item.get('bytes_toserver', 0) or 0 for item in traffic_data)

    # 평균 패킷 크기 계산
    avg_packet_size = int(total_traffic / len(traffic_data) if traffic_data else 0)

    # 비정상 세션 수 계산
    abnormal_sessions = sum(1 for item in traffic_data if item.get('state') == 'closed' and item.get('reason') == 'timeout')

    # 가장 많은 트래픽 발생 IP
    top_src_ip = max(traffic_data, key=lambda x: x.get('bytes_toserver', 0) or 0).get('src_ip') if traffic_data else None

    return {
        'total_traffic': total_traffic,
        'avg_packet_size': avg_packet_size,
        'abnormal_sessions': abnormal_sessions,
        'top_src_ip': top_src_ip
    }


# 추천 Suricata 규칙 계산 추가
def recommend_suricata_rules():
    # JSON 데이터 가져오기
    traffic_data = json.loads(get_traffic_data_for_suricata())

    # 프로토콜과 IP의 발생 빈도를 계산
    protocol_count = {}
    ip_count = {}

    for item in traffic_data:
        proto = item['proto']
        src_ip = item['src_ip']

        if proto in protocol_count:
            protocol_count[proto] += 1
        else:
            protocol_count[proto] = 1

        if src_ip in ip_count:
            ip_count[src_ip] += 1
        else:
            ip_count[src_ip] = 1

    # 가장 많이 발생한 프로토콜과 IP 추출
    top_protocol = max(protocol_count, key=protocol_count.get) if protocol_count else None
    top_src_ip = max(ip_count, key=ip_count.get) if ip_count else None

    # Suricata 규칙 생성
    rule = {
        'name': 'Drop High Traffic',
        'description': f'Drop traffic from {top_src_ip}',
        'content': f'drop {top_protocol} {top_src_ip} any -> YOUR_SERVER_IP any (msg:"Drop traffic from {top_src_ip}"; sid:NEXT_SID;)'
    }

    return [rule]


def profile(request):
    return render(request, 'mypage/profile.html')

# 데시보드 데이터와 수리카타 규칙 데이터 보내기 추가
def get_traffic_data(request):
    # JSON 데이터 가져오기
    traffic_data_json = json.loads(get_traffic_data_to_json())
    dashboard_data = get_dashboard_data()  # 대시보드 데이터 가져오기
    suricata_rules = recommend_suricata_rules()  # Suricata 규칙 추천

    context = {
        'traffic_data': json.dumps(traffic_data_json),
        'total_traffic': dashboard_data['total_traffic'], # 총 트래픽
        'avg_packet_size': dashboard_data['avg_packet_size'], # 평균 패킷 크기
        'abnormal_sessions': dashboard_data['abnormal_sessions'], # 비정상 세션 수
        'top_src_ip': dashboard_data['top_src_ip'], # 가장 많은 트래픽 발생 IP
        'suricata_rules': suricata_rules,  # Suricata 규칙 추가
    }

    return render(request, 'mypage/traffic.html', context)

def suricata(request):
    if request.method == 'POST':
        form = SuricataRuleForm(request.POST)
        if form.is_valid():
            rule = form.cleaned_data['rule']
            # Suricata 룰을 처리하는 로직을 여기에 추가합니다.
            # 예: 파일에 저장하거나, Suricata API를 호출하는 등
            return HttpResponse("룰이 성공적으로 저장되었습니다.")
    else:
        form = SuricataRuleForm()
    return render(request, 'mypage/suricata.html', {'form': form})
