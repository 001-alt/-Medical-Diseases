<template>
  <div class="home">
    <transition name="fade" mode="out-in">
      <dv-loading v-if="!config4.data.length">Loading...</dv-loading>
      <dv-border-box-10>
        <div class="naca">
          <div class="index-header" style="margin-top: 5px">
            <div>
              <dv-decoration-10 style="width: 450px; height: 1px; margin-bottom: 45px" />
              <dv-decoration-8 style="width: 180px; height: 50px" :color="['#568aea', '#000000']" />
              <div style="
                  width: 150px;
                  color: #eeecec;
                  font-size: 18px;
                  padding: 0 15px;
                  font-weight: bold;
                ">
                可视化平台
              </div>
              <dv-decoration-8 :reverse="true" style="width: 180px; height: 50px" :color="['#568aea', '#000000']" />
              <dv-decoration-10 style="
                  width: 450px;
                  height: 1px;
                  transform: rotateY(180deg);
                  margin-bottom: 45px;
                " />
            </div>
            <dv-decoration-5 style="width: 10%; height: 20px" :color="['#568aea', '#000000']" />
          </div>

          <div class="index-content">
            <div class="left">
              <div class="left-1">
                <dv-border-box-12>
                  <div style="padding: 5px">
                    <div class="title" style="margin-top: 15px">
                      各年龄段患病占比
                    </div>
                    <div ref="firstMain" style="width: 100%; height: 160px"></div>
                  </div>
                </dv-border-box-12>
                <dv-border-box-8>
                  <div style="padding: 5px;padding-bottom:30px">
                    <div class="title" style="margin-top: 1px">疾病类型分布</div>
                    <dv-capsule-chart :config="config1" style="width: 80%; height: 160px" />
                  </div>
                </dv-border-box-8>

                <dv-border-box-11>
                  <div style="padding: 15px">
                    <div class="title" style="margin-top: 5px">病例列表</div>
                    <div class="row_list">
                      <ul class="cases_list" style="width: 100%; height: 180px; overflow: auto">
                        <li style="font-size:15px">
                          <div>编号</div>
                          <div>求诊类型</div>
                          <div>性别</div>
                          <div>年龄</div>
                          <div>身高</div>
                          <div>体重</div>
                          <div>患病时长</div>
                        </li>
                        <li v-for="caseItem in casesData" :key="caseItem.id">
                          <div>{{ caseItem[0] }}</div>
                          <div>{{ caseItem[1] }}</div>
                          <div>{{ caseItem[2] }}</div>
                          <div>{{ caseItem[3] }}</div>
                          <div>{{ caseItem[10] }}</div>
                          <div>{{ caseItem[11] }}</div>
                          <div>{{ caseItem[12] }}</div>
                        </li>

                      </ul>
                    </div>
                  </div>
                </dv-border-box-11>
              </div>
            </div>

            <div class="cents">
              <div class="above">
                <div class="aboveOne">
                  <div style="padding: 15px">
                    <div class="title">疾病数据信息</div>
                    <div style="
                        display: flex;
                        flex-direction: column;
                        width: 100%;
                        height: 160px;
                        color: #eeecec;
                      ">
                      <div style="display: flex; flex: 1">
                        <dv-decoration-11 style="height:60px;text-align:center">
                          <div style="flex:1">数据数量: {{ centerData.maxNum }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height:60px;text-align:center">
                          <div style="flex:1">最多疾病类型: {{ centerData.maxType }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height:60px;text-align:center">
                          <div style="flex:1">求诊最多科室: {{ centerData.maxDep }}</div>
                        </dv-decoration-11>
                      </div>
                      <div style="display: flex; flex: 1">
                        <dv-decoration-11 style="height:60px;text-align:center">
                          <div style="flex:1">最大患者年龄: {{ centerData.maxAge }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height:60px;text-align:center">
                          <div style="flex:1">最小患者年龄: {{ centerData.minAge }}</div>
                        </dv-decoration-11>
                        <dv-decoration-11 style="height:60px;text-align:center">
                          <div style="flex:1">热门医院: {{ centerData.maxHos }}</div>
                        </dv-decoration-11>
                      </div>
                    </div>
                  </div>
                  <div style="padding: 15px">
                    <div class="title" style="margin-top: -30px">男女性别患病比</div>
                    <div class="content">
                      <dv-active-ring-chart :config="config2" style="width:140px;height:180px" />
                      <dv-water-level-pond :config="config4" style="width:180px;height:200px" />
                      <dv-active-ring-chart :config="config3" style="width:140px;height:180px" />
                    </div>
                  </div>
                </div>

                <div class="aboveTwo">
                  <dv-border-box-9 :color="['#568aea', '#000000']">
                    <div style="padding: 15px">
                      <div class="title" style="margin-top: 5px">医院科室环形图</div>
                      <div id="secondMain" ref="secondMain" style="width: 100%; height: 160px"></div>
                    </div>
                  </dv-border-box-9>
                  <dv-border-box-1>
                    <div style="padding: 5px">
                      <div class="title" style="margin-top: 5px">疾病关键词云图</div>
                      <div ref="thirdMain" style="width: 400px; height: 160px"></div>
                    </div>
                  </dv-border-box-1>
                </div>
              </div>

              <div class="below">
                <dv-border-box-13>
                  <div style="padding: 7px">
                    <div class="title" style="margin-top: 5px">患病身高体重平均数图</div>
                    <div ref="lastMain" style="width: 100%; height: 240px; margin-top: 25px"></div>
                  </div>
                </dv-border-box-13>
              </div>
            </div>
          </div>
        </div>
      </dv-border-box-10>
    </transition>
  </div>
</template>

<script>
import $ from "jquery";
import LeftTop from "@/components/LeftTop.vue";
import * as echarts from 'echarts';
import { WordCloudChart } from 'echarts'

export default {
  name: "Index",
  data() {
    return {
      currentIndex: 0,
      pieData: [],
      casesData: [],
      centerData: {
        maxNum: "",
        maxType: "",
        maxDep: "",
        maxHos: "",
        maxAge: "",
        minAge: "",
      },
      wordData: "",
      circleData: "", // 初始化为空数组
      lastData: {},
      config1: {},
      config2: {
        lineWidth: 20,
        radius: "50%",
        activeRadius: "60%",
        activeTime: 2000,
        digitalFlopStyle: {
          fontSize: 13,
        },
        data: [],
      },
      config3: {
        lineWidth: 20,
        radius: "50%",
        activeRadius: "60%",
        activeTime: 1500,
        digitalFlopStyle: {
          fontSize: 13,
        },
        data: [],
      },
      config4: {
        data: [],
        shape: "roundRect",
      },
    };
  },
  methods: {
    setPieData() {
      const chartDom = this.$refs.firstMain;
      const myChart = this.$echarts.init(chartDom);
      myChart.dispatchAction({
        type: "downplay",
        seriesIndex: 0,
        dataIndex: this.currentIndex,
      });
      this.currentIndex = (this.currentIndex + 1) % this.pieData.length;
      myChart.dispatchAction({
        type: "highlight",
        seriesIndex: 0,
        dataIndex: this.currentIndex,
      });

      const option = {
        tooltip: {
          trigger: 'item',
          formatter: "{a}<br/>:{c}({d}%)",
        },
        toolbox: {
          show: true,
        },
        legend: {
          orient: 'vertical',
          icon: 'circle',
          left: 0,
          data: this.pieData.map((item) => item.name),
          textStyle: {
            color: "#fff",
          },
        },
        series: [
          {
            name: '患病年龄占比',
            type: 'pie',
            radius: [20, 50],
            roseType: "area",
            center: ["50%", "55%"],
            label: {
              show: true,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                label: {
                  show: true,
                  fontWeight: "bold",
                },
              },
            },
            data: this.pieData,
          },
        ],
      };
      myChart.setOption(option);
    },
    changeData(x) {
      const st = x[0];
      for (let i = 0; i < x.length - 1; i++) {
        x[i] = x[i + 1];
      }
      x[x.length - 1] = st;
    },
    getSeriesData() {
      const series = [];
      this.circleData.forEach((item, index) => {
        if (index < 5) {
          series.push({
            name: item.name,
            type: "pie",
            clockWise: false,
            hoverAnimation: false,
            radius: [73 - index * 15 + "%", 68 - index * 15 + "%"],
            center: ["50%", "50%"],
            label: {
              show: false,
            },
            data: [
              {
                value: item.value,
                name: item.name,
              },
              {
                value: 3,
                itemStyle: {
                  color: "rgba(0,0,0,0)",
                  borderWidth: 0,
                },
                tooltip: {
                  show: false,
                },
                hoverAnimation: false,
              },
            ],
          });
        }
      });
      return series;
    },
    randomColor() {
      const r = Math.floor(Math.random() * 255);
      const g = Math.floor(Math.random() * 255);
      const b = Math.floor(Math.random() * 255);
      return `rgb(${r},${g},${b})`;
    },
    setWordData() {
      var chartDom = this.$refs.thirdMain;
      var myChart = this.$echarts.init(chartDom)
      var option = {
        series: {
          type: "wordCloud",
          sizeRange: [20, 30], // 修正拼写
          gridSize: 0,
          rotationRange: [0, 0],
          layoutAnimation: true,
          textStyle: {
            color: this.randomColor() // 调用方法
          },
          emphasis: {
            textStyle: {
              fontWeight: "bold",
              color: "#fff",
            },
          },
          data: this.wordData
        },
      };
      myChart.setOption(option);
    },
    setCircleData() {
      $(document).ready(() => {
        var newData = this.circleData
        this.changeData(newData)
        this.circleData = newData;
        var chartDom = document.getElementById("secondMain")
        var myChart = this.$echarts.init(chartDom)
        var option = {
          legend: {
            show: true,
            icon: "circle",
            top: "8%",
            left: "10%",
            data: this.circleData.map((item) => item.name),
            width: -5,
            itemWidth: 10,
            itemHight: 10,
            itemGap: 6,
            textStyle: {
              fontSize: 12,
              lineHeight: 5,
              color: "#ffffff"
            },
          },
          tooltip: {
            show: true,
            trigger: "item",
            formatter: "{b}<br>{c}({d}%)",
          },
          yAxis: [
            {
              type: "category",
              inverse: true,
              axisLine: {
                show: false,
              },
            },
          ],
          xAxis: [
            {
              show: true,
            },
          ],
          series: this.getSeriesData()
        };
        myChart.setOption(option);
      });
    },
    setLastData() {
      $(document).ready(() => {
        var newData = this.lastData;
        this.changeData(newData.xData);
        this.changeData(newData.y1Data);
        this.changeData(newData.y2Data);
        this.lastData = newData;

        var chartDom = this.$refs.lastMain;
        var myChart = this.$echarts.init(chartDom);

        var option = {
          tooltip: {
            trigger: "axis",
            backgroundColor: "rgba(255,255,255,0.1)",
            axisPointer: {
              type: "shadow",
              label: {
                show: true,
                backgroundColor: "#7B7DDC",
              },
            },
          },
          dataZoom: [
            {
              type: "slider",
              start: 0,
              end: 80,
              show: false,
            },
          ],
          legend: {
            data: ["身高", "体重"],
            textStyle: {
              color: "#B4B4B4",
            },
            top: "0%",
          },
          grid: {
            x: "8%",
            width: "85%",
            height: "81%",
            y: "4%",
          },
          xAxis: {
            data: this.lastData.xData, // 确保使用 lastData 的 xData
            axisLine: {
              lineStyle: {
                color: "#B4B4B4",
              },
            },
            axisLabel: {
              show: true,
              interval: 0,
            },
            axisTick: {
              show: false,
            },
          },
          yAxis: [
            {
              splitLine: { show: false },
              axisLine: {
                lineStyle: {
                  color: "#B4B4B4",
                },
              },
              axisLabel: {
                formatter: "{value}",
              },
            },
            {
              splitLine: { show: false },
              axisLine: {
                lineStyle: {
                  color: "#B4B4B4",
                },
              },
              axisLabel: {
                formatter: "{value}",
              },
            },
          ],
          series: [
            {
              name: "身高",
              type: "line",
              smooth: true,
              showAllSymbol: true,
              symbol: "emptyCircle",
              symbolSize: 8,
              yAxisIndex: 1,
              itemStyle: {
                normal: {
                  barBorderRadius: 5,
                  color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: "#5C4033" },
                    { offset: 1, color: "#FAEBD7" },
                  ]),
                },
              },
              data: this.lastData.y1Data,
            },
            {
              name: "体重",
              type: "bar",
              barWidth: "60%",
              itemStyle: {
                normal: {
                  barBorderRadius: 5,
                  color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: "#082e53" },
                    { offset: 1, color: "white" },
                  ]),
                },
              },
              data: this.lastData.y2Data,
            },
          ],
        };

        option && myChart.setOption(option);
      });
    },

    setConfig1() {
      const newData = this.config1.data;
      this.changeData(newData);
      this.config1 = {
        data: newData,
        showValue: true,
      };
    },
  },
  async created() {
    setInterval(() => {
      this.setPieData();
      this.setConfig1();
      this.setWordData();
    }, 2000);
    setInterval(() => {
      this.setCircleData();
    }, 2000);
    setInterval(() => {
      this.setLastData();
    }, 2000);
  },
  async mounted() {
    const res = await this.$http.get("/getHomeData");
    this.pieData = res.data.pieData;
    this.config1.data = res.data.configOne;
    this.casesData = res.data.casesData;
    this.centerData = {
      maxNum: res.data.maxNum,
      maxType: res.data.maxType,
      maxDep: res.data.maxDep,
      maxHos: res.data.maxHos,
      maxAge: res.data.maxAge,
      minAge: res.data.minAge,
    };
    this.circleData = res.data.circleData;
    this.wordData = res.data.wordData;
    this.lastData = res.data.lastData;
    this.config2.data = res.data.boyList;
    this.config3.data = res.data.girlList;
    this.config4.data = res.data.ratioData;
    console.log(this.lastData)

  },
  components: {
    LeftTop,
  },
};
</script>


<style lang="less" scoped>
.loading {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.cent-1-content {
  padding: 20px;
  display: flex;
}

.right-content {
  margin-left: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.right-content div {
  display: flex;
  font-size: 15px;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.cents {
  display: flex;
  flex-direction: column;
}

.above {
  display: flex;
}

.aboveOne {
  display: flex;
  flex-direction: column;
}

.aboveTwo {
  display: flex;
  flex-direction: column;
}

.cent {
  width: 850px;
  height: 300px;
}

.cent-1 {
  margin: 10px;
  color: aliceblue;
  width: 500px;
  height: 220px;
  /* background-color: rgb(26, 26, 133); */
}

.left {
  display: flex;
  flex-direction: column;
}

.left-1 {
  margin: 15px;
  color: aliceblue;
  width: 550px;
  display: flex;
  flex-direction: column;
}

.left-2 {
  margin: 15px;
  color: aliceblue;
  width: 530px;
  display: flex;
  flex-direction: column;
}

.naca {
  /* padding: 35px 15px 0 15px; */
  box-sizing: border-box;
  width: 100%;
  height: 820px;
  /* 默认高度 */
  display: flex;
  flex-direction: column;
}

@media (max-width: 1200px) {
  .naca {
    height: 600px;
    /* 中等屏幕高度 */
  }
}

@media (max-width: 768px) {
  .naca {
    height: 400px;
    /* 小屏幕高度 */
  }
}

@media (max-width: 480px) {
  .naca {
    height: 300px;
    /* 超小屏幕高度 */
  }
}

.naca .index-header {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.naca .index-header div {
  display: flex;
  justify-content: center;
  align-items: center;
}

.naca .index-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

.bg {
  width: 100%;
  height: 45rem;
  background-color: black;
  position: relative;
}

.title {
  color: #3f96a5;
  font-size: 18px;
  margin-top: -20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;
}

.content {
  display: flex;
  align-items: center;
}

.content-word {
  width: 140px;
  height: 130px;
  background: #11193e;
  border-radius: 40px;
  border: 1px solid #3d3d3d;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.content-word-item {
  margin-left: 19px;
  margin-bottom: 10px;

  img {
    width: 20px;
    height: 20px;
  }
}

.content-word-item-title {
  font-size: 18px;
}

.content-word-item-content {
  margin-top: 5px;

  display: flex;
  align-items: center;
}

.row_list {
  list-style: none;
}

.cases_list::-webkit-scrollbar {
  display: none;
}

.cases_list li {
  display: grid;
  -ms-grid-columns: 30px 110px 60px 60px 60px 50px 100px;
  grid-template-columns: 30px 110px 60px 60px 60px 50px 100px;
  cursor: pointer;
  margin-left: 23px;
  text-align: center;
  line-height: 30px;
  color: rgb(238, 236, 236);
}

.list_time {
  height: 30px;
  overflow: auto;
}

.list_time::-webkit-scrollbar {
  display: none;
}
</style>