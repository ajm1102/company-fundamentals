import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";


function SharePriceLineChart(props: any) {
    console.log(props.data)
  return (
    <>
    <div >
    <LineChart
      width={600}
      height={400}
      data={props.data}
      margin={{
        top: 20,
        right: 20,
        left: 70,
        bottom: 15
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
    <Line
        type="monotone"
        dataKey="price"
        stroke="#8884d8"
      /> 
    </LineChart>
    </div>
    </>
  );
}
export default SharePriceLineChart