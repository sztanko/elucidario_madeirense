import Head from 'next/head'
import { Box, Container, Heading, Text, Link } from '@chakra-ui/react'
import { useTranslation } from 'next-i18next' // or your i18n library's hook

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
      <Container maxW='container.md' centerContent>
        <Box
        backgroundColor="rgba(255, 255, 255, 0.5)"
        p={{ base: 4, md: 8 }} // Responsive padding
        m={{ base: 4, md: 8 }} // Responsive margin
        >
          <Heading mb='2' as={"h1"} textAlign={"center"}>Elucidario Madeirense</Heading>
          <Text>
            Explore the rich history and culture of Madeira through a
            comprehensive collection of articles. Start browsing through various
            topics on flora, fauna, geography, and notable figures of Madeira.
          </Text>
          {/* Add more content, links or structure as needed */}
        </Box>
      </Container>
    </>
  )
}
