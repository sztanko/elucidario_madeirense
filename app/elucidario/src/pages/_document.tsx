import { Html, Head, Main, NextScript } from 'next/document'
import i18nextConfig from '../../next-i18next.config'

export default function Document (props) {
  // console.log('props', props)
  const currentLocale =
    props.__NEXT_DATA__.query.locale || i18nextConfig.i18n.defaultLocale
  const baseURI = process.env.NEXT_PUBLIC_WEB_PATH || ''
  return (
    <Html lang={currentLocale}>
      <Head>
        <link rel='icon' href={`${baseURI}/favicon.ico`} />
        <script
          data-goatcounter='https://elucidario.goatcounter.com/count'
          async
          src='//gc.zgo.at/count.js'
        ></script>
      </Head>
      <body
        style={{
          minHeight: '100vh',
          background: `url('${baseURI}/background.webp'), linear-gradient(to right, rgb(232, 232, 220), rgb(230, 229, 218))`,
          backgroundPosition: 'center bottom',
          backgroundRepeat: 'no-repeat',
          backgroundSize: '100% auto'
        }}
      >
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
