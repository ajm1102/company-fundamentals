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


function DataLineChart(props: any) {
  return (
    <>
    <div className=''>
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
        dataKey={props.metric}
        stroke="#8884d8"
      /> 
    </LineChart>
    </div>
    </>
  );
}
export default DataLineChart