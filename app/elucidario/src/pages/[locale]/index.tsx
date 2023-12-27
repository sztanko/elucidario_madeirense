import Head from 'next/head'
import { Heading, Text } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next' // or your i18n library's hook
import { getStaticPaths, makeStaticProps } from '../../lib/i18n/getStatic'
import { AppLayout } from '@/components/layout/AppLayout'
// import { loadArticleIndex } from '@/lib/search/dataUtils'
import { createSearchIndex } from '@/lib/search/fuseUtils'

const createSearchIndexProps = async ctx => {
  const { locale } = ctx.params
  const { loadArticleIndex } = require('@/lib/search/dataUtils')
  const {articleIndex} = await loadArticleIndex(locale)
  // const searchIndex = createSearchIndex(articleIndex)
  return { articleIndex, locale }
}

const getStaticProps = makeStaticProps(createSearchIndexProps)
export { getStaticPaths, getStaticProps }

export default function Home ({ searchIndex, articleIndex, locale}) {
  const { t } = useTranslation('common')
  return (
    <>
      <Head>
        <title>Elucidario Madeirense</title>
        <meta name='description' content={t('meta_description')} />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <AppLayout>
        <Heading mb='2' as={'h1'} textAlign={'center'}>
          Elucidário Madeirense
        </Heading>
        <Text>{t('meta_description')}</Text>
      </AppLayout>
    </>
  )
}
