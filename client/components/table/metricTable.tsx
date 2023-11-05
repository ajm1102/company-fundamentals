import React from 'react'
import SaveTable from './saveTable'
function MetricTable(props: any) {
  const data = Object.values(props.data) as any

  return (
    <>
      <table id='metricTable'>
        <thead>
        <tr>
          <th>date</th>
          <th>{props.metric}</th>
        </tr>
        </thead>        
        <tbody>
        {data.map((x: any) => (
            <tr>
              <td>{x.date}</td>
              <td>{x[props.metric]}</td>
            </tr>
        ))}
        </tbody>
      </table>
      <SaveTable metric={props.metric} savedata={data}/>
    </>    
    )
}

export default MetricTable