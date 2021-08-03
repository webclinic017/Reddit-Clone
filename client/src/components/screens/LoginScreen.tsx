import React from 'react';
import { Link } from 'react-router-dom';
import LoginForm from '../forms/LoginForm';
import { Heading, Text } from '@chakra-ui/react';
import '../../styles/loginScreen.css';

function LoginScreen() {
  return (
    <div className="loginScreen">
      <div className="loginScreen__left"></div>
      <div className="loginScreen__right">
        <div className="heading">
          <Heading as="h3" size="lg">
            Welcome Back! Sign In
          </Heading>
        </div>
        <div className="formWrapper">
          <LoginForm />
        </div>
        <div className="registerLinkContainer">
          <Text>Don't have an account?</Text>
          <Link className="registerLink" to="/register">
            Create one here
          </Link>
        </div>
      </div>
    </div>
  );
}

export default LoginScreen;
