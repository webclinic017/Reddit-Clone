import React from 'react';
import UserTag from '../general/UserTag';
import GroupTag from '../general/GroupTag';
import UpvoteController from './UpvoteController';
import DownvoteController from './DownvoteController';
import { Box, Button, Text, Heading } from '@chakra-ui/react';
import { Post } from '../../state';
import { formatDate } from '../../utils/date';
import '../../styles/postCard.css';

interface PostCardProps {
  post: Post;
  onPostDetailClick?: (post: Post) => void;
}

function PostCard({ post, onPostDetailClick }: PostCardProps) {
  return (
    <Box margin="4" padding="6" boxShadow="lg" borderRadius="8" bg="white">
      <Box className="postCard__top">
        <Text>
          Posted By <UserTag userId={post.postedBy} /> In{' '}
          <GroupTag groupName={post.groupName} />
        </Text>
        <div className="date">{formatDate(post.createdAt * 1000)}</div>
      </Box>
      <Box className="postCard__middle" margin="18px 0">
        <Heading as="h3" size="md">
          {post.title}
        </Heading>
        <Text fontSize="md">{post.post}</Text>
      </Box>
      <Box className="postCard__bottom" margin="20px 0 0 0">
        <div className="votes">
          <UpvoteController postId={post.postId} />
          <DownvoteController postId={post.postId} />
        </div>
        {onPostDetailClick && (
          <div className="details">
            <Button size="sm" onClick={() => onPostDetailClick(post)}>
              View Post Details
            </Button>
          </div>
        )}
      </Box>
    </Box>
  );
}

export default PostCard;
