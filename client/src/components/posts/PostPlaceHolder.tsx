import React from 'react';
import { Box, SkeletonCircle, SkeletonText } from '@chakra-ui/react';

function PostPlaceHolder() {
  return (
    <Box margin="3" padding="6" boxShadow="lg" borderRadius="8" bg="white">
      <SkeletonCircle size="10" />
      <SkeletonText mt="4" noOfLines={4} spacing="4" />
    </Box>
  );
}

export default PostPlaceHolder;
