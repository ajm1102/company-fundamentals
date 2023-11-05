import '@/styles/globals.css'
import '@/styles/loading.css'
import '@/styles/enterStock.css'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
