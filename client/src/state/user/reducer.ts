import { UserState, UserAction } from './types';

export const initialUserState: UserState = {
  isSignedIn: false,
  user: null,
  token: null,
};

export function userReducer(
  state: UserState = initialUserState,
  action: UserAction
): UserState {
  switch (action.type) {
    case 'LOGIN':
      return {
        ...state,
        isSignedIn: true,
        user: action.payload.user,
        token: action.payload.token,
      };
    case 'REGISTER':
      return {
        ...state,
        isSignedIn: true,
        user: action.payload.user,
        token: action.payload.token,
      };
    case 'LOGOUT':
      return { ...state, isSignedIn: false, user: null, token: null };
    default:
      return state;
  }
}
