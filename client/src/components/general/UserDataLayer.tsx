import React, { createContext, useContext, useReducer } from 'react';
import { initialUserState, userReducer } from '../../state/user/reducer';
import { UserState } from '../../state/user/types';

export const DataLayerContext = createContext<{
  state: UserState;
  dispatch: React.Dispatch<any>;
}>({ state: initialUserState, dispatch: () => null });

export const useDataLayerValue = () => useContext(DataLayerContext);

export const UserDataLayer: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(userReducer, initialUserState);
  return (
    <DataLayerContext.Provider value={{ state, dispatch }}>
      {children}
    </DataLayerContext.Provider>
  );
};
