import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
  styles: {
    global: {
      // Applying styles globally across all text elements
      body: {
        fontFamily: 'Georgia, serif',
        fontSize: '1.125rem', // Equivalent to 18px
        lineHeight: '1.6',
        color: 'rgba(83, 61, 59)'
      }
    }
  },
  // You can also set the fonts more granularly for specific components or text styles
  fonts: {
    heading: 'Times New Roman, serif',
    body: 'Georgia, serif'
  }
  // ... other theme customizations
})

export default theme
