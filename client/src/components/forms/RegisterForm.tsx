import React, { useState } from 'react';
import TextFormField from './TextFormField';
import EmailFormField from './EmailFormField';
import PasswordFormField from './PasswordFormField';
import ErrorAlert from '../alerts/ErrorAlert';
import { Button, Spinner } from '@chakra-ui/react';
import { validateRegisterForm } from '../../utils/register';
import { registerWithApi } from '../../API/auth';
import { useUserActions } from '../../hooks/useUserAction';
import history from '../../history';

export interface RegisterFormValues {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export type RegisterFormError = string | null;

function RegisterForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [formError, setFormError] = useState<RegisterFormError>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { registerAction } = useUserActions();

  async function onFormSubmit(
    e: React.FormEvent,
    formValues: RegisterFormValues
  ) {
    // prevent default form submission
    e.preventDefault();

    // reset the form error
    if (formError) setFormError(null);

    // check if there is a form error
    const error = validateRegisterForm(formValues);
    if (error !== null) {
      setFormError(error);
      return;
    }

    setIsLoading(true);

    try {
      const res = await registerWithApi(username, email, password);
      // make register request to API
      registerAction(res.data.user, res.data.token);
      setIsLoading(false);
      history.push('/');
    } catch (error) {
      setFormError(
        error?.response?.data?.error || 'Unable to Create New Account'
      );
      setIsLoading(false);
    }
  }

  return (
    <form
      method="POST"
      className="registerForm"
      onSubmit={(e) =>
        onFormSubmit(e, { username, email, password, confirmPassword })
      }
    >
      {formError && (
        <ErrorAlert message={formError} onClose={() => setFormError(null)} />
      )}
      <fieldset className="registerForm formFields">
        <TextFormField
          label={'Create Your Username'}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
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
        <PasswordFormField
          label="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </fieldset>
      <Button colorScheme="blue" type="submit">
        {isLoading ? <Spinner size="md" /> : 'Create Account'}
      </Button>
    </form>
  );
}

export default RegisterForm;
