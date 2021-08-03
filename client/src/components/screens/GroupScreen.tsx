import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchGroupDetails } from '../../API/groups';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { useIsMemberToggle } from '../../hooks/useIsMemberToggle';
import ErrorAlert from '../alerts/ErrorAlert';
import NavBar from '../general/NavBar';
import PostFeed from '../posts/PostFeed';
import { GroupInfo } from '../groups/GroupHeader';
import { IconButton, Box, Heading, Text } from '@chakra-ui/react';
import { AddIcon, CheckIcon } from '@chakra-ui/icons';
import Modal from '../general/Modal';
import CreatePostForm from '../posts/CreatePostForm';
import { Button } from '@chakra-ui/react';
import '../../styles/groupScreen.css';

function GroupScreen() {
  const { name } = useParams<{ name: string }>();
  const { isMember, toggleMembership } = useIsMemberToggle(name);
  const [groupInfo, setGroupInfo] = useState<GroupInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isCreatePostModalOpen, setIsCreatePostModalOpen] = useState(false);
  const { token } = useTypedSelector((state) => state.user);
  const iconColorScheme = isMember ? 'green' : 'blue';

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchGroupDetails(name, token as string);
        setGroupInfo(res.data.group);
      } catch (error) {
        setError('An error occurred while fetch the group Detail');
      }
    })();
  }, [name, token]);

  function onCreatePostModalClose() {
    setIsCreatePostModalOpen(false);
  }

  return (
    <div className="groupScreen">
      <NavBar />
      <div className="groupScreen__main">
        {error && <ErrorAlert message={error} onClose={() => setError(null)} />}
        <div className="groupScreen__top">
          {groupInfo && (
            <Box
              className="postCard__middle"
              margin="4"
              padding="6"
              boxShadow="lg"
              borderRadius="8"
              bg="white"
            >
              <Heading as="h3" size="lg">
                {groupInfo?.groupName}
              </Heading>
              <Text fontSize="lg">{groupInfo?.description}</Text>
              <IconButton
                colorScheme={iconColorScheme}
                onClick={() => toggleMembership()}
                aria-label="join this group"
                icon={isMember ? <CheckIcon /> : <AddIcon />}
              />
              {isMember && (
                <Button onClick={() => setIsCreatePostModalOpen(true)}>
                  Share Post
                </Button>
              )}
            </Box>
          )}
        </div>

        {/* Modal for creating a new post */}
        <Modal
          isOpen={isCreatePostModalOpen}
          closeModal={onCreatePostModalClose}
        >
          {isCreatePostModalOpen && <CreatePostForm groupName={name} />}
        </Modal>

        <div className="groupScreen__bottom">
          <PostFeed groupName={name} />
        </div>
      </div>
    </div>
  );
}

export default GroupScreen;
