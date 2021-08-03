import React, { useState } from 'react';
import UserAvatarCard from './UserAvatarCard';
import history from '../../history';
import { Button, Spinner } from '@chakra-ui/react';
import { logoutWithApi } from '../../API/auth';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { useUserActions } from '../../hooks/useUserAction';
import '../../styles/navBar.css';

function NavBar() {
  const [isLoading, setIsLoading] = useState(false);
  const { logoutAction } = useUserActions();
  const { token } = useTypedSelector((state) => state.user);

  async function onLogoutClick() {
    setIsLoading(true);
    const didLogOut = await logoutWithApi(token as string);
    if (didLogOut) {
      logoutAction();
    }
    setIsLoading(false);
  }

  return (
    <nav className="navBar">
      <div className="navBar__left">
        <UserAvatarCard />
      </div>
      <div className="navBar__middle">
        <Button
          className="navItem"
          onClick={() => history.push('/groups/explore')}
        >
          Explore Groups
        </Button>
        <Button className="navItem" onClick={() => history.push('/')}>
          My Feed
        </Button>
      </div>
      <div className="navBar__right">
        <Button colorScheme="blue" size="md" onClick={onLogoutClick}>
          {isLoading ? <Spinner size="md" /> : 'Logout'}
        </Button>
      </div>
    </nav>
  );
}

export default NavBar;
