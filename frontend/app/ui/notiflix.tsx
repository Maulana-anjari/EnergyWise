'use client'
import React from 'react';
import { Notify } from 'notiflix/build/notiflix-notify-aio';

const Notifier = ({ message, type }: { message: string, type: string}) => {
  React.useEffect(() => {
    if (message) {
      switch (type) {
        case 'success':
          Notify.success(message);
          break;
        case 'info':
          Notify.info(message);
          break;
        case 'warning':
          Notify.warning(message);
          break;
        case 'failure':
          Notify.failure(message);
          break;
        default:
          Notify.failure(message);
      }
    }
  }, [message, type]);

  return null;
};

export default Notifier;
