import Head from 'next/head'
import { Heading, Text } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next' // or your i18n library's hook
import { getStaticPaths, makeStaticProps } from '../../lib/i18n/getStatic'
import { AppLayout } from '@/components/layout/AppLayout'
import { loadArticleIndex } from '@/lib/search/dataUtils'
import { SearchBox } from '@/components/search/SearchBox'
// import { createSearchIndex } from '@/lib/search/fuseUtils'
/*
const createSearchIndexProps = async ctx => {
  const { locale } = ctx.params
  const { articleIndex } = await loadArticleIndex(locale)
  return { articleIndex, locale }
}
*/

const getStaticProps = makeStaticProps() // createSearchIndexProps)
export { getStaticPaths, getStaticProps }

export default function Home ({ locale }) {
  const { t } = useTranslation('common')
  return (
    <>
      <Head>
        <title>Elucidario Madeirense</title>
        <meta name='description' content={t('meta_description')} />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <AppLayout locale={locale}>
        <Heading mb='2' as={'h1'} textAlign={'center'}>
          Elucidário Madeirense
        </Heading>
        <Text>{t('meta_description')}</Text>
        <SearchBox dataUrl={`/index/index_${locale}.json`} />
      </AppLayout>
    </>
  )
}
