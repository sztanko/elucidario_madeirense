import React from 'react'
import { Box } from '@chakra-ui/react'

export const Platform = ({ children, ...rest }) => {
  return (
    <Box
      backgroundColor='rgba(255, 255, 255, 0.8)'
      p={4}
      {...rest}
    >
      {children}
    </Box>
  )
}
