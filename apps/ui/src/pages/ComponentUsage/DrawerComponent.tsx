import { useState } from 'react';
import Drawer from '../../../../../resources/components/drawer/Drawer';
import Button from '../../../../../resources/components/button/Button';

export default function DrawerComponent() {
  const [openDrawer, setOpenDrawer] = useState<null | 'top' | 'bottom' | 'left' | 'right'>(null);

  const toggleDrawer = (position: 'top' | 'bottom' | 'left' | 'right') => {
    setOpenDrawer(position);
  };

  const closeDrawer = () => setOpenDrawer(null);

  return (
    <div className="space-y-4 p-4">
      <Button label="Open Top" onClick={() => toggleDrawer('top')} children={undefined} />
      <Button label="Open Bottom" onClick={() => toggleDrawer('bottom')} children={undefined} />
      <Button label="Open Left" onClick={() => toggleDrawer('left')} children={undefined} />
      <Button label="Open Right" onClick={() => toggleDrawer('right')} children={undefined} />

      <Drawer
        position="top"
        title="Top Panel"
        isOpen={openDrawer === 'top'}
        onClose={closeDrawer}
      >
        Top offcanvas content
      </Drawer>

      <Drawer
        position="bottom"
        title="Bottom Panel"
        isOpen={openDrawer === 'bottom'}
        onClose={closeDrawer}
      >
        Bottom offcanvas content
      </Drawer>

      <Drawer
        position="left"
        title="Left Panel"
        isOpen={openDrawer === 'left'}
        onClose={closeDrawer}
      >
        Left offcanvas content
      </Drawer>

      <Drawer
        position="right"
        title="Right Panel"
        isOpen={openDrawer === 'right'}
        onClose={closeDrawer}
      >
        Right offcanvas content
      </Drawer>
    </div>
  );
}
