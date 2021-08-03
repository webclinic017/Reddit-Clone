export interface User {
  userId: string;
  username: string;
  email: string;
}

export interface UserState {
  isSignedIn: boolean;
  user: User | null;
  token: string | null;
}

export interface UserAction {
  type: string;
  payload: any;
}
