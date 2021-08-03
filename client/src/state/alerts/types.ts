export interface AlertState {
  errorMessage: string;
  infoMessage: string;
  warningMessage: string;
  successMessage: string;
}

export const ERROR_ALERT = 'ERROR_ALERT';
export const INFO_ALERT = 'INFO_ALERT';
export const WARNING_ALERT = 'WARNING_ALERT';
export const SUCCESS_ALERT = 'SUCCESS_ALERT';
export const CLEAR_ALERT = 'CLEAR_ALERT';

interface ErrorAlertAction {
  type: typeof ERROR_ALERT;
  payload: string;
}

interface InfoAlertAction {
  type: typeof INFO_ALERT;
  payload: string;
}

interface WarningAlertAction {
  type: typeof WARNING_ALERT;
  payload: string;
}

interface SuccessAlertAction {
  type: typeof SUCCESS_ALERT;
  payload: string;
}

interface ClearAlertAction {
  type: typeof CLEAR_ALERT;
}

export type AlertActionType =
  | ErrorAlertAction
  | InfoAlertAction
  | WarningAlertAction
  | SuccessAlertAction
  | ClearAlertAction;
