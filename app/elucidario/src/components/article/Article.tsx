import { useTranslation } from 'next-i18next'
import { Box, Heading } from '@chakra-ui/react'
import { size } from 'lodash'
import { MarkdownRenderer } from '../MarkdownRenderer'
import { EnumList } from './EnumList'
import { TextWithTranslation } from '../TextWithTranslation'
import { ArticleData } from '@/models/ArticleData'
import { Categories } from './Categories'

type ArticleProps = {
  article: ArticleData
}

export function Article ({ article }: ArticleProps) {
  const { t } = useTranslation('common')

  return (
    <Box maxWidth={'900px'}>
      <Categories categories={article.categories} />
      <Heading mb='0' mt={4} fontSize='4xl' as={'h1'} textAlign={'left'}>
        <TextWithTranslation
          text={article.title}
          originalText={article.original_title}
        />
      </Heading>

      <MarkdownRenderer markdownText={article.body} />

      {article.people && size(article.people) > 0 && (
        <EnumList name={t('people')} data={article.people} />
      )}
      {article.years && size(article.years) > 0 && (
        <EnumList name={t('years')} data={article.years} />
      )}
      {article.locations && size(article.locations) > 0 && (
        <EnumList name={t('locations')} data={article.locations} />
      )}
    </Box>
  )
}
