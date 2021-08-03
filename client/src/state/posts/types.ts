export interface Post {
  postId: string;
  groupName: string;
  title: string;
  post: string;
  createdAt: number;
  postedBy: string;
}

export interface PostState {
  [groupName: string]: Post[];
}

export interface PostAction {
  type: string;
  payload: any;
}
