import React from 'react';
import UserTag from '../general/UserTag';
import { Box, Text } from '@chakra-ui/react';
import { formatDate } from '../../utils/date';
import '../../styles/postCard.css';

export interface Response {
  createdAt: number;
  postId: string;
  response: string;
  responseId: string;
  postedBy: string;
}

interface ResponseCardProps {
  response: Response;
}

function ResponseCard({ response }: ResponseCardProps) {
  return (
    <Box margin="3" padding="6" boxShadow="lg" borderRadius="8" bg="white">
      <Box className="postCard__top">
        <Text>
          <UserTag userId={response.postedBy} /> Responded:
        </Text>
        <div className="date">{formatDate(response.createdAt * 1000)}</div>
      </Box>
      <Box className="postCard__middle" margin="18px 0">
        <Text fontSize="lg">{response.response}</Text>
      </Box>
    </Box>
  );
}

export default ResponseCard;
