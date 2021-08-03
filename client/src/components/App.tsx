import React from 'react';
import history from '../history';
import RegisterScreen from './screens/RegisterScreen';
import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import GroupScreen from './screens/GroupScreen';
import ExploreGroupsScreen from './screens/ExploreGroupsScreen';
import PageNotFound from './screens/PageNotFound';
import PrivateRoute from './general/PrivateRoute';
import { UserDataLayer } from './general/UserDataLayer';
import { Router, Switch, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from '../state';
import { ChakraProvider } from '@chakra-ui/react';
import '../styles/index.css';

function App() {
  return (
    <ChakraProvider>
      <Provider store={store}>
        <div className="app">
          <UserDataLayer>
            <Router history={history}>
              <Switch>
                <Route exact path="/login" component={LoginScreen} />
                <Route exact path="/register" component={RegisterScreen} />
                <PrivateRoute exact path="/">
                  <HomeScreen />
                </PrivateRoute>
                <PrivateRoute exact path="/groups/explore">
                  <ExploreGroupsScreen />
                </PrivateRoute>
                <PrivateRoute exact path="/groups/:name">
                  <GroupScreen />
                </PrivateRoute>
                <Route path="*" component={PageNotFound} />
              </Switch>
            </Router>
          </UserDataLayer>
        </div>
      </Provider>
    </ChakraProvider>
  );
}

export default App;
