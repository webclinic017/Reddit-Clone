import React, { useState } from 'react';
import { Box, Heading, Text, Button } from '@chakra-ui/react';
import NavBar from '../general/NavBar';
import Modal from '../general/Modal';
import '../../styles/exploreGroups.css';
import GroupsContainer from '../groups/GroupsContainer';
import CreateGroupForm from '../groups/CreateGroupForm';

function ExploreGroupsScreen() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="exploreGroupsScreen">
      <NavBar />
      <div className="exploreGroupsScreen__main">
        <Box
          className="exploreGroupsScreen__top"
          margin="4"
          padding="6"
          boxShadow="lg"
          borderRadius="8"
          bg="white"
        >
          <Heading as="h3" size="lg">
            Explore Groups
          </Heading>
          <Text fontSize="lg">Customize your feed by joining groups</Text>
          <Button onClick={() => setIsModalOpen(true)}>Create a Group</Button>
        </Box>
        <Modal isOpen={isModalOpen} closeModal={() => setIsModalOpen(false)}>
          <CreateGroupForm />
        </Modal>
        <div className="exploreGroupsScreen__bottom">
          <GroupsContainer />
        </div>
      </div>
    </div>
  );
}

export default ExploreGroupsScreen;
