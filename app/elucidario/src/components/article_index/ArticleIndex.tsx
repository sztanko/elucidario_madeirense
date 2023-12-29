import { useTranslation } from 'next-i18next'
import * as _ from 'lodash'

import { VStack, HStack, Link, Box, Divider } from '@chakra-ui/react'
import { Letter } from './Letter'
import { ArticleIndexItem } from '@/models/ArticleIndexItem'

type ArticleIndexProps = {
  articleIndex: ArticleIndexItem[]
  locale: string,
  showLetters?: boolean
}

export function ArticleIndex ({ articleIndex, showLetters, locale }: ArticleIndexProps) {
  const { t } = useTranslation('common', { useSuspense: false })
  // Group all articles by first letter and order both keys and value array
  const letters = _.chain(articleIndex)
    .groupBy(article => article.fl)
    .toPairs()
    .sort((a, b) => a[0].localeCompare(b[0], locale))
    .fromPairs()
    .value()

  const letterLinks = showLetters?_.keys(letters).map(letter => (
    <Link
      href={`#${letter}`}
      key={letter}
      scrollBehavior='smooth'
      fontSize={20}
    >
      {letter}
    </Link>
  )):null

  const letterComponents = _.chain(letters)
    .toPairs()
    .map(([letter, articles]) => (
      <Letter key={letter} letter={letter} articles={articles} showLetter={true} />
    ))
    .value()
  // const people
  //<HStack justifyContent={'space-around'}>{letterLinks}</HStack>
  return (
    <Box>
      {showLetters && <><HStack justifyContent={'space-around'} flexWrap='wrap'>{letterLinks}</HStack>
      <Divider borderColor='#333' mt={3} mb={3} /></>}
      
      <VStack spacing={6} color={'#888'} mb={4} justifyContent={'flex-end'}>
        {letterComponents}
      </VStack>
    </Box>
  )
}
