import { store } from 'react-notifications-component';

const notify = (title: string, message: string, success: boolean) => {
  store.addNotification({
    title,
    message,
    type: success ? 'success' : 'danger',
    insert: 'top',
    container: 'top-right',
    animationIn: ['animate__animated', 'animate__fadeIn'],
    animationOut: ['animate__animated', 'animate__fadeOut'],
    dismiss: {
      duration: 4000,
      onScreen: true,
    },
  });
};

export const notifySuccess = (title: string, message: string) => {
  notify(title, message, true);
};

export const notifyError = (title: string, message: string) => {
  notify(title, message, false);
};
