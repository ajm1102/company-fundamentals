import React, {useEffect, useState} from 'react'
import DataLineChart from '@/components/charts/dataLineChart'
import SharePriceLineChart from '../charts/sharePriceLineChart'
import MetricTable from '../table/metricTable'

function StockDataFetch() {
    const [stockTicker, setStockTicker] = useState('')
    const [metricList, setMetricList] = useState([])
    const [renderList, setRenderList] = useState(false)
    const [metric, setMetric] = useState('')
    const [results, setResults] = useState([])
    const [sharePriceResults, setSharePriceResults] = useState([])

    useEffect(()=>{
    }, [metricList])

    useEffect(()=>{
    }, [results])

    useEffect(()=>{
    }, [metric])

    useEffect(()=>{
    }, [sharePriceResults])


    const handleChange = (event: { target: { value: React.SetStateAction<string> } }) => {
        setStockTicker(event.target.value);
    };

    async function getMetrics() {
        setRenderList(false)
        let res = await fetch(`http://localhost:8080/getMetrics?stockTicker=${stockTicker}`, { credentials: 'include' });
        
        let share_price_hist = await fetch(`http://localhost:8080/share_price_hist?stockTicker=${stockTicker}`, { credentials: 'include' });
        let message_received = await res.text();
        let share_price_hist_text = await share_price_hist.text();

        if (res.ok ) {
            let metricListVar = JSON.parse(message_received) as Array<TemplateStringsArray>

            setMetricList(JSON.parse(message_received))
            setRenderList(true)
            setSharePriceResults(JSON.parse(share_price_hist_text))
            getDataForInitialMetric(Object.values(metricListVar)[0])

        }
    }

    async function getDataForInitialMetric(firstMetric: any) {
        
        setMetric(firstMetric)
        let res = await fetch(`http://localhost:8080/metricHistory?metric=${firstMetric}`,
        { credentials: 'include' });
        
        let message_received = await res.text();
        
        if (res.ok) {
            setResults(JSON.parse(message_received));
        }
    }

    async function getDataForMetric(event: { target: { value: React.SetStateAction<string>; }; }) {
        setMetric(event.target.value)
        let res = await fetch(`http://localhost:8080/metricHistory?metric=${event.target.value}`,
        { credentials: 'include' });
        
        let message_received = await res.text();
        
        if (res.ok) {
            setResults(JSON.parse(message_received));
        }
    }



  return (
    <>
        <div id='enterListContainer'>
            <p className='enterTicker'>Please enter stock ticker below:</p>
            <input className='tickerTextBox' type='text' onChange={handleChange}></input>
            <button className='enterButton' role="button" onClick={getMetrics}>Enter</button>
        
            {renderList && <select className='listResult' onChange={getDataForMetric}>
                {metricList.map((listMetric)=> {
                    return <option>{listMetric}</option>
                })}
            </select>}
            </div>
        <div id='tableGraphOutputContainer'>
            {renderList && <DataLineChart className='metricGraph' metric={metric} data={results} />}
            {renderList && <MetricTable className='metricTable' metric={metric} data={results}/>}
            {renderList && <SharePriceLineChart className='sharePriceGraph' data={sharePriceResults} />} 
        </div>
    </>
  )
}

export default StockDataFetch