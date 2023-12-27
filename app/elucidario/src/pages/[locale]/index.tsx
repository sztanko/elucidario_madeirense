import Head from 'next/head'
import { Heading, Text } from '@chakra-ui/react'
import { getStaticPaths, makeStaticProps } from '../../lib/i18n/getStatic'
import { useTranslation } from 'next-i18next' // or your i18n library's hook


const createSearchIndex = async () => {

}

const getStaticProps = makeStaticProps(['common'])
export { getStaticPaths, getStaticProps }

export default function Home () {
  const { t } = useTranslation('common') // 'common' is a namespace for your translations

  return (
    <>
      <Head>
        <title>Elucidario Madeirense</title>
        <meta name='description' content={t('meta_description')} />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel='icon' href='/favicon.ico' />
      </Head>

      <Heading mb='2' as={'h1'} textAlign={'center'}>
      Elucidário Madeirense
      </Heading>
      <Text>
        Explore the rich history and culture of Madeira through a comprehensive
        collection of articles. Start browsing through various topics on flora,
        fauna, geography, and notable figures of Madeira from 1920-ies.
      </Text>
      
    </>
  )
}
