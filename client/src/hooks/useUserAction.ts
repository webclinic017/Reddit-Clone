import { useDispatch } from 'react-redux';
import { bindActionCreators } from 'redux';
import { userActionCreators } from '../state';

export const useUserActions = () => {
  const dispatch = useDispatch();
  return bindActionCreators(userActionCreators, dispatch);
};
