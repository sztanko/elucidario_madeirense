import Head from 'next/head'
import { Box, Center, Image, Heading, Text } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next' // or your i18n library's hook
import { getStaticPaths, makeStaticProps } from '../../lib/i18n/getStatic'
import { AppLayout } from '@/components/layout/AppLayout'
import { loadArticleIndex } from '@/lib/search/dataUtils'
import { SearchBox } from '@/components/search/SearchBox'
import { Letter } from '@/components/article_index/Letter'
// import { createSearchIndex } from '@/lib/search/fuseUtils'

const createSearchIndexProps = async ctx => {
  const { locale } = ctx.params
  const { articleIndex } = await loadArticleIndex(locale)
  const topArticles = articleIndex.filter(article => article.length > 10000)
  return { topArticles, locale }
}

const getStaticProps = makeStaticProps(createSearchIndexProps) // createSearchIndexProps)
export { getStaticPaths, getStaticProps }

export default function Home ({ topArticles, locale }) {
  const { t } = useTranslation('common')

  // Use NEXT_PUBLIC_WEB_PATH env varialbe as prefix
  const dataUrl = `${process.env.NEXT_PUBLIC_WEB_PATH}/index/index_${locale}.json`
  return (
    <>
      <Head>
        <title>Elucidario Madeirense</title>
        <meta name='description' content={t('meta_description')} />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
      </Head>
      <AppLayout locale={locale}>
        <Heading mb='2' as={'h1'} textAlign={'center'}>
          Elucidário Madeirense
        </Heading>
        <Text textAlign={'justify'}>{t('meta_description')}</Text>

        <Box mt={10} ml={10} mr={10}>
          <SearchBox dataUrl={dataUrl} showTags={true} fontSize={'xl'} />
        </Box>

        <Heading
          mb='10'
          mt={10}
          as={'h2'}
          textAlign={'center'}
          fontSize={'xl'}
          color='#777'
        >
          {t('important_articles')}
        </Heading>
        <Letter articles={topArticles} letter='A' showLetter={false} />
      </AppLayout>
    </>
  )
}
