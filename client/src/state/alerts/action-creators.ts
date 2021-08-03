import {
  AlertActionType,
  ERROR_ALERT,
  INFO_ALERT,
  WARNING_ALERT,
  SUCCESS_ALERT,
  CLEAR_ALERT,
} from './types';

export const createErrorAlert = (message: string): AlertActionType => {
  return {
    type: ERROR_ALERT,
    payload: message,
  };
};

export const createInfoAlert = (message: string): AlertActionType => {
  return {
    type: INFO_ALERT,
    payload: message,
  };
};

export const createWarningAlert = (message: string): AlertActionType => {
  return {
    type: WARNING_ALERT,
    payload: message,
  };
};

export const createSuccessAlert = (message: string): AlertActionType => {
  return {
    type: SUCCESS_ALERT,
    payload: message,
  };
};

export const clearAlerts = (): AlertActionType => {
  return { type: CLEAR_ALERT };
};
