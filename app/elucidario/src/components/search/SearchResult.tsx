import { Text, Box, Heading, HStack, Tag } from '@chakra-ui/react'
import { FuseResult } from 'fuse.js'
import { LoLink } from '../LoLink'
import { ArticleData } from '@/models/ArticleData'
import { TextWithTranslation } from '../TextWithTranslation'
import { ResultHighlightList } from './ResultHighlightList'

type SearchResultProps = {
  results: FuseResult<ArticleData>
}
export const SearchResult = ({ result }) => {
    console.info('SearchResult', result)
  const bodyMatches = result.matches.find(match => match.key === 'body')

  return (
    <Box key={result.item.id} mb={4}>
      <Heading as='h2' fontSize='xl' marginBottom={4}>
        <LoLink href={`/articles/${result.item.id}`}>
          <TextWithTranslation
            text={result.item.title}
            originalText={result.item.original_title}
          />
        </LoLink>
      </Heading>
      {bodyMatches && <ResultHighlightList
        indices={bodyMatches?.indices}
        value={bodyMatches?.value}
        threshold={30}
      />}
    </Box>
  )
}
