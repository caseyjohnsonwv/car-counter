function renderTodayChart(data, labels) {
  let ctx = document.getElementById("todayChart").getContext('2d')
  let todayChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: data,
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

function loadTodayData() {
  let data = [0, 1, 6];
  let labels = ["a","b","c"];
  return [data, labels];
}

$(document).ready(
  function () {
    values = loadTodayData();
    data = values[0];
    labels = values[1];
    renderTodayChart(data, labels)
  }
);
