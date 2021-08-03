import { useSelector, TypedUseSelectorHook } from 'react-redux';
import { RootReducerType } from '../state';

export const useTypedSelector: TypedUseSelectorHook<RootReducerType> =
  useSelector;
