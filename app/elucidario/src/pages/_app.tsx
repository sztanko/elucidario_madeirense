import { ChakraProvider } from '@chakra-ui/react'
import { Container, Box } from '@chakra-ui/react'

import { Platform } from '../components/Platform'
import { Menu } from '../components/Menu'
import theme from '../theme/theme' // Adjust the import path to where your theme file is located

function MyApp ({ Component, pageProps }) {
  return (
    <ChakraProvider theme={theme}>
      <Container maxW='container.xxl' centerContent>
        <Platform w={'100%'}>
          <Menu />
        </Platform>
      </Container>
      <Container maxW='container.xl' centerContent>
        <Platform mt={4}>
          <Component {...pageProps} />
        </Platform>
      </Container>
    </ChakraProvider>
  )
}

export default MyApp
