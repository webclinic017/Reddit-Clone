import { useMemo } from 'react';
import { useDispatch } from 'react-redux';
import { bindActionCreators } from 'redux';
import { postActionCreators } from '../state';

export const usePostActions = () => {
  const dispatch = useDispatch();
  return useMemo(
    () => bindActionCreators(postActionCreators, dispatch),
    [dispatch]
  );
};
