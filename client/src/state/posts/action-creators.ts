import { Post } from './types';

export function fetchPostsAction(groupName: string, posts: Post[]) {
  return {
    type: 'FETCH_POSTS',
    payload: {
      groupName,
      posts,
    },
  };
}

export function createPostAction(groupName: string, posts: Post[]) {
  return {
    type: 'CREATE_POST',
    payload: {
      groupName,
      posts,
    },
  };
}
