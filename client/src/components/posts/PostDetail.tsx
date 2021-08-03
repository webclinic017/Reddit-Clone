import React from 'react';
import PostCard from './PostCard';
import ResponsesController from './ResponsesController';
import { Post } from '../../state';
import '../../styles/postDetail.css';

interface PostDetailProps {
  post: Post;
}

function PostDetail({ post }: PostDetailProps) {
  return (
    <div className="postDetail">
      <div className="postDetail__post">
        <PostCard post={post} />
      </div>
      <div className="postDetail__responseForm"></div>
      <div className="postDetail__responses">
        <ResponsesController postId={post.postId} />
      </div>
    </div>
  );
}

export default PostDetail;
