import { Box, Heading, Tag, HStack } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next'
import { FuseResult } from 'fuse.js'
import { LoLink } from '../LoLink'
import { ArticleData } from '@/models/ArticleData'
import { TextWithTranslation } from '../TextWithTranslation'
import { ResultHighlightList } from './ResultHighlightList'

export const SearchResult = ({ result }) => {
  const { t } = useTranslation('common')
  const bodyMatches = result.matches.find(match => match.key === 'body')
  const categories = result.item.categories.map(category => (
    <Tag key={category}>{t(category)}</Tag>
  ))
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
      <HStack spacing={6} color={'#888'} mb={4} justifyContent={'flex-start'}>
        {categories}
      </HStack>
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
