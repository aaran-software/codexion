import { useEffect } from 'react';
import { Card, CardAction, CardContent, CardHeader } from '../Chart/card';
import AnimateButton from '../Input/animatebutton';

interface WarningProps {
  title: string;
  message: string;
  onConfirm: () => void;
  onClose: () => void;
}

function Warning({ title, message, onConfirm, onClose }: WarningProps) {

  useEffect(() => {

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center">
      <div className="animate-scaleIn">
        <Card className="bg-background p-5 shadow-xl rounded-xl max-w-md w-full">
          <CardHeader className="text-lg font-semibold">{title}</CardHeader>
          <CardContent className="py-3 text-muted-foreground">{message}</CardContent>
          <CardAction className="flex justify-end gap-3 px-4 pb-2">
            <AnimateButton
              mode="close"
              label="Close"
              className="bg-delete"
              onClick={onClose}
            />
            <AnimateButton
              mode="confirm"
              label="Confirm"
              className="bg-create"
              onClick={onConfirm}
            />
          </CardAction>
        </Card>
      </div>
    </div>
  );
}

export default Warning;
