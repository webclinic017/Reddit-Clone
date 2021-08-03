import React, { useState, useEffect } from 'react';
import { Tag, TagLabel } from '@chakra-ui/react';
import { fetchUsername } from '../../API/auth';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { CircularProgress } from '@chakra-ui/react';

interface UserTagProps {
  userId: string;
}

function UserTag({ userId }: UserTagProps) {
  const [username, setUsername] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { token } = useTypedSelector((state) => state.user);

  // when component mounts, fetch the username for the user that created
  // the post
  useEffect(() => {
    if (token === null) return;

    (async () => {
      try {
        const res = await fetchUsername(userId, token as string);
        setUsername(res.data.username[0].username);
      } catch (error) {
        console.log(error.response);
      }
      setIsLoading(false);
    })();
  }, [userId, token]);

  function renderLoading() {
    return <CircularProgress size="5" isIndeterminate color="blue.300" />;
  }

  return (
    <Tag size="md" colorScheme="blue" borderRadius="full">
      <TagLabel>{isLoading ? renderLoading() : username}</TagLabel>
    </Tag>
  );
}

export default UserTag;
