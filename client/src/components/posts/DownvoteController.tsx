import React, { useState, useEffect } from 'react';
import { IconButton, Text, CircularProgress } from '@chakra-ui/react';
import { ArrowDownIcon } from '@chakra-ui/icons';
import {
  fetchDownvoteCount,
  addDownvote,
  removeDownvote,
} from '../../API/posts';
import { useTypedSelector } from '../../hooks/useTypedSelector';

interface DownvoteControllerProps {
  postId: string;
}

function UpvoteController({ postId }: DownvoteControllerProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [downvotedByMe, setdownvotedByMe] = useState(false);
  const [count, setCount] = useState(0);
  const { token } = useTypedSelector((state) => state.user);

  // fetch the number of upvotes for post
  useEffect(() => {
    (async () => {
      if (token === null) return;

      try {
        const res = await fetchDownvoteCount(postId, token as string);
        setCount(res.data.downvotes);
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
    const newIsDownvotedStatus = !downvotedByMe;

    if (newIsDownvotedStatus) {
      if (await addDownvote(postId, token as string)) {
        setCount((prevCount) => prevCount + 1);
      }
    } else {
      if (await removeDownvote(postId, token as string)) {
        setCount((prevCount) => prevCount - 1);
      }
    }

    setdownvotedByMe(newIsDownvotedStatus);
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
        colorScheme={downvotedByMe ? 'red' : ''}
        variant={downvotedByMe ? 'solid' : 'ghost'}
        icon={<ArrowDownIcon w={5} h={5} />}
        marginRight="5px"
      />

      <Text size="md">{isLoading ? renderLoading() : count}</Text>
    </div>
  );
}

export default UpvoteController;
