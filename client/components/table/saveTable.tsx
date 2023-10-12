import React from 'react'
import { CSVLink, CSVDownload } from "react-csv";

function saveTable(props: any) {
    
    const data = props.savedata as any

    const arrayLength = data.length;

    const headers = ['dates', props.metric]
    const zip = (a:any, b:any) => a.map((k:any, i:any) => `${k}, ${b[i]||''}`)
    const zipLonger = (a:any, b:any) => a.length > b.length ? zip(a, b) : zip(b, a)

    let dates = []
    let vals = []

    for (var i = 0; i < arrayLength; i++) {
        dates.push(data[i].date)
        vals.push(data[i][props.metric])
    }

    let shit = headers.join(', ')+'\n'+
                zipLonger(vals, dates).join('\n')

  return (
    <>
    <button>
        <CSVLink className="button" data={shit} separator={","}>
            Download me
        </CSVLink>
    </button>
    </>
  )
}

export default saveTable