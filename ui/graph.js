var lastCharts = {};

let source_ids = [
    'cnn',
    'fox-news',
    'abc-news',
    'cbc-news',
    'the-hill',
    'the-new-york-times',
    'politico',
    'associated-press',
    'msnbc',
    'the-washington-post',
    'reuters',
    'breitbart-news'
]


var parse_dataset = (timeline, datatype) => {
    var results = [];
    for(date_str in timeline) {
        let subjectivity = timeline[date_str][datatype];
        let date_components = date_str.split(':');
        let year = date_components[0];
        let month = date_components[1];
        let day = date_components[2];
        let date = new Date(year, month, day);
        results.push({
            'x': date,
            'y': subjectivity
        });
    }
    return results;
};

var plotChart = (timelines, datatype) => {
    console.log("chart")
    if(datatype in lastCharts) {
        lastCharts[datatype].destroy();
    }

    let datasets = timelines.map((timeline) => {
        let dataset = parse_dataset(timeline['data'], datatype);
        let random_color = "#"+((1<<24)*Math.random()|0).toString(16);
        return {
            data: dataset,
            label: timeline['source'],
            fill: false,
            borderColor: random_color, // random
            backgroundColor: random_color // for legend labels
        };
    });
    let chartId = `${datatype}-chart`;

    var chartContext = document.getElementById(chartId).getContext('2d');
    var lineChart = new Chart(chartContext, {
        type: 'line',
        data: {
            // labels: [chart_data['dates']],
            datasets: datasets
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                }]
            },
            legend: {
                labels: {
                    fontColor: 'black'
                }
            }
        }
    });
    lastCharts[datatype] = lineChart;
}

for(var i=0;i<source_ids.length;i++) {
    timelines = [];
    fetchData('trump', source_ids[i], timeline => {
        timelines.push(timeline);
        if(timelines.length == source_ids.length) {
            plotChart(timelines, 'subjectivity');
            plotChart(timelines, 'polarity');
        }
    });

}
