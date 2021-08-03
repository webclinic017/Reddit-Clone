import { LoginFormError, LoginFormValues } from '../components/forms/LoginForm';

export function validateLoginForm(formValues: LoginFormValues): LoginFormError {
  const { email, password } = formValues;
  if (email === '') return 'Email not provided';
  if (password === '') return 'Password not provided';
  return null;
}
