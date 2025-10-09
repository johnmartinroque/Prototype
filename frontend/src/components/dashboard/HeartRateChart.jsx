import React from "react";
import Chart from "react-apexcharts";

function HeartRateBarChart() {
  const chartConfig = {
    series: [
      {
        name: "Heart Rate",
        data: [70, 80, 62, 70, 50, 55], // your averageHeartBeat
      },
    ],
    options: {
      chart: {
        type: "bar",
        toolbar: { show: false },
      },
      plotOptions: {
        bar: {
          borderRadius: 6,
          columnWidth: "50%",
        },
      },
      dataLabels: {
        enabled: true,
      },
      xaxis: {
        categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        title: { text: "Days" },
      },
      yaxis: {
        title: { text: "BPM" },
      },
      colors: ["#1e88e5"],

      // 🔑 Make responsive
      responsive: [
        {
          breakpoint: 1024, // tablet
          options: {
            plotOptions: { bar: { columnWidth: "60%" } },
          },
        },
        {
          breakpoint: 640, // mobile
          options: {
            plotOptions: { bar: { columnWidth: "70%" } },
            dataLabels: { enabled: false },
            xaxis: { labels: { show: false } },
          },
        },
      ],
    },
  };

  return (
    <div className="relative flex flex-col rounded-xl bg-white p-6 shadow-md w-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        <div className="w-max rounded-lg bg-gray-900 p-5 text-white">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="h-6 w-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3
                 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25
                 -4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0
                 l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142
                 0l-5.571 3-5.571-3"
            />
          </svg>
        </div>
        <div>
          <h6 className="text-base font-semibold text-gray-900">Bar Chart</h6>
          <p className="text-sm text-gray-700">
            Visualize your data in a simple way using ApexCharts.
          </p>
        </div>
      </div>

      {/* Chart */}
      <div className="pt-6 w-full">
        <Chart
          options={chartConfig.options}
          series={chartConfig.series}
          type="bar"
          height="300" // use only height
        />
      </div>
    </div>
  );
}

export default HeartRateBarChart;
