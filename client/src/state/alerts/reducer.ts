import {
  AlertState,
  AlertActionType,
  ERROR_ALERT,
  INFO_ALERT,
  WARNING_ALERT,
  SUCCESS_ALERT,
  CLEAR_ALERT,
} from './types';

const initialState: AlertState = {
  errorMessage: '',
  infoMessage: '',
  warningMessage: '',
  successMessage: '',
};

export const alertsReducers = (
  state: AlertState = initialState,
  action: AlertActionType
): AlertState => {
  switch (action.type) {
    case ERROR_ALERT:
      return { ...state, errorMessage: action.payload };
    case INFO_ALERT:
      return { ...state, infoMessage: action.payload };
    case WARNING_ALERT:
      return { ...state, warningMessage: action.payload };
    case SUCCESS_ALERT:
      return { ...state, successMessage: action.payload };
    case CLEAR_ALERT:
      return initialState;
    default:
      return state;
  }
};
