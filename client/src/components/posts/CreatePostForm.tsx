import React, { useState } from 'react';
import TextFormField from '../forms/TextFormField';
import { Box, Textarea, Button } from '@chakra-ui/react';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { usePostActions } from '../../hooks/usePostActions';
import { createNewPost } from '../../API/posts';

interface CreatePostFormProps {
  groupName: string;
}

function CreatePostForm({ groupName }: CreatePostFormProps) {
  const [title, setTitle] = useState('');
  const [post, setPost] = useState('');
  const { createPostAction } = usePostActions();
  const [isLoading, setIsLoading] = useState(false);

  const {
    user: { token },
    posts: { [groupName]: posts },
  } = useTypedSelector((state) => state);

  async function onFormSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await createNewPost(title, post, groupName, token as string);

      setPost('');
      setTitle('');
      createPostAction(groupName, [res.data, ...posts]);
    } catch (error) {
      console.log('couldnt create post', error);
    }
    setIsLoading(false);
  }

  return (
    <Box margin="3" padding="6" boxShadow="lg" borderRadius="8" bg="white">
      <form className="postForm" onSubmit={onFormSubmit}>
        <TextFormField
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <Textarea
          placeholder="Write your post here..."
          value={post}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
            setPost(e.target.value)
          }
        />
        <Button
          type="submit"
          isLoading={isLoading}
          isDisabled={title.length === 0 || post.length === 0}
          colorScheme="blue"
        >
          Share Post
        </Button>
      </form>
    </Box>
  );
}

export default CreatePostForm;
