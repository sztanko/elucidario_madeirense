import { useTranslation } from 'next-i18next'
import { Box, Heading, Text, HStack, Tag} from '@chakra-ui/react'
import { size } from 'lodash'
import { MarkdownRenderer } from '../MarkdownRenderer'
import { EnumList } from './EnumList'
import { TextWithTranslation } from '../TextWithTranslation'
import { ArticleData } from '@/models/ArticleData'

type ArticleProps = {
  article: ArticleData
}

export function Article ({ article }: ArticleProps) {
  const { t } = useTranslation('common')
  const categories = article.categories.map(category => (
    <Tag key={category}>{t(category)}</Tag>
  ))

  // const people
  return (
    <Box maxWidth={'900px'}>
      <HStack spacing={6} color={'#888'} mb={4} justifyContent={'flex-end'}>
        {categories}
      </HStack>
      <Heading mb='0' fontSize='4xl' as={'h1'} textAlign={'left'}>
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
