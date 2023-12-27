import React from 'react';
import { Box, Text } from '@chakra-ui/react';
import _ from 'lodash';
import { Glossary } from '@/models/Glossary';


interface EnumListProps {
    name: string;
    data: Glossary;
  }

  export const EnumList: React.FC<EnumListProps> = ({ name, data }) => {
    const sortedData = _(data).toPairs().sortBy(0).fromPairs().value();

    return (
      <Box as="section" marginY={4}>
        <Text as="h2" fontSize="xl" marginBottom={4} fontWeight={"bold"}>{name}</Text>
        <Box as="dl" paddingX={4}>
          {Object.entries(sortedData).map(([key, values]) => (
            <React.Fragment key={key}>
              <Text as="dt" fontWeight="bold" fontSize="lg">{key}</Text>
              {values.map((value, index) => (
                <Text as="dd" key={index} fontSize="md" marginLeft={4}>{value}</Text>
              ))}
            </React.Fragment>
          ))}
        </Box>
      </Box>
    );
  };