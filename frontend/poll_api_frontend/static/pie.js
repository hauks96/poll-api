function process_chart_data(chart_data){
    let regions = Object.keys(chart_data);
    for(let i=0; i<regions.length; i++){
        let region_name = regions[i];
        console.log(region_name);
        let region_data = chart_data[region_name];
        let container_name = 'chart-container-'+(i+1).toString();
        // Single pie chart
        console.log(region_data)
        add_chart(region_data, region_name, container_name);
    }
}

function add_chart(region_data, region_name, container_name){
    Highcharts.chart(container_name, {
        chart: {
            styledMode: true
        },

        title: {
            text: region_name
        },

        series: [{
            type: 'pie',
            allowPointSelect: true,
            keys: ['name', 'y', 'selected', 'sliced'],
            data: region_data,
            showInLegend: true
        }]
    });
}