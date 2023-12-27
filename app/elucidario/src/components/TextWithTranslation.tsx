import { Text } from '@chakra-ui/react'

export const TextWithTranslation = ({ text, originalText }) => {
  return (
    <Text>
      {text}
      {text !== originalText && (
        <Text as='span' color={'#777'} display={'inline'} fontSize={"smaller"}>
          {' '}
          / {originalText}
        </Text>
      )}
    </Text>
  )
}
