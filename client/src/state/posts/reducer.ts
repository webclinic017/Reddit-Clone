import { PostState, PostAction } from './types';

export const initialPostState: PostState = {
  feed: [],
};

export function postsReducer(
  state: PostState = initialPostState,
  action: PostAction
): PostState {
  switch (action.type) {
    case 'FETCH_POSTS':
      return { ...state, [action.payload.groupName]: action.payload.posts };
    case 'CREATE_POST':
      return { ...state, [action.payload.groupName]: action.payload.posts };
    case 'LOGOUT':
      return { feed: [] };
    default:
      return state;
  }
}
