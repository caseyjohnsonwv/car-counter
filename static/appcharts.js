function renderMainChart() {
  selection = $("input[name=chartType]:checked").val()
  selection == 'today' ? renderTodayChart() : renderHistoryChart();
}

function renderTodayChart() {
  let ctx = $("#mainChart");
  let rawData = todayData;
  let labels = todayLabels;
  var mainChart = new Chart(ctx, {
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
      responsive: true,
      maintainAspectRatio: false,
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

function renderHistoryChart() {
  let ctx = $("#mainChart");
  let rawData = historyData;
  let labels = historyLabels;
  let mainChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: "Raw Data",
        data: rawData,
        borderColor: '#B3AB94',
        backgroundColor: '#FFFFFF00'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
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

$(document).ready(function () {
    //load the page
    $("[name=chartType]").val(["today"]);
    renderMainChart();

    //bind event listeners
    $("[name=chartType]").change(function() {
        renderMainChart();
    });
});
