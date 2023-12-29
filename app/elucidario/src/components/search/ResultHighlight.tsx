import React from 'react';
import { Box, Text } from '@chakra-ui/react';

type ResultHighlightProps = {
  text: string;
  start: number;
  end: number;
  threshold: number;
};

export const ResultHighlight: React.FC<ResultHighlightProps> = ({ text, start, end, threshold }) => {
  // const words = text.split(' ');
  const startContext = Math.max(start - threshold, 0);
  const endContext = Math.min(end + threshold, text.length - 1);

  return (
    <Box fontStyle={"italic"}>
      ...{text.slice(startContext, start)}
      <Text as="span" color="blue.500" fontWeight="bold">
        {text.slice(start, end + 1)}
      </Text>
      {text.slice(end + 1, endContext + 1)}...
    </Box>
  );
};