import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'next-i18next'
// import { useRouter } from 'next/router'
// import useSearch from '@/lib/search/useSearch'
import useLoadSearch from '@/lib/search/useLoadSearch'
import {
  Box,
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  InputProps,
  Progress,
  Text
} from '@chakra-ui/react'
import { FuseResult } from 'fuse.js'
import { SearchIcon } from '@chakra-ui/icons'

import { ArticleData } from '@/models/ArticleData'

type AdvancedSearchBoxProps = InputProps & {
  dataUrl: string
  onSearch: (searchTerm: string, results: FuseResult<ArticleData>[]) => void
}
const SEARCH_OPTIONS = {
  includeScore: true,
  includeMatches: true,
  ignoreLocation: true,
  threshold: 0,
  minMatchCharLength: 3,
  keys: ['body', 'title', 'original_title']
}

export const AdvancedSearchBox = ({
  dataUrl,
  onSearch,
  ...rest
}: AdvancedSearchBoxProps) => {
  const { t } = useTranslation('common')

  // if you define search keys inside here, it will result in an infinite loop
  const { search, loading } = useLoadSearch<ArticleData>(
    dataUrl,
    SEARCH_OPTIONS
  )

  const [searchTerm, setSearchTerm] = useState('')

  const onClick = () => {
    const r = search.search(searchTerm, { limit: 30 })
    onSearch(searchTerm, r)
  }
  if (loading)
    return (
      <Box width='100%' margin={1}>
        <Text>{t['loading']}</Text>
        <Progress size='xs' isIndeterminate />
      </Box>
    )
  return (
    <Box width='100%' margin={1}>
      <form
        onSubmit={e => {
          e.preventDefault()
          e.stopPropagation()
          onClick()
        }}
      >
        <InputGroup>
          <InputLeftElement pointerEvents='none'>
            <SearchIcon color='gray.800' />
          </InputLeftElement>
          <Input
            {...rest}
            value={searchTerm}
            placeholder={t('search')}
            onChange={event => setSearchTerm(event.target.value)}
          />
          <Button onClick={onClick}>{t('find')}</Button>
        </InputGroup>
      </form>
    </Box>
  )
}
