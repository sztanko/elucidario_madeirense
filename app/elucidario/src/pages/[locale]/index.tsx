import Head from 'next/head'
import { Heading, Text } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next' // or your i18n library's hook
import { getStaticPaths, makeStaticProps } from '../../lib/i18n/getStatic'
import { AppLayout } from '@/components/layout/AppLayout'

const createSearchIndex = async () => {}

const getStaticProps = makeStaticProps(['common', 'menu'])
export { getStaticPaths, getStaticProps }

export default function Home () {
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
