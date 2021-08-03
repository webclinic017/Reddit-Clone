import React from 'react';
import { useIsMemberToggle } from '../../hooks/useIsMemberToggle';
import { Box, Text, Heading, IconButton, Button } from '@chakra-ui/react';
import { AddIcon, CheckIcon } from '@chakra-ui/icons';

import { Link } from 'react-router-dom';
import '../../styles/groupCard.css';

export interface Group {
  createdBy: string;
  groupName: string;
  description: string;
}

interface GroupCardProps {
  group: Group;
}

function GroupCard({ group }: GroupCardProps) {
  const { isMember, toggleMembership } = useIsMemberToggle(group.groupName);
  const iconColorScheme = isMember ? 'green' : 'blue';

  return (
    <Box
      maxW="md"
      minW="sm"
      className="groupsCard"
      padding="6"
      boxShadow="lg"
      bg="white"
    >
      <div className="groupCard__main">
        <Heading as="h3" size="lg">
          {group.groupName}
        </Heading>
        <Text>{group.description}</Text>
      </div>
      <div className="groupCard__bottom">
        <IconButton
          colorScheme={iconColorScheme}
          onClick={() => toggleMembership()}
          aria-label="join this group"
          icon={isMember ? <CheckIcon /> : <AddIcon />}
        />
        <Button>
          <Link to={`/groups/${group.groupName}`}>Visit Group Page</Link>
        </Button>
      </div>
    </Box>
  );
}

export default GroupCard;
