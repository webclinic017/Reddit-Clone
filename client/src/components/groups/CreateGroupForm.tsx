import React, { useState } from 'react';
import TextFormField from '../forms/TextFormField';
import { Box, Textarea, Button } from '@chakra-ui/react';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { useGroupActions } from '../../hooks/useGroupActions';
import { createGroup } from '../../API/groups';

function CreateGroupForm() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const {
    user: { token },
    groups: { groups },
  } = useTypedSelector((state) => state);
  const { createGroupsAction } = useGroupActions();

  async function onFormSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await createGroup(name, description, token as string);
      createGroupsAction([res.data, ...groups]);
    } catch (error) {
      console.log('couldnt create Group', error);
    }
    setIsLoading(false);
  }

  return (
    <Box margin="3" padding="6" boxShadow="lg" borderRadius="8" bg="white">
      <form className="postForm" onSubmit={onFormSubmit}>
        <TextFormField
          label="Group Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Textarea
          placeholder="group description..."
          value={description}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
            setDescription(e.target.value)
          }
        />
        <Button
          type="submit"
          isLoading={isLoading}
          isDisabled={name.length === 0 || description.length === 0}
          colorScheme="blue"
        >
          Create Group
        </Button>
      </form>
    </Box>
  );
}

export default CreateGroupForm;
