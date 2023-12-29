import Head from 'next/head'
import { useState } from 'react'
import { Box, Center, Heading, Text } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next' // or your i18n library's hook
import { getStaticPaths, makeStaticProps } from '@/lib/i18n/getStatic'
import { AppLayout } from '@/components/layout/AppLayout'
import { AdvancedSearchBox } from '@/components/search/AdvancedSearchBox'
import { SearchResults } from '@/components/search/SearchResults'

const getStaticProps = makeStaticProps() // createSearchIndexProps)
export { getStaticPaths, getStaticProps }

export default function Home ({ topArticles, locale }) {
  const { t } = useTranslation('common')
  const { t: tm } = useTranslation('menu')
  const [searchResults, setSearchResults] = useState([])
  // Use NEXT_PUBLIC_WEB_PATH env varialbe as prefix
  const dataUrl = `${process.env.NEXT_PUBLIC_WEB_PATH}/index/index_full_${locale}.json`
  return (
    <>
      <Head>
        <title>{`${tm('advanced_search')} - Elucidario Madeirense`}</title>
        <meta name='description' content={t('meta_description')} />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <AppLayout locale={locale}>
        <Heading mb='2' as={'h1'} textAlign={'center'}>
          Elucidário Madeirense - {tm('advanced_search')}
        </Heading>

        <Box
          mt={10}
          width='80%'
          display='flex'
          justifyContent='center'
          alignItems='center'
        >
          <AdvancedSearchBox dataUrl={dataUrl} fontSize={'xl'} onSearch={setSearchResults}/>
        </Box>
      <SearchResults results={searchResults}/>
      </AppLayout>
    </>
  )
}
