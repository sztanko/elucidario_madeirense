import { Html, Head, Main, NextScript } from 'next/document'
import i18nextConfig from '../../next-i18next.config'

export default function Document (props) {
  console.log('props', props)
  const currentLocale =
    props.__NEXT_DATA__.query.locale || i18nextConfig.i18n.defaultLocale
  console.info('currentLocale', currentLocale)
  return (
    <Html lang={currentLocale}>
      <Head />
      <body
        style={{
          minHeight: '100vh',
          background: `url('/background.webp'), linear-gradient(to right, rgb(232, 232, 220), rgb(230, 229, 218))`,
          backgroundPosition: 'center bottom',
          backgroundRepeat: 'no-repeat',
          backgroundSize: '100% auto'
        }}
      >
        
        <Main />
        <pre>
          {props.__NEXT_DATA__.query.locale} || {i18nextConfig.i18n.defaultLocale}
        </pre>
        <NextScript />
      </body>
    </Html>
  )
}
