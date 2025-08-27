import NotificationButton from '../../../../../resources/components/Alert/NotificationButton'
import { useState } from 'react'

function NotificationComponent() {
  const [notification] = useState([
    {
      icon: "mail",
      label: "Inbox",
      count: 6,
      mode: "icon",
    },
        {
      icon: "message",
      label: "Inbox",
      count: 6,
      mode: "icon",
    },
    {
      icon: "bell",
      label: "Alert",
      count: 3,
      mode: "label",
    },
    {
      icon: "alert",
      label: "Notification",
      count: 12,
      mode: "label",
    },

  ]);

  return (
    <div className="flex gap-10 flex-wrap justify-center">
      {notification.map((notify, index) => (
        <NotificationButton
          key={index}
          icon={notify.icon as any} // cast if needed
          mode={notify.mode as any}
          label={notify.label}
          count={notify.count}
        />
      ))}
    </div>
  );
}

export default NotificationComponent;
