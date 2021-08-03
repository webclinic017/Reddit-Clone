import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import { alertsReducers } from './alerts/reducer';
import { userReducer } from './user/reducer';
import { postsReducer } from './posts/reducer';
import { GroupsReducer } from './groups/reducer';

const rootReducer = combineReducers({
  alerts: alertsReducers,
  user: userReducer,
  posts: postsReducer,
  groups: GroupsReducer,
});

export type RootReducerType = ReturnType<typeof rootReducer>;

export const store = createStore(rootReducer, {}, applyMiddleware(thunk));
