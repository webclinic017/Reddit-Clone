import React, { useRef, useEffect } from 'react';
import '../../styles/modal.css';

interface ModalProps {
  isOpen: boolean;
  closeModal: () => void;
}

const Modal: React.FC<ModalProps> = ({ isOpen, closeModal, children }) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const modalContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickAway = (e: any) => {
      const wasClickAway =
        modalRef.current &&
        modalContentRef.current &&
        modalRef.current.contains(e.target) &&
        !modalContentRef.current.contains(e.target);

      if (wasClickAway) {
        closeModal();
      }
    };

    document.addEventListener('click', handleClickAway, true);
    return () => document.removeEventListener('click', handleClickAway, true);
  }, [closeModal]);

  if (!isOpen) return null;

  return (
    <div className="modal" ref={modalRef}>
      <div className="modal__content" ref={modalContentRef}>
        {children}
      </div>
    </div>
  );
};

export default Modal;
