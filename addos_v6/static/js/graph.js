document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM 로드 완료');
    // Morris 객체 확인
    console.log('Morris object:', Morris);
    function preprocessData(data) {
        const hourlyData = {};
        let latestTimestamp = 0;
      // 데이터에서 가장 최신 시간 찾기
        data.forEach(item => {
            const timestamp = new Date(item['@timestamp']).getTime();
            latestTimestamp = Math.max(latestTimestamp, timestamp);
        });
    const latestDate = new Date(latestTimestamp);  
      // 최신 시간부터 12시간 전까지 초기화
    for (let i = 0; i < 12; i++) {
        const date = new Date(latestDate - i * 60 * 60 * 1000);
        const hourKey = date.toISOString().slice(0, 13) + ':00:00.000Z';
        hourlyData[hourKey] = { time: hourKey, total: 0, TCP: 0, UDP: 0, ICMP: 0, HTTP: 0 };
    }
      // 데이터 집계
    data.forEach(item => {
        const itemDate = new Date(item['@timestamp']);
        const hourKey = itemDate.toISOString().slice(0, 13) + ':00:00.000Z';
        
        if (hourlyData[hourKey]) {
        hourlyData[hourKey].total += 1;
        hourlyData[hourKey][item.proto] += 1;
        }
    });
      // 시간 순으로 정렬된 배열로 변환
    const sortedData = Object.values(hourlyData).sort((a, b) => {
        return new Date(b.time) - new Date(a.time);
    });
    console.log('Preprocessed data:', JSON.stringify(sortedData, null, 2));
    return sortedData;
    }
    // 실제 데이터 처리
    var processedData = preprocessData(rawData);
    console.log('처리된 데이터:', processedData);
    // 트래픽 그래프 (Area Chart) 생성
    try {
    console.log('Area 차트 생성 시도');
    Morris.Area({
        element: 'morris-area-chart',
        data: processedData,
        xkey: 'time',
        ykeys: ['total'],
        labels: ['총 트래픽'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true,
        lineColors: ['#1e88e5'],
        fillOpacity: 0.5,
        xLabels: 'hour',
        xLabelFormat: function(d) {
        return new Date(d).toLocaleString('ko-KR', {hour: '2-digit', minute:'2-digit'});
        },
        dateFormat: function(x) {
            return new Date(x).toLocaleString('ko-KR');
        },
        hoverCallback: function(index, options, content, row) {
            const date = new Date(row.time);
            return "시간: " + date.toLocaleString('ko-KR') + "<br/>총 트래픽: " + row.total;
        }
    });
    console.log('트래픽 그래프 (Area Chart) 생성 완료');
    } catch (error) {
        console.error('트래픽 그래프 (Area Chart) 생성 중 오류 발생:', error);
    }
    // 프로토콜 그래프 (Line Chart) 생성
    try {
        console.log('Line 차트 생성 시도');
        Morris.Line({
        element: 'morris-line-chart',
        data: processedData,
        xkey: 'time',
        ykeys: ['TCP', 'UDP', 'ICMP', 'HTTP'],
        labels: ['TCP', 'UDP', 'ICMP', 'HTTP'],
        hideHover: 'auto',
        resize: true,
        lineColors: ['#1AB394', '#FF5733', '#FFC300', '#DAF7A6'],
        pointSize: 3,
        lineWidth: 2,
        smooth: false,
        xLabels: 'hour',
        xLabelFormat: function(d) {
            return new Date(d).toLocaleString('ko-KR', {hour: '2-digit', minute:'2-digit'});
        },
        dateFormat: function(x) {
            return new Date(x).toLocaleString('ko-KR');
        },
        hoverCallback: function(index, options, content, row) {
            const date = new Date(row.time);
            return "시간: " + date.toLocaleString('ko-KR') + "<br/>TCP: " + row.TCP + "<br/>UDP: " + row.UDP + 
                "<br/>ICMP: " + row.ICMP + "<br/>HTTP: " + row.HTTP;
        }
    });
    console.log('프로토콜 그래프 (Line Chart) 생성 완료');
    } catch (error) {
    console.error('프로토콜 그래프 (Line Chart) 생성 중 오류 발생:', error);
    }
    // 프로토콜 비율 차트 (Donut Chart) 생성
    try {
        console.log('Donut 차트 생성 시도');
        const totalCounts = processedData.reduce((acc, hour) => {
        acc.TCP += hour.TCP;
        acc.UDP += hour.UDP;
        acc.ICMP += hour.ICMP;
        acc.HTTP += hour.HTTP;
        return acc;
        }, { TCP: 0, UDP: 0, ICMP: 0, HTTP: 0 });
        const donutData = Object.entries(totalCounts).map(([key, value]) => ({
        label: key,
        value: value
    }));
    Morris.Donut({
        element: 'morris-donut-chart',
        data: donutData,
        colors: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12'],
        formatter: function (value, data) { return value + ' 패킷'; }
    });
    console.log('프로토콜 비율 차트 (Donut Chart) 생성 완료');
    } catch (error) {
        console.error('프로토콜 비율 차트 (Donut Chart) 생성 중 오류 발생:', error);
    }
    console.log('모든 차트 생성 시도 완료');
});