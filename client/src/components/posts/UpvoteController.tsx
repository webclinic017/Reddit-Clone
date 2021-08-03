import React, { useState, useEffect } from 'react';
import { IconButton, Text, CircularProgress } from '@chakra-ui/react';
import { ArrowUpIcon } from '@chakra-ui/icons';
import { fetchUpvoteCount, addUpvote, removeUpvote } from '../../API/posts';
import { useTypedSelector } from '../../hooks/useTypedSelector';

interface UpvoteControllerProps {
  postId: string;
}

function UpvoteController({ postId }: UpvoteControllerProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [upvotedByMe, setUpvotedByMe] = useState(false);
  const [count, setCount] = useState(0);
  const { token } = useTypedSelector((state) => state.user);

  // fetch the number of upvotes for post
  useEffect(() => {
    (async () => {
      if (token === null) return;

      try {
        const res = await fetchUpvoteCount(postId, token as string);
        setCount(res.data.upvotes);
      } catch (error) {
        setCount(0);
      }
      setIsLoading(false);
    })();
  }, [token, postId]);

  // fetch if the post has been upvoted by current user
  useEffect(() => {
    (async () => {})();
  }, [token, postId]);

  async function onClick() {
    const newIsUpvotedStatus = !upvotedByMe;

    if (newIsUpvotedStatus) {
      if (await addUpvote(postId, token as string)) {
        setCount((prevCount) => prevCount + 1);
      }
    } else {
      if (await removeUpvote(postId, token as string)) {
        setCount((prevCount) => prevCount - 1);
      }
    }

    setUpvotedByMe(newIsUpvotedStatus);
  }

  function renderLoading() {
    return <CircularProgress size="5" isIndeterminate color="blue.300" />;
  }

  return (
    <div className="up">
      <IconButton
        onClick={onClick}
        aria-label="upvote"
        isRound
        size="sm"
        colorScheme={upvotedByMe ? 'green' : ''}
        variant={upvotedByMe ? 'solid' : 'ghost'}
        icon={<ArrowUpIcon w={5} h={5} />}
        marginRight="5px"
      />

      <Text size="md">{isLoading ? renderLoading() : count}</Text>
    </div>
  );
}

export default UpvoteController;
