import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'next-i18next'
// import { useRouter } from 'next/router'
// import useSearch from '@/lib/search/useSearch'
import useLoadSearch from '@/lib/search/useLoadSearch'
import { Box, Input, InputGroup, InputLeftElement } from '@chakra-ui/react'
import { SearchIcon } from '@chakra-ui/icons'

import { ArticleIndexItem } from '@/models/ArticleIndexItem'
import { TextWithTranslation } from '../TextWithTranslation'
import { AutoComplete } from './AutoComplete'
import { LoLink } from '../LoLink'

type SearchBoxProps = {
  dataUrl: string
}
const SEARCH_KEYS = ['title', 'original_title']

export const SearchBox = ({ dataUrl }: SearchBoxProps) => {
  const { t } = useTranslation('common')
  const inputRef = useRef<HTMLInputElement>(null)
  const [inputWidth, setInputWidth] = useState('0px')
  const [isOpen, setIsOpen] = useState(false)
  const currentWitdth = inputRef?.current?.offsetWidth || 0
  useEffect(() => {
    if (inputRef.current) {
      setInputWidth(`${inputRef.current.offsetWidth}px`)
    }
  }, [currentWitdth])

  // if you define search keys inside here, it will result in an infinite loop
  const { search } = useLoadSearch<ArticleIndexItem>(dataUrl, SEARCH_KEYS)

  const [searchTerm, setSearchTerm] = useState('')
  const [results, setResults] = useState<ArticleIndexItem[]>([])
  const onSearchTermChange = event => {
    const value = event.target.value
    setSearchTerm(value)
    if (value.length >= 1) {
      const r = search.search(value, { limit: 10 })
      const items = r.map(result => result.item)
      setResults(items)
    } else {
      setResults([])
    }
  }

  const resultsList = results.map(result => {
    return (
      <LoLink href={`/articles/${result.id}`} key={result.id}>
        <TextWithTranslation
          text={result.title}
          originalText={result.original_title}
        />
      </LoLink>
    )
  })

  return (
    <Box
      width='100%'
      margin={5}
      // onBlur={() => setIsOpen(false)}
      onFocus={() => setIsOpen(true)}
      // display="flex"          // Added for Flexbox layout
      //justifyContent="center" // Centers horizontally in the flex container
    >
      <Box width='50hv' paddingLeft={5} paddingRight={5}>
        <InputGroup>
          <InputLeftElement pointerEvents='none'>
            <SearchIcon color='gray.800' />
          </InputLeftElement>
          <Input
            value={searchTerm}
            fontSize={'xl'}
            width={'100%'}
            ref={inputRef}
            placeholder={t('search')}
            onChange={onSearchTermChange}
          />
        </InputGroup>

        {isOpen && (
          <AutoComplete width={inputWidth}>{resultsList}</AutoComplete>
        )}
      </Box>
    </Box>
  )
}
