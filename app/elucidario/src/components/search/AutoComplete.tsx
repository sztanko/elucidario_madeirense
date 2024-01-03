import { Box, List, ListItem } from '@chakra-ui/react'
import type { BoxProps } from '@chakra-ui/react'
import React from 'react'

type AutoCompleteProps = BoxProps & {
  // children must be an array of AutoCompleteItem components
  children: React.ReactElement[]
}

export const AutoComplete = ({ children, ...rest }: AutoCompleteProps) => {
  if (children.length === 0) return null

  return (
    <Box
      position='absolute' // Makes the component float above other elements
      bg='white'
      zIndex='dropdown' // Ensures it's above other content
      shadow='md' // Adds a shadow for better visibility
      cursor={'pointer'}
      {...rest}
    >
      <List spacing={0}>
        {children.map((item, index) => (
          <ListItem
            key={index}
            p={2}
            _hover={{ bg: 'gray.100' }}
            borderBottom={'1px solid #eee'}
          >
            {item}
          </ListItem>
        ))}
      </List>
    </Box>
  )
}
