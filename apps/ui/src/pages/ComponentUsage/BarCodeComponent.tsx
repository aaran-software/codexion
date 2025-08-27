import BarCode from '../../../../../resources/components/common/BarCode'
import { useState } from 'react';

function BarCodeComponent() {
    const [values]=useState([
        {
            title:"item1",
            value:"123456789098"
        },
        {
            title:"item2",
            value:"567832904323"
        },
        {
            title:"item3",
            value:"678354190385"
        },
    ])

  return (
    <div>
      <BarCode values={values}/>
    </div>
  )
}

export default BarCodeComponent