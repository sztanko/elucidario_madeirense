import Head from 'next/head'
import { Heading, Text, Link, UnorderedList, ListItem } from '@chakra-ui/react'
import { AppLayout } from '@/components/layout/AppLayout'

export default function AboutProjectRu () {
  return (
    <>
      <Head>
        <title>О проекте - Elucidario Madeirense</title>
      </Head>
      <AppLayout locale='ru'>
        <Heading as='h1' size='xl' mb={4}>
          О проекте
        </Heading>
        <Text mb={4}>
          Будучи благодарным за волшебные моменты и теплое гостеприимство, которые я
          испытал на солнечном острове Мадейра и среди его жителей, я чувствую
          сердечное обязательство сохранить и распространить исторический вклад
          его выдающихся мыслителей наиболее доступным способом этой цифровой
          эпохи. Этот веб-сайт - личная инициатива, которая была осуществлена в
          моем свободном времени без какого-либо финансирования. Он является
          открытым исходным кодом, и код доступен здесь:{' '}
          <Link
            href='https://github.com/sztanko/elucidario_madeirense'
            isExternal
          >
            https://github.com/sztanko/elucidario_madeirense
          </Link>
          .
        </Text>
        <Text mb={4}>
          Все статьи на этом сайте происходят из PDF-версий книги, поскольку у
          меня нет доступа к оригиналу. Я старался исправить большинство ошибок,
          возникших в результате оптического распознавания символов, но не могу
          гарантировать, что все они были устранены. Иногда некоторые статьи
          объединяются в одну.
        </Text>
        <Text mb={4}>
          Для форматирования и дальнейшего перевода текста были использованы
          большие языковые модели, такие как ChatGPT и Claude. Я признаю, что ни
          один из методов не идеален, и иногда в переводе и верстке возникают
          значительные ошибки. Однако я планирую переработать содержимое, как
          только модели улучшатся. Все изображения также были созданы с помощью
          технологий искусственного интеллекта.
        </Text>
        <Text mb={4}>
          Меня зовут Дима, я живу в Лондоне, и меня глубоко интересует
          культура и история Мадейры. Я не историк, и я не говорю
          по-португальски (хотя я учусь). Пожалуйста, свяжитесь со мной по
          электронной почте по адресу{' '}
          <Link href='mailto:sztanko@gmail.com'>sztanko@gmail.com</Link>.
        </Text>
        <Text mb={4}>Я хотел бы выразить свою благодарность:</Text>
        <UnorderedList mb={4}>
          <ListItem>
            Дуарте В. Р. Афонсу (
            <Link
              href='https://www.scribd.com/user/31817682/Duarte-V-R-Afonso'
              isExternal
            >
              https://www.scribd.com/user/31817682/Duarte-V-R-Afonso
            </Link>
            ) за загрузку PDF-версий оригинальной книги.
          </ListItem>
          <ListItem>
            Разработчикам современных больших языковых моделей за то, что
            позволили мне взяться за задачи, которые казались недостижимыми
            всего год назад.
          </ListItem>
          <ListItem>
            Моей жене и сыну за бесконечное терпение, которое они проявляли,
            пока я разрабатывал этот веб-сайт.
          </ListItem>
        </UnorderedList>
      </AppLayout>
    </>
  )
}