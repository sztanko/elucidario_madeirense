import { Text, Link, UnorderedList, ListItem } from '@chakra-ui/react'

export default function AboutProjectEn () {
  return (
    <>
      <Text mb={4}>
        In appreciation of the enchanting moments and warm hospitality I&apos;ve
        experienced on the sunny island of Madeira and its inhabitants, I am
        compelled by a heartfelt duty to preserve and disseminate the historical
        contributions of its most distinguished thinkers in the most accessible
        manner of this digital age. This website is a personal endeavor,
        undertaken in my free time without any funding. It is open source, and
        the code is available here:{' '}
        <Link
          href='https://github.com/sztanko/elucidario_madeirense'
          isExternal
        >
          https://github.com/sztanko/elucidario_madeirense
        </Link>
        .
      </Text>
      <Text mb={4}>
        All articles on this site are derived from PDF versions of the book, as
        I do not have access to the original. While I have strived to correct
        most errors resulting from optical character recognition, I cannot
        guarantee that all have been addressed. Occasionally, some articles
        merge into one.
      </Text>
      <Text mb={4}>
        For formatting and subsequent translation of the text, Large Language
        Models such as ChatGPT and Claude were employed. I acknowledge that
        neither method is flawless, and sometimes significant mistakes occur in
        translation and layout. However, I plan to reprocess the content as the
        models improve. All images were also generated using AI technology.
      </Text>
      <Text mb={4}>
        My name is Dimi, residing in London, UK, and I am deeply fascinated by
        Madeiran culture and history. I am not a historian, nor do I speak
        Portuguese (though I am learning). Feel free to contact me via email at{' '}
        <Link href='mailto:sztanko@gmail.com'>sztanko@gmail.com</Link>.
      </Text>
      <Text mb={4}>I would like to extend my gratitude to:</Text>
      <UnorderedList mb={4}>
        <ListItem>
          Duarte V R Afonso (
          <Link
            href='https://www.scribd.com/user/31817682/Duarte-V-R-Afonso'
            isExternal
          >
            https://www.scribd.com/user/31817682/Duarte-V-R-Afonso
          </Link>
          ) for uploading the PDF versions of the original book.
        </ListItem>
        <ListItem>
          The developers of modern Large Language Models for enabling me to
          undertake tasks that seemed unattainable just a year ago.
        </ListItem>
        <ListItem>
          My wife and son for the boundless patience they have shown while I
          have been developing this website.
        </ListItem>
      </UnorderedList>
    </>
  )
}
