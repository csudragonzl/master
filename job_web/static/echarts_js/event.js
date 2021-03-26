

var chartDom_bar = document.getElementById('barCharts');
var barChart = echarts.init(chartDom_bar);
var option;

barChart.showLoading();

$.get('http://127.0.0.1:5000/group/group_analysis', function (data) {
    barChart.hideLoading();
    barChart.setOption({

    grid: [
        {x: '5%', y: '10%', width: '40%', height: '80%'},//图位置控制
        {x: '50%', y: '10%', width: '40%', height: '80%'}
    ],
    title: [
        {
            text: 'Group所属国家统计',
            left: '20%'
        },
        {
            text: 'Group所属类别统计',
            left: '65%'
        }
    ],
    xAxis: [
        {
            gridIndex: 0,
            type: 'category',
            data: data.country_list
        },
        {
            gridIndex: 1,
            type: 'category',
            data: data.category_list,
            axisLabel: {
                interval:0,      //坐标轴刻度标签的显示间隔(在类目轴中有效) 0:显示所有  1：隔一个显示一个 :3：隔三个显示一个...
                formatter:function(value){
                    var str = "";
                    flag = value.indexOf("&")

                    if(flag >= 0) {
                        str = value.slice(0, flag + 1) + "\n" + value.slice(flag + 1)
                        return str;
                    } else {
                        return value;
                    }
                }
            }
        }
    ],
    yAxis: [  //y轴
        {gridIndex: 0 ,},//定义y轴index
        {gridIndex: 1 ,}
    ],
    series: [
        {
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: data.country_counts_list
        },
        {
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: data.category_counts_list
        },
    ]
    });
}, 'json')

