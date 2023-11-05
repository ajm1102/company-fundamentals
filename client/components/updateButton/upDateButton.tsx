import { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import { redirect } from 'next/navigation'
import { useRouter } from 'next/navigation';
import Loading from '@/components/loadingAnim/loading'


function UpDateButton() {
  const [loadingSpinner, setLoadingSpinner] = useState(false);
  const [downloadItems, setDownloadItems] = useState<any[]>([])
  const [stopDownload, setStop] = useState(false)

  const stateRef = useRef();
  stateRef.current = stopDownload as any;
  
  const { push } = useRouter();
 
  async function startUpdate() {
    setLoadingSpinner(true)
    let res = await fetch(`http://localhost:8080/download_update_dataset?update=true`,
    { credentials: 'include' });
    
    if (res.ok) {
      console.log("finished")
      //
      setLoadingSpinner(false)
      push('/charts');
    } 
  }

 
  const stopDownloadFn = (e: any) => {
    setStop(true)
    console.log("sfsdf")
  }
 
  useEffect(() => {
    const socketInstance = io('http://localhost:8080'); // Replace with your Flask server's address

    socketInstance.on('message_from_server', (data, fn) => {
      setDownloadItems((old) => [...old, data.data])
      console.log(stateRef.current)
      
      if (stateRef.current == false){
        fn("ok")
      } else {
        fn("stop")
      }
      
    });
  }, []);

  return (
    <>
      <ul id='loadingItemsList'>
        {downloadItems.map((downloadItem) => (
          <li>{downloadItem}</li>
        ))}
      </ul>
      <div className="wrapper">
      <button id='stopDownload' onClick={stopDownloadFn}>Stop download</button>
      <button id='downloadDataButton' onClick={startUpdate}>Download</button>
      {loadingSpinner && <Loading/>}
      <button id='skipButton' onClick={() => push('/charts')}>Skip</button>
      </div>
    </>
  )
}

export default UpDateButton