import React from 'react';
import {
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  CloseButton,
} from '@chakra-ui/react';

interface ErrorAlertProps {
  message: string;
  onClose: () => void;
}

function ErrorAlert({ message, onClose }: ErrorAlertProps) {
  return (
    <Alert status="error">
      <AlertIcon />
      <AlertTitle mr={2}>Error!</AlertTitle>
      <AlertDescription>{message}</AlertDescription>
      <CloseButton
        position="absolute"
        right="8px"
        top="8px"
        onClick={onClose}
      />
    </Alert>
  );
}

export default ErrorAlert;
