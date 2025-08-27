import type { ChartConfig } from '../../../../../resources/components/chart/chart';
import Chart from '../../../../../resources/components/chart/bar-chart'
import ChartCount from '../../../../../resources/components/Chart/chart-count'
import ChartLine from '../../../../../resources/components/Chart/Chart-line'
import { NetIncomeChart } from '../../../../../resources/components/chart/NetProfitChart';

function ChartComponent() {
    const chartData = [
        { month: "January", year: 2024, desktop: 186, mobile: 80 },
        { month: "February", year: 2024, desktop: 305, mobile: 200 },
        { month: "April", year: 2024, desktop: 73, mobile: 190 },
        { month: "May", year: 2024, desktop: 209, mobile: 130 },
        { month: "June", year: 2024, desktop: 214, mobile: 140 },
        { month: "January", year: 2025, desktop: 400, mobile: 200 },
        { month: "March", year: 2025, desktop: 300, mobile: 210 },
    ];

        const chartConfig = {
        desktop: {
            label: "Desktop",
            color: "#3b82f6", // resolved Tailwind color (blue-500)
        },
        mobile: {
            label: "Mobile",
            color: "#ec4899", // resolved Tailwind color (pink-500)
        },
     
    };

    
const chartLineData = [
  { month: "January", year: 2024, desktop: 186, mobile: 80 },
  { month: "February", year: 2024, desktop: 305, mobile: 200 },
  { month: "March", year: 2024, desktop: 237, mobile: 120 },
  { month: "April", year: 2024, desktop: 73, mobile: 190 },
  { month: "May", year: 2024, desktop: 209, mobile: 130 },
  { month: "June", year: 2024, desktop: 214, mobile: 140 },
  { month: "January", year: 2023, desktop: 150, mobile: 60 },
  { month: "February", year: 2023, desktop: 190, mobile: 90 },
]

const chartLineConfig = {
  desktop: {
    label: "Desktop",
    color: "hsl(var(--chart-1))",
  },
  mobile: {
    label: "Mobile",
    color: "hsl(var(--chart-2))",
  },
}

const myChartData = [
  { year: 2024, month: "January", desktop: 186, mobile: 100 },
  { year: 2024, month: "February", desktop: 305, mobile: 120 },
  { year: 2024, month: "March", desktop: 237, mobile: 90 },
  { year: 2024, month: "April", desktop: 73, mobile: 50 },
  { year: 2024, month: "May", desktop: 209, mobile: 110 },
  { year: 2024, month: "June", desktop: 214, mobile: 130 },
  { year: 2024, month: "July", desktop: 322, mobile: 150 },
  { year: 2024, month: "August", desktop: 278, mobile: 140 },
  { year: 2024, month: "September", desktop: 345, mobile: 160 },
  { year: 2024, month: "October", desktop: 312, mobile: 170 },
  { year: 2024, month: "November", desktop: 388, mobile: 180 },
  { year: 2024, month: "December", desktop: 600, mobile: 200 },
  { year: 2025, month: "January", desktop: 134, mobile: 80 },
  { year: 2025, month: "February", desktop: 278, mobile: 110 },
  { year: 2025, month: "March", desktop: 300, mobile: 130 },
  { year: 2025, month: "April", desktop: 198, mobile: 95 },
  { year: 2025, month: "May", desktop: 233, mobile: 105 },
];

const myChartConfig = {
  desktop: {
    label: "Desktop Traffic",
    color: "hsl(var(--chart-1))",
  },
  mobile: {
    label: "Mobile Traffic",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

const anotherChartConfig = {
  sales: {
    label: "Monthly Sales",
    color: "hsl(var(--blue-500))", // Example of a different color variable
  }
} satisfies ChartConfig;

const salesData = [
  { year: 2024, month: "January", sales: 5000 },
  { year: 2024, month: "February", sales: 6500 },
  { year: 2024, month: "March", sales: 7200 },
  { year: 2025, month: "January", sales: 4800 },
  { year: 2025, month: "February", sales: 6000 },
];

// net profit chart

const NetIncomeDate = [
  { month: "January", value: 186 },
  { month: "February", value: 205 },
  { month: "March", value: -207 },
  { month: "April", value: 173 },
  { month: "May", value: -209 },
  { month: "June", value: 214 },
]
  return (
    <div className='flex flex-col gap-5 lg:w-[50%]'>
       <Chart
            data={chartData}
            config={chartConfig}
            title="Visitors by Device"
            description="Breakdown of desktop vs mobile users"
            />
        <ChartCount
        data={myChartData}
        config={myChartConfig}
        initialSelectedYear={2024}
        chartTitle="Website Traffic"
        chartDescription="Monthly visitors"
        barDataKey="desktop"
        barColor="#3a238b"
        trendingText="Desktop traffic increased by 5.2%!"
        footerDescription="Showing desktop visitors for"
      />

      {/* Example 2: Using a different data key and color */}
      <ChartCount
        data={salesData}
        config={anotherChartConfig}
        initialSelectedYear={2025}
        chartTitle="Sales Performance"
        chartDescription="Monthly revenue"
        barDataKey="sales"
        barColor="#1d9f0d" // Using a different chart color
        trendingText="Sales are booming by 8.5%!"
        footerDescription="Displaying total sales for"
      />
        
        <ChartLine
        title="Visitors Trend"
        description="Showing visits for"
        data={chartLineData}
        dataKeys={["desktop", "mobile"]}
        config={chartLineConfig}
        defaultYear={2024}
        />

        <NetIncomeChart
          title="Visitors Overview"
          description="Jan - Jun 2024"
          data={NetIncomeDate}
          dataKey="value"
          labelKey="month"
          footerInfo="Summarized visitor flow for last 6 months"
          trend="Up by 5.2%"
        />
    </div>
  )
}

export default ChartComponent