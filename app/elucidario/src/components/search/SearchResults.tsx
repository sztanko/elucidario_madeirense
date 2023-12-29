import { Text, Box, Heading, HStack, Tag } from '@chakra-ui/react'
import { FuseResult } from 'fuse.js'
import { ArticleData } from '@/models/ArticleData'
import { SearchResult } from './SearchResult'

type SearchResultsProps = {
  results: FuseResult<ArticleData>[]
}
export const SearchResults = ({ results }: SearchResultsProps) => {
  return (
    <Box>
      {results.map(result => (
        <SearchResult key={result.item.id} result={result} />
      ))}
    </Box>
  )
}
