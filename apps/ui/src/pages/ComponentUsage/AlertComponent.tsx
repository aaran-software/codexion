import { useState } from 'react';
import Alert from '../../../../../resources/components/alert/alert';
import Button from '../../../../../resources/components/button/Button';

interface AlertItem {
  id: number;
  type: "success" | "update" | "warning" | "delete";
  message: string;
}

function AlertComponent() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);

  const triggerAlert = (type: AlertItem["type"], message: string) => {
    const id = Date.now() + Math.random();
    const newAlert = { id, type, message };
    setAlerts((prev) => [...prev, newAlert]);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      setAlerts((prev) => prev.filter((alert) => alert.id !== id));
    }, 5000);
  };

  const buttons = [
    {
      label: "Success Notification",
      className: "bg-create text-create-foreground",
      alerttype: "success",
      message: "Success Notification",
    },
    {
      label: "Update Notification",
      className: "bg-update text-update-foreground",
      alerttype: "update",
      message: "Update Notification",
    },
    {
      label: "Delete Notification",
      className: "bg-delete text-delete-foreground",
      alerttype: "delete",
      message: "Delete Notification",
    },
    {
      label: "Warning Notification",
      className: "bg-warning text-warning-foreground",
      alerttype: "warning",
      message: "Warning Notification",
    },
  ];

  return (
    <div className="relative">
      {/* Alert Stack */}
      <div className="fixed top-15 right-3 md:top-6 md:right-6 z-50 space-y-3">
        {alerts.map((alert) => (
          <Alert
            key={alert.id}
            type={alert.type}
            message={alert.message}
            show={true}
            onClose={() =>
              setAlerts((prev) => prev.filter((a) => a.id !== alert.id))
            }
          />
        ))}
      </div>

      {/* Header */}
      <div className="text-center mb-5 text-xl">
        Click button to preview Alert Message
      </div>

      {/* Buttons */}
      <div className="flex flex-wrap justify-center gap-3 px-5">
        {buttons.map((button, idx) => (
          <Button
            key={idx}
            label={button.label}
            className={button.className}
            onClick={() => triggerAlert(button.alerttype as any, button.message)} children={undefined}          />
        ))}
      </div>
    </div>
  );
}

export default AlertComponent;
