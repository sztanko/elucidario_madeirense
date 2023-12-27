import { ChakraProvider } from '@chakra-ui/react'
import { Container } from '@chakra-ui/react'
import { appWithTranslation } from 'next-i18next'

import { Platform } from '../components/layout/Platform'
import { Menu } from '../components/layout/Menu'
import theme from '../theme/theme' // Adjust the import path to where your theme file is located

function App ({ Component, pageProps }) {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps} />
    </ChakraProvider>
  )
}

export default appWithTranslation(App)
