import React, { useState } from 'react';
import EmailFormField from './EmailFormField';
import PasswordFormField from './PasswordFormField';
import ErrorAlert from '../alerts/ErrorAlert';
import { validateLoginForm } from '../../utils/login';
import { Button, Spinner } from '@chakra-ui/react';
import { useUserActions } from '../../hooks/useUserAction';
import { loginWithApi } from '../../API/auth';
import history from '../../history';

export interface LoginFormValues {
  email: string;
  password: string;
}

export type LoginFormError = string | null;

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState<LoginFormError>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { loginAction } = useUserActions();

  async function onFormSubmit(e: React.FormEvent, formValues: LoginFormValues) {
    // prevent default form submission
    e.preventDefault();

    // reset the form error
    if (formError) setFormError(null);

    // check if there is a form error
    const error = validateLoginForm({ email, password });
    if (error) {
      setFormError(error);
      return;
    }

    setIsLoading(true);

    try {
      const res = await loginWithApi(email, password);
      // make register request to API

      loginAction(res.data.user, res.data.token);
      setIsLoading(false);
      history.push('/');
    } catch (error) {
      setFormError(
        error?.response?.data?.error ||
          'Unable to login with provided credentials'
      );
      setIsLoading(false);
    }
  }

  return (
    <form
      method="POST"
      className="registerForm"
      onSubmit={(e) => onFormSubmit(e, { email, password })}
    >
      {formError && (
        <ErrorAlert message={formError} onClose={() => setFormError(null)} />
      )}
      <fieldset className="registerForm formFields">
        <EmailFormField
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <PasswordFormField
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </fieldset>
      <Button colorScheme="blue" type="submit">
        {isLoading ? <Spinner size="md" /> : 'Sign In'}
      </Button>
    </form>
  );
}

export default LoginForm;
