import React from 'react';
import { Avatar, Text, Heading } from '@chakra-ui/react';
import '../../styles/userAvatarCard.css';
import { useTypedSelector } from '../../hooks/useTypedSelector';

function UserAvatarCard() {
  const { user } = useTypedSelector((state) => state.user);

  if (user === null) return null;

  return (
    <div className="userAvatarCard">
      <div className="userAvatarCard__left">
        <Avatar name={user.username} />
      </div>
      <div className="userAvatarCard__right">
        <Heading as="h5" size="sm">
          {user.username}
        </Heading>
        <Text fontSize="md">{user.email}</Text>
      </div>
    </div>
  );
}

export default UserAvatarCard;
