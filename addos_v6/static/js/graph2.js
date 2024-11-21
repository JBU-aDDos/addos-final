$(document).ready(function() {
  // 시간대별 트래픽 량 그래프
  Morris.Line({
    element: 'morris-line-chart',
    data: formattedHourlyData,
    xkey: 'hour',
    ykeys: ['count'],
    labels: ['트래픽 량'],
    parseTime: false,
    xLabelAngle: 60,
    resize: true
  });

  // 프로토콜 빈도수 원그래프
  Morris.Donut({
      element: 'morris-donut-chart',
      data: donutData,
      colors: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12'],
      resize: true,
      formatter: function (value, data) { return value + ' 패킷'; }
  });
});