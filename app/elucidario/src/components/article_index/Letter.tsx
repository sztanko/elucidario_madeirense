import React from 'react'
import { Box, Text } from '@chakra-ui/react'
import { LoLink } from '../LoLink'
import { TextWithTranslation } from '../TextWithTranslation'
import { ArticleIndexItem } from '@/models/ArticleIndexItem'

interface LetterProps {
  letter: string
  articles: ArticleIndexItem[],
  showLetter?: boolean
}

export const Letter: React.FC<LetterProps> = ({
  letter,
  articles,
  showLetter
}: LetterProps) => {

  const sortedArticles = articles.sort((a, b) => a.title.localeCompare(b.title))
  
  return (
    <Box width='100%'>
      {showLetter && <Text
        as='h2'
        id={letter}
        fontSize={30}
        textAlign={'left'}
        marginBottom={2}
        fontWeight={'bold'}
      >
        {letter} ({articles.length})
      </Text>}
      <Box
        as='dl'
        paddingX={4}
        width='100%'
        style={{
          columnWidth: '300px',
          columnGap: '1rem' // or any other spacing you prefer
        }}
      >
        {sortedArticles.map((article, index) => (
          <Box
            as='dd'
            key={index}
            fontSize='md'
            marginLeft={4}
            lineHeight={'150%'}
          >
            <LoLink href={`/articles/${article.id}`}>
              <TextWithTranslation
                text={article.title}
                originalText={article.original_title}
              />{' '}
            </LoLink>
          </Box>
        ))}
      </Box>
    </Box>
  )
}
