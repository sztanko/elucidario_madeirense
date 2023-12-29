import { extendTheme } from '@chakra-ui/react'
import { darken, lighten } from 'polished'

const base = 'rgb(83, 61, 59)'

const theme = extendTheme({
  colors: {
    main: {
      base: base,
      link: darken(10, base),
      linkHover: darken(20, base)
    }
  },
  styles: {
    global: {
      // Applying styles globally across all text elements
      body: {
        fontFamily: 'Georgia, serif',
        // fontSize: '1.125rem', // Equivalent to 18px
        lineHeight: '1.6',
        color: 'main.base'
      },
      a: {
        color: 'main.link',
        textDecoration: 'none',
        _hover: {
          color: 'main.linkHover',
          textDecoration: 'underline'
        }
      }
    }
  },
  components: {
    "Tag": {
      baseStyle: {
        borderRadius: '0',
        color: 'main.base',
        bg: 'yellow',
        border: '1px solid',
        borderColor: 'main.base',
        _hover: {
          bg: 'main.base',
          color: 'white'
        }
      }
    },
    },
  

  // You can also set the fonts more granularly for specific components or text styles
  fonts: {
    heading: 'Times New Roman, serif',
    body: 'Georgia, serif'
  }
  // ... other theme customizations
})

export default theme
