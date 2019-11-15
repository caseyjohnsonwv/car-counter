function renderTodayChart(rawData, labels) {
  let ctx = document.getElementById("todayChart").getContext('2d');
  let todayChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: "Raw Data",
        data: rawData,
        borderColor: '#F87060',
        backgroundColor: '#FFFFFF00'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
          }
        }]
      },
      legend: {
        display: false,
      }
    },
  });
}

$(document).ready(
  function () {
    renderTodayChart(todayData, todayLabels);
  }
);
