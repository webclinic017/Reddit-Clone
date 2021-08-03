import React from 'react';
import { Link } from 'react-router-dom';
import RegisterForm from '../forms/RegisterForm';
import { Heading, Text } from '@chakra-ui/react';
import '../../styles/registerScreen.css';

function RegisterScreen() {
  return (
    <div className="registerScreen">
      <div className="registerScreen__left"></div>
      <div className="registerScreen__right">
        <div className="heading">
          <Heading as="h3" size="lg">
            Welcome! Create an Account
          </Heading>
        </div>
        <div className="formWrapper">
          <RegisterForm />
        </div>
        <div className="loginLinkContainer">
          <Text>Already have an account?</Text>
          <Link className="loginLink" to="/login">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}

export default RegisterScreen;
