import { ChakraProvider } from '@chakra-ui/react'
import { Box } from '@chakra-ui/react'
import theme from "../theme/theme"; // Adjust the import path to where your theme file is located

function MyApp({ Component, pageProps }) {
  return (
    <ChakraProvider theme={theme}>
            <Box
                minHeight='100vh' // Ensures the div is at least the height of the viewport
                background={`url('/background.webp'), linear-gradient(to right, rgb(232, 232, 220), rgb(230, 229, 218))`}
                backgroundPosition='center bottom' // Aligns the image at the bottom center
                backgroundRepeat='no-repeat' // Prevents the image from repeating
                backgroundSize='100% auto' // Ensures the image covers the entire div
                width='100%' // Ensures the div spans the full width
      >
        <Component {...pageProps} />
      </Box>
      

    </ChakraProvider>
  )
}

export default MyApp