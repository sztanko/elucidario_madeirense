import { Box, Heading, Flex } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next'
import { LoLink } from '../LoLink'
import { TextWithTranslation } from '../TextWithTranslation'
import { ResultHighlightList } from './ResultHighlightList'
import { Categories } from '../article/Categories'

export const SearchResult = ({ result }) => {
  const { t } = useTranslation('common')
  const bodyMatches = result.matches.find(match => match.key === 'body')

  return (
    <Box key={result.item.id} mb={4}>
      <Flex justify={'space-between'} mb={2}>
        <Heading as='h2' fontSize='xl'>
          <LoLink href={`/articles/${result.item.id}`}>
            <TextWithTranslation
              text={result.item.title}
              originalText={result.item.original_title}
            />
          </LoLink>
        </Heading>
        <Categories categories={result.item.categories} fontSize={'smaller'} />
      </Flex>
      {bodyMatches && (
        <ResultHighlightList
          indices={bodyMatches?.indices}
          value={bodyMatches?.value}
          threshold={30}
        />
      )}
    </Box>
  )
}
