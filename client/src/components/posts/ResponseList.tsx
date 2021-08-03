import React from 'react';
import ResponseCard, { Response } from './ResponseCard';
import { Heading } from '@chakra-ui/react';
import '../../styles/responseList.css';

interface ResponseListProps {
  responses: Response[];
}

function ResponseList({ responses }: ResponseListProps) {
  function renderResponses() {
    return responses
      .sort((a, b) => b.createdAt - a.createdAt)
      .map((response) => <ResponseCard response={response} />);
  }

  function renderNoResponsesMessage() {
    return (
      <Heading as="h5" size="md">
        Looks like no one has responded yet...
      </Heading>
    );
  }

  return (
    <div className="responseList">
      {responses.length ? renderResponses() : renderNoResponsesMessage()}
    </div>
  );
}

export default ResponseList;
