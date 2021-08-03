import React from 'react';
import { Text, Heading, Box } from '@chakra-ui/react';

export interface GroupInfo {
  created_by: string;
  description: string;
  groupId: string;
  groupName: string;
}

interface GroupHeaderProps {
  groupInfo: GroupInfo;
}

function GroupHeader({ groupInfo }: GroupHeaderProps) {
  return (
    <Box
      className="postCard__middle"
      margin="4"
      padding="6"
      boxShadow="lg"
      borderRadius="8"
      bg="white"
    >
      <Heading as="h3" size="lg">
        {groupInfo?.groupName}
      </Heading>
      <Text fontSize="lg">{groupInfo?.description}</Text>
    </Box>
  );
}

export default GroupHeader;
