import { Group } from './types';

export function fetchGroupsAction(groups: Group[]) {
  return {
    type: 'FETCH_GROUPS',
    payload: {
      groups,
    },
  };
}

export function createGroupsAction(groups: Group[]) {
  return {
    type: 'CREATE_GROUP',
    payload: {
      groups,
    },
  };
}
