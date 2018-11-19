'use strict';

function makeTimelineChart() {

    // 自定义ECharts对象
    function timelineItem(params, api) {
        let categoryIndex = api.value(0);
        let start = api.coord([api.value(1), categoryIndex]);
        let end = api.coord([api.value(2), categoryIndex]);
        let height = api.size([0, 1])[1] * 0.6;

        let rectShape = echarts.graphic.clipRectByRect({
            x: start[0],
            y: start[1] - height / 2,
            width: end[0] - start[0],
            height: height
        }, {
            x: params.coordSys.x,
            y: params.coordSys.y,
            width: params.coordSys.width,
            height: params.coordSys.height
        });

        return rectShape && {
            type: 'rect',
            shape: rectShape,
            style: api.style()
        };
    }

    let myChart = echarts.init(document.getElementById('chart2'));
    // 显示标题，图例和空的坐标轴
    myChart.setOption({
        title: {
            text: '示例时间图'
        },
        tooltip: {
            formatter: function (params) {
                return params.marker + params.name;
            }
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                // restore : {show: true},
                // saveAsImage : {show: true}
            }
        },
        grid: {
            height: 300
        },
    });

    myChart.showLoading();    //数据加载完之前先显示一段简单的loading动画
    let data = [];
    $.ajax({
        type: "get",
        async: true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
        url: "http://127.0.0.1:5000/getTimelineData",    //请求发送到Servlet处
//       data : {},
        dataType: "json",        //返回数据形式为json
        success: function (result) {
            //请求成功时执行该函数内容，result即为服务器返回的json对象
            if (result) {
//           	alert(result["data"]);
                let data_list = result["data"];
                for (let i = 0; i < data_list.length; i++) {
                    data.push({
                        name: data_list[i]["time_range"],
                        // name: data_list[i]["type"],
                        value: [
                            data_list[i]["weekday_row"],      // row
                            data_list[i]["base_time"],    // start time
                            data_list[i]["base_time"] + data_list[i]["duration"],
                            data_list[i]["duration"]
                        ],
                        itemStyle: {
                            normal: {
                                color: data_list[i]["color"]
                            }
                        }
                    });
                }
                // alert(JSON.stringify(data));
                myChart.hideLoading();    //隐藏加载动画
                myChart.setOption({        //加载数据图表
                    title: {
                        subtext: result["date_range"],
                        left: 'center'
                    },
                    xAxis: {
                        min: 0,
                        scale: true,
                        axisLabel: {
                            formatter: function (val) {
                                console.log(val);
                                let d = new Date(val);
                                let h = d.getHours()-8;
                                let m = d.getMinutes();
                                let s = d.getSeconds();
                                return h + ':' + m + ':' + s;
                            }
                        }
                    },
                    yAxis: {
                        data: result["weekdays"]
                    },

                    series: [{
                        type: 'custom',
                        renderItem: timelineItem,
                        itemStyle: {
                            normal: {
                                opacity: 1
                            }
                        },
                        encode: {
                            x: [1, 2],
                            y: 0
                        },
                        data: data
                    }]
                });

            }

        },
        error: function (errorMsg) {
            //请求失败时执行该函数
            alert("图表请求数据失败!");
            myChart.hideLoading();
        }
    });
}

makeTimelineChart();