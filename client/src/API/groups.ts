import axios from 'axios';

const groups_service = axios.create({
  baseURL: `http://${process.env.REACT_APP_BASE_URL}/api/v1/groups`,
  timeout: 6000,
});

export async function fetchGroupDetails(groupName: string, token: string) {
  return await groups_service.get(`/${groupName}`, {
    params: {
      token: token,
    },
  });
}

export async function fetchGroups(token: string) {
  return await groups_service.get('', {
    params: {
      token: token,
    },
  });
}

export async function createGroup(
  name: string,
  description: string,
  token: string
) {
  return await groups_service.post('', {
    token: token,
    group: {
      name,
      description,
    },
  });
}

export async function fetchIsGroupMember(
  groupName: string,
  userId: string,
  token: string
) {
  return await groups_service.get(`/${groupName}/members/${userId}`, {
    params: {
      token: token,
    },
  });
}

export async function addGroupMembership(groupName: string, token: string) {
  return await groups_service.post(`/${groupName}/members`, {
    token: token,
  });
}

export async function deleteGroupMembership(groupName: string, token: string) {
  return await groups_service.delete(`/${groupName}/members`, {
    data: {
      token: token,
    },
  });
}
