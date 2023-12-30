import Head from 'next/head'
import { Heading, Text, Link, UnorderedList, ListItem } from '@chakra-ui/react'
import { AppLayout } from '@/components/layout/AppLayout'

export default function AboutProjectDe () {
  return (
    <>
      <Head>
        <title>Über dieses Projekt - Elucidario Madeirense</title>
      </Head>
      <AppLayout locale='de'>
        <Heading as='h1' size='xl' mb={4}>
          Über dieses Projekt
        </Heading>
        <Text mb={4}>
          In Anerkennung der bezaubernden Momente und der herzlichen
          Gastfreundschaft, die ich auf der sonnigen Insel Madeira und ihren
          Einwohnern erlebt habe, fühle ich mich aus tiefstem Herzen
          verpflichtet, die historischen Beiträge ihrer bedeutendsten Denker auf
          die zugänglichste Art und Weise dieses digitalen Zeitalters zu
          bewahren und zu verbreiten. Diese Website ist ein persönliches
          Unterfangen, das ich in meiner Freizeit ohne jegliche Finanzierung
          durchführe. Es ist Open Source, und der Code ist hier verfügbar:{' '}
          <Link
            href='https://github.com/sztanko/elucidario_madeirense'
            isExternal
          >
            https://github.com/sztanko/elucidario_madeirense
          </Link>
          .
        </Text>
        <Text mb={4}>
          Alle Artikel auf dieser Seite stammen von PDF-Versionen des Buches, da
          ich keinen Zugang zum Original habe. Während ich mich bemüht habe, die
          meisten Fehler, die durch optische Zeichenerkennung entstanden sind,
          zu korrigieren, kann ich nicht garantieren, dass alle behoben wurden.
          Gelegentlich verschmelzen einige Artikel zu einem.
        </Text>
        <Text mb={4}>
          Für die Formatierung und anschließende Übersetzung des Textes wurden
          Großsprachmodelle wie ChatGPT und Claude verwendet. Ich erkenne an,
          dass keine Methode fehlerfrei ist und manchmal erhebliche Fehler in
          der Übersetzung und im Layout auftreten. Ich plane jedoch, den Inhalt
          erneut zu verarbeiten, wenn sich die Modelle verbessern. Alle Bilder
          wurden ebenfalls mit Hilfe von KI-Technologie generiert.
        </Text>
        <Text mb={4}>
          Mein Name ist Dimi, ich wohne in London, UK, und ich bin tief
          fasziniert von der Madeiranischen Kultur und Geschichte. Ich bin kein
          Historiker und spreche auch kein Portugiesisch (obwohl ich es lerne).
          Sie können mich gerne per E-Mail unter{' '}
          <Link href='mailto:sztanko@gmail.com'>sztanko@gmail.com</Link>{' '}
          kontaktieren.
        </Text>
        <Text mb={4}>Ich möchte meine Dankbarkeit ausdrücken:</Text>
        <UnorderedList mb={4}>
          <ListItem>
            Duarte V R Afonso (
            <Link
              href='https://www.scribd.com/user/31817682/Duarte-V-R-Afonso'
              isExternal
            >
              https://www.scribd.com/user/31817682/Duarte-V-R-Afonso
            </Link>
            ) für das Hochladen der PDF-Versionen des Originalbuches.
          </ListItem>
          <ListItem>
            Den Entwicklern moderner Großsprachmodelle, die es mir ermöglicht
            haben, Aufgaben zu übernehmen, die noch vor einem Jahr unerreichbar
            schienen.
          </ListItem>
          <ListItem>
            Meiner Frau und meinem Sohn für die grenzenlose Geduld, die sie
            gezeigt haben, während ich diese Website entwickelt habe.
          </ListItem>
        </UnorderedList>
      </AppLayout>
    </>
  )
}
