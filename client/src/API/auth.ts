import axios from 'axios';

const auth_service = axios.create({
  baseURL: `http://${process.env.REACT_APP_BASE_URL}/api/v1/auth`,
  timeout: 6000,
});

export async function loginWithApi(
  email: string,
  password: string
): Promise<any> {
  return await auth_service.post('/login', {
    user: {
      email: email,
      password: password,
    },
  });
}

export async function registerWithApi(
  username: string,
  email: string,
  password: string
): Promise<any> {
  return await auth_service.post('/register', {
    user: {
      email: email,
      username: username,
      password: password,
    },
  });
}

export async function logoutWithApi(token: string): Promise<boolean> {
  return await auth_service
    .post('/logout', {
      token: token,
    })
    .then(() => true)
    .catch((err) => {
      return false;
    });
}

export async function fetchUsername(userId: string, token: string) {
  return auth_service.get(`/user/${userId}`, {
    params: {
      token: token,
    },
  });
}
