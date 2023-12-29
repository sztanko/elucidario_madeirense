import React from 'react'
import {
  Box,
  Code,
  Heading,
  Text,
  List,
  ListItem,
  UnorderedList,
  Table,
  Thead,
  Tbody,
  Tr,
  Td,
  Th,
  OrderedList
} from '@chakra-ui/react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export const MarkdownRenderer = ({ markdownText }) => {

  return (
    <Box p={5} textAlign={"justify"}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ node, ...props }) => <Heading size='xl' {...props} />,
          h2: ({ node, ...props }) => <Heading size='lg' {...props} />,
          h3: ({ node, ...props }) => <Heading size='md' {...props} />,
          p: ({ node, ...props }) => <Text my={3} as={"p"} {...props} />,
          pre: ({ node, children, ...props }) => (
            <Text as='p' borderColor={'red'}>
              {children}
            </Text>
          ),
          code: ({ node, ...props }) => <Code p={2} {...props} />,
          blockquote: ({ node, ...props }) => (
            <Box
              as='blockquote'
              p={0}
              {...props}
              fontStyle={'italic'}
              whiteSpace={'pre-wrap'}
            />
          ),
          li: ({ node, ...props }) => <ListItem my={2} {...props} />,
          //li: ({ node, children, ...props }) => <ListItem as='li'>- ({children})</ListItem>,
          ol: ({ node, children, ...props }) => <UnorderedList as='ol'>{children}</UnorderedList>,
          ul: ({ node, children, ...props }) => <UnorderedList as='ol'>{children}</UnorderedList>,
          // ul: ({ node, ...props }) => <UnorderedList my={2} {...props} />,
          em: ({ node, ...props }) => <Text as='em' {...props} />,
          text: ({ node, children, ...props }) => (
            <Text as='p'>{children}</Text>
          ),
          table: props => <Table variant='simple' size='sm' {...props} />,
          thead: props => <Thead bgColor='gray.100' {...props} />,
          tbody: Tbody,
          tr: Tr,
          td: props => (
            <Td
              fontSize='sm'
              py={2}
              border='1px'
              borderColor='gray.200'
              {...props}
            />
          ),
          th: props => (
            <Th
              fontSize='sm'
              py={2}
              fontWeight='bold'
              border='1px'
              borderColor='gray.200'
              textAlign='left'
              {...props}
            />
          )
        }}
      >
        {markdownText}
      </ReactMarkdown>
    </Box>
  )
}
