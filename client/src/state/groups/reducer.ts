import { GroupState, GroupAction } from './types';

export const initialGroupState: GroupState = {
  groups: [],
};

export function GroupsReducer(
  state: GroupState = initialGroupState,
  action: GroupAction
): GroupState {
  switch (action.type) {
    case 'FETCH_GROUPS':
      return { ...state, groups: action.payload.groups };
    case 'CREATE_GROUP':
      return { ...state, groups: action.payload.groups };
    default:
      return state;
  }
}
