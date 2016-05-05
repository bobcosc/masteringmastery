/* Project specific Javascript goes here. */
$(function () {
    $('.annie').highcharts({
        credits: {
            enabled: false
        },
        chart: {
            type: 'bar'
        },
        title: {
            text: ''
        },
       
        
        xAxis: {
            categories: ['Annie bot', 'Scarra', 'Some loser'],
            title: {
                text: null
            },
            lineWidth: 0,
            minorGridLineWidth: 0,
            lineColor: 'transparent',
            labels: {
                enabled: true
            },
            minorTickLength: 0,
            tickLength: 0
        },
        yAxis: {
            gridLineWidth: 0,
            minorGridLineWidth: 0,
            min: 0,
            title: {
                text: null,
                
            },
            labels: {
                enabled:false
            }
        },
       
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                },
                colorByPoint: true,
                colors: ["#D9A441", "#CCC2C2", "#965A38"],
            }
        },
        series: [{
            showInLegend: false,
            pointPadding: 0,
            groupPadding: 0.1,
            data: [32700030, 31100000, 16350000, ]
        }, ]

    });
});