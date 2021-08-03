export interface Group {
  createdBy: string;
  groupName: string;
  description: string;
}

export interface GroupState {
  groups: Group[];
}

export interface GroupAction {
  type: string;
  payload: any;
}
