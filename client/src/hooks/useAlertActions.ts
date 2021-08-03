import { useDispatch } from 'react-redux';
import { bindActionCreators } from 'redux';
import { alertActionCreators } from '../state';

export const useAlertActions = () => {
  const dispatch = useDispatch();
  return bindActionCreators(alertActionCreators, dispatch);
};
