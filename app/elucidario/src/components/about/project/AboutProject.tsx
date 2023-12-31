import { useTranslation } from 'react-i18next'
import Head from 'next/head'
import { Heading, Box, Image, Center } from '@chakra-ui/react'
import { AppLayout } from '@/components/layout/AppLayout'
import AboutProjectEn from './AboutProjectEn'
import AboutProjectPt from './AboutProjectPt'
import AboutProjectUk from './AboutProjectUk'
import AboutProjectDe from './AboutProjectDe'
import AboutProjectRu from './AboutProjectRu'

export const AboutProject = ({ locale }) => {
  const { t } = useTranslation('menu')
  var content = null
  if (locale === 'pt') content = <AboutProjectPt />
  else if (locale === 'de') content = <AboutProjectDe />
  else if (locale === 'ru') content = <AboutProjectRu />
  else if (locale === 'uk') content = <AboutProjectUk />
  else content = <AboutProjectEn />

  return (
    <>
      <Head>
        <title>{`${t('about_project')} - Elucidario Madeirense`}</title>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
      </Head>
      <AppLayout locale={locale}>
        <Center>
          <Image
            src={`${process.env.NEXT_PUBLIC_WEB_PATH}/home_icon.png`}
            alt='Elucidário Madeirense'
            align={'center'}
          />
        </Center>
        <Center>
          <Heading as='h1' size='xl' mb={4}>
            {t('about_project')}
          </Heading>
        </Center>
        <Box textAlign='justify'>{content}</Box>
      </AppLayout>
    </>
  )
}
