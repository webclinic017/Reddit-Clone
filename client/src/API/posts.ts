import axios from 'axios';

const posts_service = axios.create({
  baseURL: `http://${process.env.REACT_APP_BASE_URL}/api/v1/posts`,
  timeout: 6000,
});

export async function fetchUserFeed(token: string) {
  return await posts_service.get('/feed', {
    params: {
      token: token,
    },
  });
}

export async function fetchGroupsPostFeed(groupName: string, token: string) {
  return await posts_service.get('', {
    params: {
      group: groupName,
      token: token,
    },
  });
}

export async function createNewPost(
  title: string,
  post: string,
  groupName: string,
  token: string
) {
  return await posts_service.post('', {
    post: {
      title,
      post,
      groupName,
    },
    token: token,
  });
}

export async function fetchUpvoteCount(postId: string, token: string) {
  return await posts_service.get(`/${postId}/upvotes/count`, {
    params: {
      token: token,
    },
  });
}

export async function addUpvote(postId: string, token: string) {
  return await posts_service
    .post(`/${postId}/upvotes`, {
      token: token,
    })
    .then(() => true)
    .catch(() => false);
}

export async function removeUpvote(postId: string, token: string) {
  return await posts_service
    .delete(`/${postId}/upvotes`, {
      data: { token: token },
    })
    .then(() => true)
    .catch(() => false);
}

export async function fetchDownvoteCount(postId: string, token: string) {
  return await posts_service.get(`/${postId}/downvotes/count`, {
    params: {
      token: token,
    },
  });
}

export async function addDownvote(postId: string, token: string) {
  return await posts_service
    .post(`/${postId}/downvotes`, {
      token: token,
    })
    .then(() => true)
    .catch(() => false);
}

export async function removeDownvote(postId: string, token: string) {
  return await posts_service
    .delete(`/${postId}/downvotes`, {
      data: { token: token },
    })
    .then(() => true)
    .catch(() => false);
}

export async function fetchIfUserUpvotedPost(postId: string, token: string) {
  return await posts_service.get(`/${postId}/upvotes`, {
    params: {
      token: token,
    },
  });
}

export async function fetchResponsesForPost(postId: string, token: string) {
  return await posts_service.get(`/${postId}/responses`, {
    params: {
      token: token,
    },
  });
}

export async function createResponsesForPost(
  postId: string,
  response: string,
  token: string
) {
  return await posts_service.post(`/${postId}/responses`, {
    token: token,
    response: response,
  });
}
