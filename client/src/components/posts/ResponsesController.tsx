import React, { useState, useEffect } from 'react';
import ResponseList from './ResponseList';
import ErrorAlert from '../alerts/ErrorAlert';
import { Response } from './ResponseCard';
import { fetchResponsesForPost, createResponsesForPost } from '../../API/posts';
import { useTypedSelector } from '../../hooks/useTypedSelector';
import { Textarea, Button, Box } from '@chakra-ui/react';

interface ResponsesControllerProps {
  postId: string;
}

function ResponsesController({ postId }: ResponsesControllerProps) {
  const [responses, setResponses] = useState<Response[]>([]);
  const [responseMsg, setResponseMsg] = useState('');
  const [isSubmittingForm, setIsSubmittingForm] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { token } = useTypedSelector((state) => state.user);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchResponsesForPost(postId, token as string);
        setResponses(res.data);
      } catch (error) {
        setError('Unable to fetch the responses to this post');
      }
    })();
  }, [postId, token]);

  async function onResponseFormSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsSubmittingForm(true);

    try {
      const res = await createResponsesForPost(
        postId,
        responseMsg,
        token as string
      );
      setResponses([res.data as Response, ...responses]);
    } catch (error) {
      setError('Unable to create your response');
    }

    setResponseMsg('');
    setIsSubmittingForm(false);
  }

  return (
    <div className="responsesController">
      {error && <ErrorAlert message={error} onClose={() => setError(null)} />}
      <Box margin="3" padding="6" boxShadow="lg" borderRadius="8" bg="white">
        <form className="responseForm" onSubmit={onResponseFormSubmit}>
          <Textarea
            placeholder="respond to this post..."
            value={responseMsg}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
              setResponseMsg(e.target.value)
            }
          />
          <Button
            type="submit"
            isLoading={isSubmittingForm}
            isDisabled={responseMsg.length === 0}
            colorScheme="blue"
          >
            create response
          </Button>
        </form>
      </Box>
      <div className="responses">
        <ResponseList responses={responses} />
      </div>
    </div>
  );
}

export default ResponsesController;
