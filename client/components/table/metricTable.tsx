import React from 'react'
import SaveTable from './saveTable'
function MetricTable(props: any) {
  const data = Object.values(props.data) as any

  return (
    <>
      <tbody>
      {data.map((x: any) => (
          <tr>
            <td>{x.date}</td>
            <td>{x[props.metric]}</td>
          </tr>
      ))}
      </tbody>
      <SaveTable metric={props.metric} savedata={data}/>
    </>    
    )
}

export default MetricTable