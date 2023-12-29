import React from 'react'
import { Box, Text, UnorderedList, ListItem } from '@chakra-ui/react'
import _ from 'lodash'
import { ResultHighlight } from './ResultHighlight'

// ResultHighlightList component
type ResultHighlightListProps = {
  indices: number[][]
  value: string
  threshold: number
}

export const ResultHighlightList: React.FC<ResultHighlightListProps> = ({
  indices,
  value,
  threshold
}) => {
    if (!indices) {
        return null
    }
    const maxLength = _.max(indices.map(([start, end]) => end - start))
    const topIndices = indices.filter(([start, end]) => end - start === maxLength)
  return (
    <UnorderedList styleType='none'>
      {topIndices.map(([start, end], index) => (
        <ListItem key={index}>
          <ResultHighlight
            text={value}
            start={start}
            end={end}
            threshold={threshold}
          />
        </ListItem>
      ))}
    </UnorderedList>
  )
}
