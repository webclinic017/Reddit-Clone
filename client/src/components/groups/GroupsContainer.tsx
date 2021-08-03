import React, { useState, useEffect } from 'react';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { Box } from '@chakra-ui/react';
import GroupCardPlaceholder from './GroupCardPlaceholder';
import { fetchGroups } from '../../API/groups';
import { useGroupActions } from '../../hooks/useGroupActions';
import GroupCard from './GroupCard';

function GroupsContainer() {
  const [isLoading, setIsLoading] = useState(true);
  const {
    user: { token },
    groups: { groups },
  } = useTypedSelector((state) => state);
  const { fetchGroupsAction } = useGroupActions();

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchGroups(token as string);
        fetchGroupsAction(res.data.groups);
      } catch (error) {
        console.log(error);
      }
      setIsLoading(false);
    })();
  }, [token, fetchGroupsAction]);

  function renderPlaceholders() {
    const placeholders = [0, 1, 2, 3, 4, 5, 6, 7];
    return placeholders.map((num) => <GroupCardPlaceholder key={num} />);
  }

  function renderGroups() {
    return groups.map((group) => <GroupCard group={group} />);
  }

  return (
    <Box
      className="groupsContainer"
      margin="4"
      padding="6"
      boxShadow="lg"
      borderRadius="8"
      bg="white"
    >
      {isLoading ? renderPlaceholders() : renderGroups()}
    </Box>
  );
}

export default GroupsContainer;
