import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'next-i18next'
// import { useRouter } from 'next/router'
// import useSearch from '@/lib/search/useSearch'
import useLoadSearch from '@/lib/search/useLoadSearch'
import {
  Box,
  Input,
  InputGroup,
  InputLeftElement,
  InputRightElement,
  InputProps,
  Flex,
  Tag
} from '@chakra-ui/react'
import { SearchIcon, SmallCloseIcon } from '@chakra-ui/icons'

import { ArticleIndexItem } from '@/models/ArticleIndexItem'
import { TextWithTranslation } from '../TextWithTranslation'
import { AutoComplete } from './AutoComplete'
import { LoLink } from '../LoLink'

type SearchBoxProps = InputProps & {
  dataUrl: string
  showTags?: boolean
}
const SEARCH_OPTIONS = {
  includeScore: true,
  threshold: 0.3,
  keys: ['title', 'original_title']
}

export const SearchBox = ({ dataUrl, showTags, ...rest }: SearchBoxProps) => {
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
  const { search, loading } = useLoadSearch<ArticleIndexItem>(
    dataUrl,
    SEARCH_OPTIONS
  )

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
      <LoLink
        href={`/articles/${result.id}`}
        key={result.id}
        onClick={() => setIsOpen(false)}
      >
        <Flex>
          <TextWithTranslation
            text={result.title}
            originalText={result.original_title}
          />
          {showTags &&
            result.categories.map(category => (
              <Tag
                key={category}
                ml={2}
                mr={2}
                color={'#888'}
                fontSize={'smaller'}
              >
                {t(category)}
              </Tag>
            ))}
        </Flex>
      </LoLink>
    )
  })

  return (
    <Box
      width='100%'
      margin={[0, 1]}
      // onBlur={() => setIsOpen(false)}
      onFocus={() => setIsOpen(true)}
      display='flex' // Added for Flexbox layout
      justifyContent='center' // Centers horizontally in the flex container
    >
      <Box width={'100%'}>
        <InputGroup>
          <InputLeftElement pointerEvents='none'>
            <SearchIcon color='gray.800' />
          </InputLeftElement>
          <Input
            {...rest}
            disabled={loading}
            value={searchTerm}
            borderColor={'gray.800'}
            // fontSize={'xl'}
            ref={inputRef}
            placeholder={loading ? t('loading') : t('search')}
            onChange={onSearchTermChange}
          />
          {searchTerm && (
            <InputRightElement>
              <SmallCloseIcon
                color='gray.800'
                _hover={{ cursor: 'pointer', color: '#999' }}
                onClick={() => {
                  setSearchTerm('')
                  setIsOpen(false)
                }}
              />
            </InputRightElement>
          )}
        </InputGroup>

        {isOpen && searchTerm.length > 0 && (
          <AutoComplete width={inputWidth}>{resultsList}</AutoComplete>
        )}
      </Box>
    </Box>
  )
}
