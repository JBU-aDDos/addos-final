#!/bin/bash

### 수리카타 ###
# 1. 수리카타 설치
# 2. 수리카타 설정파일 및 룰 설정
# 3. 수리카타 재시작 및 enable 설정

### 파일비트 ###
# 1. 파일비트 설치
# 2. 파일비트 설정 파일 수정
# 파일비트 재시작 및 enable설정

set -e 
# Valuable
Suricata_Cf=/etc/suricata/suricata.yaml
Suricata_Rules=/etc/suricata/suricata.rules
Filebeat_Cf=/etc/filebeat/filebeat.yml

# 이메일 관련 변수
EVE_LOG=/var/log/suricata/eve.json
ALERT_THRESHOLD=1048576 # 1MB
CHECK_INTERVAL=60 # 초 단위
EMAIL="$1" # 알림을 받을 이메일 주소

# Function

WELLPLAY() {
  job="$1"
  if [ $? -eq 0 ]; then
    echo "[ OK ] $job 완료"
  else
    echo "[FAIL] $job 에 실패하였습니다. 로그를 확인해 보세요"
    exit 1
  fi
}

START() {
  SVC="$1"
  systemctl restart $SVC
  if [ $? -eq 0 ]; then
    systemctl enable $SVC
    systemctl status $SVC
  else
    echo "[FAIL] 서비스가 켜지지 않았습니다. 로그를 확인해 보세요"
    exit 1
  fi
}

send_alert() {
  if echo "많은 트래픽이 감지되었습니다. 저희 서비스를 방문해주세요" | msmtp --from=default -t "$EMAIL"; then
    echo "[ WARN ] 메일을 확인해주세요."
  else
    echo "[FAIL] 메일 발송에 실패했습니다."
  fi
}

monitor_log_size() {
  previous_size=0
  while true; do
    current_size=$(stat -c%s "$EVE_LOG")
    if [ $previous_size -gt 0 ]; then
      size_diff=$((current_size - previous_size))
      if [ $size_diff -gt $ALERT_THRESHOLD ]; then
        send_alert
      fi
    fi
    previous_size=$current_size
    sleep $CHECK_INTERVAL
  done
}

# Main
### 수리카타 ###
# 1. 수리카타 설치
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt-get update
sudo apt-get install -y -q suricata
WELLPLAY Suricata설치

# 2. 수리카타 설정파일 및 룰 설정
# fast -> disable
sed -i '85s/enabled: yes/enabled: false/' $Suricata_Cf
WELLPLAY fastlog설정

# eve.log
sed -i '94 a\
      types:\n\
        - alert\n\
        - http\n\
        - dns\n\
        - icmp\n\
        - smtp\n\
        - ssh\n\
        - fileinfo\n\
        - flow\n\
        - tls\n\
        - stats' $Suricata_Cf
WELLPLAY eve.log설정

# suricata-rules
touch $Suricata_Rules
chmod u+w $Suricata_Rules

cat << EOF > $Suricata_Rules
alert udp any any -> any 53 (msg:"Possible DNS DDoS Attack Detected"; threshold: type both, track by_src, count 100, seconds 10; flow: stateless; sid:1000004;)
alert icmp \$EXTERNAL_NET any -> \$HOME_NET any (msg:"ICMP Echo Request Flood Detected"; icmp_type:8; threshold:type:threshold, track by_src, count 100, seconds 10; classtype:attempted-dos; sid:1000001; rev:1;)
alert tcp any any -> any 80 (flags: S; flow: stateless; threshold: type both, track by_src, count 100, seconds 10; msg: "Possible Syn Flood Detected"; sid:1000001;)
alert udp any any -> any any (msg:"Possible UDP Flood Detected"; threshold: type both, track by_src, count 1000, seconds 10; sid:1000002;)
alert http any any -> any 80 (msg:"Possible HTTP Flood Detected"; flow: established; threshold: type both, track by_src, count 100, seconds 10; sid:1000003;)
EOF
WELLPLAY rules파일생성

# af-packet
sed -i 's/interface: eth0/interface: ens33/' $Suricata_Cf
WELLPLAY 네트워크인터페이스설정

# 3. 수리카타 재시작 및 enable 설정
START suricata.service
WELLPLAY 서비스시작

### 파일비트 ###
# 1. 파일비트 설치
wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.10.1-amd64.deb
sudo dpkg -i filebeat-8.10.1-amd64.deb
WELLPLAY 파일비트설치

# 2. 파일비트 설정 파일 수정
# input 설정
sed -i '/^filebeat.inputs:/a \
- type: log\
  enabled: true\
  paths:\
    - /var/log/suricata/eve.json
' $Filebeat_Cf
WELLPLAY Input설정완료

# output설정
sed -i 's/^output.elasticsearch:/# output.elasticsearch:/' $Filebeat_Cf
WELLPLAY Output.elasticsearch설정

sed -i '$a \
output.kafka:\
  hosts: ["localhost:9092"]\
  topic: "kafka"\
  partition.round_robin:\
    reachable_only: false\
  required_acks: 1' $Filebeat_Cf
WELLPLAY kafka연결

# 파일비트 재시작 및 enable설정
START filebeat.service
WELLPLAY 서비스시작

############ Mail Service ############

# msmtp 설치
sudo apt-get install -y -q msmtp
WELLPLAY msmtp설치

# 설정파일 아이디 등록
cat << EOF > ~/.msmtprc
# Gmail SMTP 설정
account default
host smtp.gmail.com
port 587
from aDDOSalarm@gmail.com
auth on
user aDDOSalarm@gmail.com
password gooz kpfn mgni wrem
tls on
tls_starttls on
tls_certcheck off
logfile ~/.msmtp.log
EOF
WELLPLAY 설정완료

# 권한주기 
chmod 600 ~/.msmtprc

# 이메일 알림 모니터링 시작
monitor_log_size &
WELLPLAY 메일서비스
