import {
  RegisterFormError,
  RegisterFormValues,
} from '../components/forms/RegisterForm';

export function validateRegisterForm(
  formValues: RegisterFormValues
): RegisterFormError {
  const { username, email, password, confirmPassword } = formValues;
  if (username === '') return 'username not provided';
  if (email === '') return 'Email not provided';
  if (password === '') return 'Password not provided';
  if (confirmPassword === '') return 'Confirm Password not provided';
  if (confirmPassword !== password) return 'Passwords do not match';
  return null;
}
