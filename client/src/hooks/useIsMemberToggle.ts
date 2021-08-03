import { useState, useEffect } from 'react';
import { useTypedSelector } from './useTypedSelector';
import {
  fetchIsGroupMember,
  addGroupMembership,
  deleteGroupMembership,
} from '../API/groups';

export function useIsMemberToggle(groupName: string) {
  const [isMember, setIsMember] = useState(false);
  const { token, user } = useTypedSelector((state) => state.user);

  useEffect(() => {
    (async () => {
      try {
        await fetchIsGroupMember(
          groupName,
          user?.userId ?? '',
          token as string
        );
        setIsMember(true);
      } catch (error) {
        setIsMember(false);
      }
    })();
  }, [groupName, user, token]);

  async function deleteMembership() {
    try {
      await deleteGroupMembership(groupName, token as string);
      return true;
    } catch (error) {
      console.log(error);
      return false;
    }
  }

  async function addMembership() {
    try {
      await addGroupMembership(groupName, token as string);
      return true;
    } catch (error) {
      console.log(error);
      return false;
    }
  }

  async function toggleMembership() {
    if (isMember) {
      if (await deleteMembership()) {
        setIsMember(false);
      }
    } else {
      if (await addMembership()) {
        setIsMember(true);
      }
    }
  }

  return { isMember, toggleMembership };
}
