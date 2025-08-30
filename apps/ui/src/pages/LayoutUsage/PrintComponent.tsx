import Print from "../../../../../resources/layouts/printformat/Print";
import PrintFormat2 from "../../../../../resources/layouts/printformat/PrintFormat2";
import { useEffect, useRef, useState } from "react";
import { useReactToPrint } from "react-to-print";

function mapDataToBody(head: string[], data: any[]) {
  return data.map((item, index) => {
    return head.map((col) => {
      switch (col.toLowerCase()) {
        case "s.no":
          return (index + 1).toString(); // Serial number
        case "hsn":
          return item.hsn || "";
        case "qty":
        case "quantity":
          return item.qty?.toString() || "";
        case "rate":
        case "price":
          return item.rate?.toString() || "";
        case "tax":
          return item.tax?.toString() || "";
        case "amount":
        case "sub total":
          return item.amount?.toString() || "";
        case "item name":
          return item.itemName || "";
        default:
          return item[col] || ""; // fallback
      }
    });
  });
}


function PrintComponent() {
  const printRef = useRef<HTMLDivElement>(null);
  const printRef2 = useRef<HTMLDivElement>(null);

  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: "sample print",
  });

  const handlePrint2 = useReactToPrint({
    contentRef: printRef2,
    documentTitle: "sample print",
  });
  const head = ["S.No", "HSN", "Qty", "Rate", "Tax", "Amount", "Item Name"];
  const [body, setBody] = useState<string[][]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("https://your-api-endpoint.com/invoice-items");
        const data = await res.json();

        const mappedBody = mapDataToBody(head, data);
        setBody(mappedBody);
      } catch (err) {
        console.error(err);
      }
    }

    fetchData();
  }, []);
  
  return (
    <div>
      <div ref={printRef2} className="block m-auto p-6">
        <PrintFormat2
          head={[
            "S.No",
            "HSN",
            "Item Name",
            "Qty",
            "Rate",
            "Tax",
            "Amount",
            "CGST",
            "SGST",
            "Sub Total",
          ]}
          body={[
            [
              "1",
              "87234",
              "Notebook Noteboo kNotebook Notebook Notebook Notebook",
              "10",
              "500",
              "5%",
              "500",
              "546",
              "5464",
              "3543",
            ],
            [
              "2",
              "87234",
             "Notebook Noteboo kNotebook Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "3",
              "87234",
             "Notebook Noteboo kNotebootebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ],
            [
              "7",
              "87234",
             "Notebook Noteboo kNotebook Notebook ok Notebook Notebook Notebook",
              "1000000",
              "5000000",
              "55%",
              "1111111111",
              "11111111",
              "11111111",
              "1111111111",
            ]
          ]}
          alignments={[
            "center",
            "center",
            "left",
            "center",
            "right",
            "right",
            "right",
            "right",
            "right",
            "right",
          ]}
          client={{
            name: "ABC CLIENTS INDIA LTD",
            address: {
              address1: "No.1, P.V.G Nagar Extension, Samundipuram South, Gandhi Nagar, HP Petrol Pump",
              address2: "Tiruppur , Tamil Nadu-641601",
            },
            phone: 9363944493,
            email: "sukraagarments96@gmail.com",
            gstinNo: "33AXIPP0352P1Z6",

          }}
          bank={{
            accountNo: "D123456789101112",
            IFSC: "DEMO1234",
            Bank: "Demo Bank",
            Branch: "DEMO BRANCH",
          }}
          logo={"/assets/logo/logo.svg"}
          customerName="DEEPA"
          BillAddress={{
            address1:"VELAKANNI SCHOOLVELAKANNI SCHOOL KIRSHNAGIRI",
            address2:"Tamil Nadu, India",
            address3:" State Code: 33 PIN Code: 635001",
            GSTIN:"GSTIN: 33AXIPP0352P1Z6"
          }}
           ShipingAddress={{
            address1:"VELAKANNI SCHOOLVELAKANNI SCHOOL KIRSHNAGIRI",
            address2:"Tamil Nadu, India",
            address3:" State Code: 33 PIN Code: 635001",
            GSTIN:"GSTIN: 33AXIPP0352P1Z6"
          }}
          
          totalColumns={["Qty", "Amount", "Sub Total", "CGST", "SGST"]}
          invoiceInfo={{
            invoiceNo: "INV-001",
            invoiceDate: "29/08/2025",
            transportMode: "Road",
            vehicleNo: "TN24AB1234",
            supplyDateTime: "29/08/2025 10:00 AM",
            placeOfSupply: "Tamil Nadu",
            IRN:"5e0d2a3c8f9b7d6a1c4f3b2e7a8d9c0b1234567890abcdef1234567890abcdef"
          }}
        />
        <button
          onClick={handlePrint2}
          className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 no-print"
        >
          Print Statement
        </button>
      </div>

      <div ref={printRef} className="block m-auto p-6">
        <Print
          head={["S.No", "Item", "Quantity", "%", "Rate", "Amount"]}
          body={[
            ["1", "Notebook", "10", "5", "50", "500"],
            ["2", "Pen", "20", "5", "5", "100"],
            ["3", "Marker", "5", "5", "20", "100"],
          ]}
          client={{
            name: "ABC CLIENTS INDIA LTD",
            address: {
              address1: "12, Park Street",
              address2: "Kolkata, West Bengal",
              address3: "9876543210",
              address4: "29ABCDE1234F1Z5",
            },
          }}
        />
        <button
          onClick={handlePrint}
          className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 no-print"
        >
          Print Statement
        </button>
      </div>
    </div>
  );
}

export default PrintComponent;
