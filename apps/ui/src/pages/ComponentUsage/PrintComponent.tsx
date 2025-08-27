import Print from '../../../../../resources/layouts/printformat/Print'
import { useRef } from 'react';
import { useReactToPrint } from 'react-to-print';

function PrintComponent() {
   const printRef = useRef<HTMLDivElement>(null);

 const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: "sample print",
  });
  return (
    <div ref={printRef} className='block m-auto p-6'>
      <Print
        head={['S.No', 'Item', 'Quantity','%', 'Rate', 'Amount']}
        body={[
          ['1', 'Notebook', '10', '5', '50', '500'],
          ['2', 'Pen', '20', '5', '5', '100'],
          ['3', 'Marker', '5', '5', '20', '100'],
        ]}
        client={{
          name: "ABC CLIENTS INDIA LTD",
          address: {
            address1: "12, Park Street",
            address2: "Kolkata, West Bengal",
            address3: "9876543210",
            address4: "29ABCDE1234F1Z5"
          }
        }}
      />
 <button
        onClick={handlePrint}
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 no-print"
      >
        Print Statement
      </button>
    </div>
  )
}

export default PrintComponent