import { User } from './types';

export function loginAction(user: User, token: string) {
  return {
    type: 'LOGIN',
    payload: {
      user,
      token,
    },
  };
}

export function registerAction(user: User, token: string) {
  return {
    type: 'REGISTER',
    payload: {
      user,
      token,
    },
  };
}

export function logoutAction() {
  return {
    type: 'LOGOUT',
  };
}
