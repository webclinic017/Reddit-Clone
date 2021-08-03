import { useMemo } from 'react';
import { useDispatch } from 'react-redux';
import { bindActionCreators } from 'redux';
import { groupActionCreators } from '../state';

export const useGroupActions = () => {
  const dispatch = useDispatch();
  return useMemo(
    () => bindActionCreators(groupActionCreators, dispatch),
    [dispatch]
  );
};
