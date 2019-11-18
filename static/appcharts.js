function renderMainChart(type) {
  let ctx = document.getElementById("mainChart").getContext('2d');
  if (type == 'today') {
    let rawData = todayData;
    let labels = todayLabels;
    let mainChart = new Chart(ctx, {
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
  else {
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
}

$(document).ready(function () {
    //load the page
    $("[name=chartType]").val(["today"]);
    renderMainChart('today');

    //bind event listeners
    $("[name=chartType]").change(function() {
        selection = $("input[name=chartType]:checked").val();
        renderMainChart(selection);
    });
});
