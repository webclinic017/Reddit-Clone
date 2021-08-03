import React, { useState, useEffect } from 'react';
import PostPlaceHolder from './PostPlaceHolder';
import { fetchUserFeed, fetchGroupsPostFeed } from '../../API/posts';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import Modal from '../general/Modal';
import PostDetail from './PostDetail';
import ErrorAlert from '../alerts/ErrorAlert';
import PostCard from './PostCard';
import { Post } from '../../state';
import { usePostActions } from '../../hooks/usePostActions';
import '../../styles/postList.css';

interface PostFeedProps {
  groupName: string;
}

function PostFeed({ groupName }: PostFeedProps) {
  // const [posts, setPosts] = useState<Post[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  const { fetchPostsAction } = usePostActions();

  const {
    user: { token },
    posts: { [groupName]: posts },
  } = useTypedSelector((state) => state);

  useEffect(() => {
    // fetch the users feed when the component mounts
    (async () => {
      if (token === null) return;

      try {
        if (groupName !== 'feed') {
          const res = await fetchGroupsPostFeed(groupName, token as string);
          fetchPostsAction(groupName, res.data);
        } else {
          const res = await fetchUserFeed(token as string);
          fetchPostsAction('feed', res.data);
        }
      } catch (error) {
        setError(
          error?.response?.data?.error ||
            'An error occurred while creating your feed'
        );
      }
      setIsLoading(false);
    })();
  }, [groupName, token, fetchPostsAction]);

  function onPostDetailClick(post: Post) {
    setSelectedPost(post);
    setIsDetailModalOpen(true);
  }

  function onDetailModalClose() {
    setIsDetailModalOpen(false);
    setSelectedPost(null);
  }

  function renderPosts() {
    return posts
      .sort((a, b) => b.createdAt - a.createdAt)
      .map((post: Post) => (
        <PostCard
          key={post.postId}
          post={post}
          onPostDetailClick={onPostDetailClick}
        />
      ));
  }

  function renderPlaceHolders() {
    const placeHolders = [];
    for (let i = 0; i < 8; i++) {
      placeHolders.push(<PostPlaceHolder key={i} />);
    }

    return placeHolders;
  }

  return (
    <div className="postListWrapper">
      {/* Modal for displaying post details */}
      <Modal isOpen={isDetailModalOpen} closeModal={onDetailModalClose}>
        {selectedPost && <PostDetail post={selectedPost} />}
      </Modal>
      <div className="postList">
        {error && <ErrorAlert message={error} onClose={() => setError(null)} />}

        {isLoading ? renderPlaceHolders() : renderPosts()}
      </div>
    </div>
  );
}

export default PostFeed;
