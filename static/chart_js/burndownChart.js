'use strict';

function makeBurndownChart() {
    let burndownChart = echarts.init(document.getElementById('chart1'));

    // 显示标题，图例和空的坐标轴
    burndownChart.setOption({
        title: {
            text: '示例燃尽图'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['测试数据']
        },
        dataZoom: [
            {
                type: 'slider',
                xAxisIndex: 0,
                filterMode: 'empty'
            },
            {
                type: 'slider',
                yAxisIndex: 0,
                filterMode: 'empty'
            },
            {
                type: 'inside',
                xAxisIndex: 0,
                filterMode: 'empty'
            },
            {
                type: 'inside',
                yAxisIndex: 0,
                filterMode: 'empty'
            }
        ],
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                magicType: {show: true, type: ['line', 'bar']},
                saveAsImage: {show: true},
                myRefresh: {
                    show: true,
                    title: '刷新数据',
                    icon: 'path://M512 0C229.230208 0 0 229.230208 0 512 0 794.769792 229.230208 1024 512 1024 761.325865 1024 973.201958 844.559514 1016.153097 601.764678 1018.151127 590.470182 1019.771663 579.089182 1021.010022 567.635639 1022.492753 553.921916 1012.577574 541.602754 998.863851 540.120021 985.150125 538.637291 972.830963 548.552469 971.348233 562.266193 970.230573 572.603369 968.768273 582.873092 966.965602 593.063262 928.217702 812.097967 736.992706 974.048781 512 974.048781 256.817504 974.048781 49.951219 767.182496 49.951219 512 49.951219 256.817504 256.817504 49.951219 512 49.951219 698.044361 49.951219 863.703281 160.916567 936.293348 328.7543 941.768939 341.414579 956.470965 347.238921 969.131243 341.763332 981.791522 336.287742 987.615863 321.585717 982.140273 308.925438 901.710383 122.961007 718.143277 0 512 0Z',
                    onclick: updateData,
                }
            }
        },
        calculable: true,

        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: []
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name: '',
                type: 'line',
                data: [],
            },]
    });

    // 整理数据
    let dates = [];    //名称数组（实际用来盛放X轴坐标值）
    let completions = [];    //数量数组（实际用来盛放Y坐标值）
    let ideals = [];
    let loss = [];
    burndownChart.showLoading();    //数据加载完之前先显示一段简单的loading动画
    function updateData() {
        // call backend function
        $.ajax({
            type: "get",
            async: true,            //异步请求（同步请求将会锁住浏览器，用户其他操作必须等待请求完成才可以执行）
            url: "http://127.0.0.1:5000/getBurndownData",    //请求发送到Servlet处
            // data : {},
            dataType: "json",        //返回数据形式为json
            success: function (result) {
                //请求成功时执行该函数内容，result即为服务器返回的json对象
                if (result) {
                    // 获取result中的数值
                    dates = result["dates"];
                    completions = result["completions"];
                    ideals = result["ideals"];
                    loss = result["loss"];
                    // 刷新图表
                    burndownChart.hideLoading();    //隐藏加载动画
                    burndownChart.setOption({        //加载数据图表
                        xAxis: {
                            data: dates
                        },
                        series: [{
                            name: '当前剩余量',
                            data: completions,
                            type: 'line',
                            symbol: 'circle',
                            smooth: true,
                            symbolSize: 3,
                            lineStyle: {
                                normal: {
                                    color: '#dc7766',
                                    width: 1,
                                    type: 'solid'
                                }
                            },
                            itemStyle: {
                                normal: {
                                    borderWidth: 2,
                                    borderColor: '#dc7766',
                                    color: '#dc7766'
                                }
                            }
                        },
                            {
                                name: '理想剩余量',
                                type: 'line',
                                smooth: true,
                                data: ideals,
                                itemStyle: {
                                    normal: {
                                        color: '#6ae68e',
                                        borderWidth: 0,
                                        areaStyle: {type: 'default'}
                                    }
                                }
                            },
                            {
                                name: '差距值',
                                type: 'bar',
                                data: loss,
                                itemStyle: {
                                    normal: {
                                        color: function (params) {
                                            if (params.value > 0) {
                                                return "#fe4d36";
                                            } else{
                                                return "#20b71e";
                                            }
                                        },
                                        borderWidth: 0,
                                    }
                                },
                                markPoint: {
                                    itemStyle: {
                                        color: "#fe4d36"
                                        },
                                    data: [
                                        {type: 'max', name: '最大值'},
                                    ]
                                },
                            }
                        ]
                    });

                }

            },
            error: function (errorMsg) {
                //请求失败时执行该函数
                alert("图表请求数据失败!");
                burndownChart.hideLoading();
            }
        });
    }

    updateData();
}

makeBurndownChart();