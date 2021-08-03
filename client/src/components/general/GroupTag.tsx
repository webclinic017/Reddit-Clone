import React from 'react';
import { Tag, TagLabel } from '@chakra-ui/react';
import history from '../../history';

interface GroupTagProps {
  groupName: string;
}

function GroupTag({ groupName }: GroupTagProps) {
  function onClick() {
    history.push(`/groups/${groupName}`);
  }

  return (
    <Tag size="md" colorScheme="green" borderRadius="full">
      <TagLabel onClick={onClick}>{groupName}</TagLabel>
    </Tag>
  );
}

export default GroupTag;
