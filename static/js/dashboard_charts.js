
// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var area = document.getElementById("barChart");
var doughnut = document.getElementById("doughnutChart")


let setupLinearChart = async (labels, data) => {
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: "tasks done ",
                lineTension: 0.3,
                backgroundColor: "rgba(78, 115, 223, 0.05)",
                borderColor: "rgb(244,98,58)",
                pointRadius: 3,
                pointBackgroundColor: "rgb(16,16,19)",
                pointBorderColor: "rgb(16,16,19)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "rgb(16,16,19)",
                pointHoverBorderColor: "rgb(16,16,19)",
                pointHitRadius: 10,
                pointBorderWidth: 2,
                data: data,
            }],
        },

        options: {

            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 7
                    }

                }],
                yAxes: [{
                    ticks: {

                        maxTicksLimit: 5,
                        padding: 10,
                        beginAtZero: true,

                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
            },


            legend: {
                position: 'top',
            },
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                intersect: false,
                mode: 'index',
                caretPadding: 10,
                callbacks: {
                    label: function (tooltipItem, chart) {
                        var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                        return datasetLabel + '' + number_format(tooltipItem.yLabel);
                    }
                }
            }
        }
    });

}


let setupBarChart = async (labels, spent_time) => {


    var BarChart = new Chart(area, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [

                {
                    label: "hours spent ",
                    data: spent_time,
                    borderColor: "rgb(0,255,255)",
                    backgroundColor: "rgb(0,255,255)",
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Bar Chart'
                }
            }
        },
    });


}


let setupDoughnutChart = async (titles, hours) => {
    var DoughnutChart = new Chart(doughnut, {
        type: 'doughnut',
        data: {
            labels: titles,
            datasets: [

                {
                    label: "dataset 1",
                    data: hours,
                    backgroundColor: Object.values(Utils.CHART_COLORS),
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Doughnut Chart'
                }
            }
        }
    });


}

