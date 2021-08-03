import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useTypedSelector } from '../../hooks/useTypedSelector';

interface PrivateRouteProps {
  path: string;
  exact?: boolean;
  children: any;
}

function PrivateRoute({ children, path, exact }: PrivateRouteProps) {
  const { isSignedIn } = useTypedSelector((state) => state.user);

  return (
    <Route
      path={path}
      exact={exact}
      render={() => {
        return isSignedIn ? children : <Redirect to="/login" />;
      }}
    />
  );
}

export default PrivateRoute;
