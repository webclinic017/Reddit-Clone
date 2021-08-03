import React from 'react';
import { Box, SkeletonCircle, SkeletonText } from '@chakra-ui/react';

function GroupCardPlaceholder() {
  return (
    <Box
      maxW="md"
      minW="sm"
      className="groupsCardPlaceholder"
      padding="6"
      boxShadow="lg"
      bg="white"
    >
      <SkeletonCircle size="10" />
      <SkeletonText mt="4" noOfLines={4} spacing="4" />
    </Box>
  );
}

export default GroupCardPlaceholder;
