import { JSX, useState } from "react";
import SafeToWords from "../../global/external/safeToWords";

interface InvoiceInfo {
  invoiceNo: string;
  invoiceDate: string;
  transportMode: string;
  vehicleNo: string;
  supplyDateTime: string;
  placeOfSupply: string;
  IRN?: string;
}
interface Bank {
  accountNo: string;
  IFSC: string;
  Bank: string;
  Branch: string;
}
interface CustomerAddress {
  address1: string;
  address2: string;
  address3: string;
  GSTIN: string;
}

const columnWidths: Record<string, string> = {
  "S.No": "w-[10px]", // max 2 digits (~40px)
  HSN: "w-[50px]", // 7 digits
  Qty: "w-[50px]", // 7 digits
  Rate: "w-[60px]", // 7 digits
  Tax: "w-[20px]", // 4 digits
  Amount: "w-[60px]", // 13 digits
  "Sub Total": "w-[60px]", // 13 digits
  CGST: "w-[50px]", // 11 digits
  SGST: "w-[50px]", // 11 digits
  "Item Name": "w-auto", // takes remaining space
};

interface PrintProps {
  head: string[];
  body: string[][];
  alignments?: ("left" | "center" | "right")[];
  client: {
    name: string;
    address: Address;
    phone: number;
    email: string;
    gstinNo: string;
  };
  bank: Bank;
  logo: string;
  customerName: string;
  BillAddress: CustomerAddress;
  ShipingAddress: CustomerAddress;
  totalColumns?: string[];
  invoiceInfo: InvoiceInfo;
}
interface Address {
  address1: string;
  address2: string;
}
function PrintFormat2({
  head,
  body,
  alignments,
  client,
  bank,
  logo,
  customerName,
  BillAddress,
  ShipingAddress,
  totalColumns = [],
  invoiceInfo,
}: PrintProps) {
  const quantityIndex = head.findIndex((h) =>
    h.toLowerCase().includes("quantity")
  );
  const priceIndex = head.findIndex((h) => h.toLowerCase().includes("price"));
  const amountIndex = head.findIndex((h) => h.toLowerCase().includes("amount"));
  const totalIndex = head.findIndex((h) => h.toLowerCase() === "total");
  const hasTotalColumn = totalIndex !== -1;

  const day = new Date();
  const today = `${String(day.getDate()).padStart(2, "0")}-${String(day.getMonth() + 1).padStart(2, "0")}-${day.getFullYear()}`;
  const hasQuantity = quantityIndex !== -1;
  const hasAmount = amountIndex !== -1;
  const hasPrice = priceIndex !== -1;
  const shouldShowTotal = hasQuantity && (hasAmount || hasPrice);

  const computedBody = body.map((row) => {
    let rowTotal = 0;
    if (shouldShowTotal) {
      if (hasAmount) {
        rowTotal =
          (parseFloat(row[quantityIndex]) || 0) *
          (parseFloat(row[amountIndex]) || 0);
      } else if (hasPrice) {
        rowTotal =
          (parseFloat(row[quantityIndex]) || 0) *
          (parseFloat(row[priceIndex]) || 0);
      }
    }

    const newRow = [...row];
    if (shouldShowTotal) {
      newRow.push(rowTotal.toFixed(2));
    }
    return newRow;
  });

  const totalQuantity = computedBody.reduce((sum, row) => {
    const val = quantityIndex !== -1 ? parseFloat(row[quantityIndex]) : 0;
    return sum + (isNaN(val) ? 0 : val);
  }, 0);

  const totalAmount = computedBody.reduce((sum, row) => {
    const val = parseFloat(row[hasTotalColumn ? totalIndex : row.length - 1]);
    return sum + (isNaN(val) ? 0 : val);
  }, 0);

  const cgst = totalAmount * 0.09;
  const sgst = totalAmount * 0.09;
  const totalGST = cgst + sgst;
  const grandTotal = totalAmount + cgst + sgst;
  const roundedTotal = Math.round(grandTotal);
  const roundOff = +(roundedTotal - grandTotal).toFixed(2);
  const grandTotalInWords =
    SafeToWords(roundedTotal).replace(/\b\w/g, (l: string) => l.toUpperCase()) +
    " Rupees Only";

  const totals: Record<string, number> = {};

  totalColumns.forEach((col) => {
    const colIndex = head.indexOf(col);
    if (colIndex !== -1) {
      totals[col] = body.reduce((sum, row) => {
        const val = Number(row[colIndex]);
        return sum + (isNaN(val) ? 0 : val);
      }, 0);
    }
  });

  // Pagination setup: 8 items per page
  const itemsPerPage = 12;
  const pages: string[][][] = [];
  for (let i = 0; i < computedBody.length; i += itemsPerPage) {
    pages.push(computedBody.slice(i, i + itemsPerPage));
  }
  return (
    <div className="w-full">
      {pages.map((pageRows, pageIndex) => (
         <div key={pageIndex} className={`page border border-ring w-full ${pageIndex>0?" mt-10":""} text-[10px]`}>
          {/* header */}
          <div className="grid grid-cols-[15%_70%] gap-5 px-5 py-1">
            <img
              className="w-full block m-auto onject-contain"
              src={logo}
              alt="Logo"
            />
            <div className="flex flex-col items-center justify-center text-center text-xs">
              <h1 className="text-3xl font-bold">{client.name}</h1>
              {Object.values(client.address).map((line, idx) => (
                <p key={idx}>{line}</p>
              ))}
              <p>
                <span className="font-bold">Phone: </span>
                {client.phone} <span className="font-bold">Email: </span>
                {client.email}
              </p>
              <p className="font-bold text-lg">GSTIN : {client.gstinNo}</p>
            </div>
          </div>

          {/* Invoice Title */}
          <h3 className="font-bold border-t border-ring text-md text-center py-1">
            TAX INVOICE
          </h3>

          {/* Tax Invoice Left side */}
          <div className="grid grid-cols-[70%_30%] border-t border-b border-ring">
            {/* Left side */}
            <div className="px-5 py-1 flex flex-col gap-2 border-ring">
              {/* Row: Invoice No */}
              <div className="flex  gap-1">
                <div className="w-[15%] flex justify-between">
                  <p className="font-bold">Invoice No</p>
                  <p>:</p>
                </div>
                <p className="font-bold w-[35%]">{invoiceInfo.invoiceNo}</p>
              </div>

              {/* Row: Invoice Date */}
              <div className="flex  gap-1">
                <div className="w-[15%] flex justify-between">
                  <p className="font-bold">Invoice Date</p>
                  <p>:</p>
                </div>

                <p className="font-bold w-[35%]">{invoiceInfo.invoiceDate}</p>
              </div>

              {/* Row: IRN */}
              <div className="flex  gap-1">
                <div className="w-[15%] flex justify-between">
                  <p className="font-bold">IRN</p>
                  <p>:</p>
                </div>
                <p className="break-all font-bold">{invoiceInfo.IRN}</p>
              </div>
            </div>

            {/* 
        <div className="px-5 py-2 flex flex-col gap-2">
          
        </div> */}
          </div>

          <div className="grid grid-cols-2">
            <div className="text-center py-1 font-bold border-r border-ring">
              Customer Name & billing Address
            </div>
            <div className="text-center py-1 font-bold">
              Customer Name & Address Shipping Address
            </div>

            <div className="text-center py-1 px-5 border-t border-r border-ring">
              {/* Name Row */}
              <div className="flex gap-2 items-start">
                <div className="w-[20%] flex justify-between">
                  <p className="font-bold">Name</p>
                  <p>:</p>
                </div>
                <p className="text-left w-[80%] font-bold">{customerName}</p>
              </div>

              {/* Address Row */}
              <div className="flex gap-2 pt-1 items-start">
                <div className="w-[20%] flex justify-between">
                  <p className="font-bold">Address</p>
                  <p>:</p>
                </div>
                <div className="flex flex-col w-[80%]">
                  <p className="text-left">{BillAddress.address1}</p>
                  <p className="text-left">{BillAddress.address2}</p>
                  <p className="text-left">{BillAddress.address3}</p>
                  <p className="text-left">{BillAddress.GSTIN}</p>
                </div>
              </div>
            </div>

            <div className="text-center py-1 px-5 border-t border-ring">
              {/* Name Row */}
              <div className="flex gap-2 items-start">
                <div className="w-[20%] flex justify-between">
                  <p className="font-bold">Name</p>
                  <p>:</p>
                </div>
                <p className="text-left w-[80%] font-bold">{customerName}</p>
              </div>

              {/* Address Row */}
              <div className="flex gap-2 pt-1 items-start">
                <div className="w-[20%] flex justify-between">
                  <p className="font-bold">Address</p>
                  <p>:</p>
                </div>
                <div className="flex flex-col w-[80%]">
                  <p className="text-left break-words">
                    {ShipingAddress.address1}
                  </p>
                  <p className="text-left break-words">
                    {ShipingAddress.address2}
                  </p>
                  <p className="text-left break-words">
                    {ShipingAddress.address3}
                  </p>
                  <p className="text-left break-words">
                    {ShipingAddress.GSTIN}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Table */}
          <table className="min-w-full table-fixed border-b border-ring">
            <thead>
              <tr>
                {head.map((h, i) => (
                  <th
                    key={i}
                    className={`border border-ring px-2 py-1 text-center font-semibold whitespace-nowrap ${columnWidths[h] || "w-auto"}`}
                  >
                    {h}
                  </th>
                ))}
                {shouldShowTotal && (
                  <th className="border border-ring px-2 py-1 text-center font-semibold w-[120px]">
                    Total
                  </th>
                )}
              </tr>
            </thead>

            <tbody>
              {pageRows.map((row, i) => {
                const itemNameIndex = head.findIndex((h) =>
                  h.toLowerCase().includes("item")
                );
                const itemName = row[itemNameIndex] || "";
                const charsPerLine = 30;
                const maxLinesPerItem = 3;
                let requiredLines =
                  Math.ceil(itemName.length / charsPerLine) || 1;
                if (requiredLines > maxLinesPerItem)
                  requiredLines = maxLinesPerItem;

                return (
                  <tr
                    key={i}
                    style={{ height: `${requiredLines * 10}px` }}
                    className="align-top"
                  >
                    {head.map((h, idx) => {
                      const align = alignments?.[idx] || "center";
                      return (
                        <td
                          key={idx}
                          className={`border-x border-ring px-1 py-0 leading-tight text-${align} ${columnWidths[h] || "w-auto"}`}
                        >
                          {row[idx] || ""}
                        </td>
                      );
                    })}
                    {shouldShowTotal && (
                      <td className="border px-1 py-0 leading-tight text-right w-[120px]">
                        {row[row.length - 1] || ""}
                      </td>
                    )}
                  </tr>
                );
              })}

              {/* Fill empty rows so each page has 8 rows */}
              {Array.from({ length: itemsPerPage - pageRows.length }).map(
                (_, idx) => (
                  <tr key={`empty-${idx}`} className="h-[30px]">
                    {head.map((h, i) => (
                      <td
                        key={i}
                        className={`border-x border-ring px-1 py-0 leading-tight text-center ${columnWidths[h] || "w-auto"}`}
                      >
                        &nbsp;
                      </td>
                    ))}
                    {shouldShowTotal && (
                      <td className="border px-1 py-0 leading-tight text-right w-[120px]">
                        &nbsp;
                      </td>
                    )}
                  </tr>
                )
              )}
            </tbody>
            <tfoot className="border-t border-ring text-center">
              {totalColumns.length > 0 && (
                <tr className="font-bold bg-gray-100">
                  {head.map((col, i) => {
                    const align = alignments?.[i] || "center";
                    const isTotalCol = totals[col] !== undefined;

                    // Find the first total column index
                    const firstTotalIndex = head.findIndex((h) =>
                      totalColumns.includes(h)
                    );

                    // Case 1: Place "Total" label right before first total column
                    if (i === firstTotalIndex - 1) {
                      return (
                        <td
                          key={i}
                          className="px-2 py-1 text-right font-bold"
                          colSpan={1}
                        >
                          Total
                        </td>
                      );
                    }

                    // Case 2: If it's a total column, show total with border
                    if (isTotalCol) {
                      return (
                        <td
                          key={i}
                          className={`px-2 py-1 text-${align} border-x border-ring`}
                        >
                          {totals[col]}
                        </td>
                      );
                    }

                    // Case 3: Otherwise empty cell
                    return <td key={i}></td>;
                  })}
                </tr>
              )}
            </tfoot>
          </table>

          {/* Tax Section */}
          <div className="w-full grid grid-cols-3">
            <div className="p-2 border-r border-ring flex flex-col gap-2">
              <div className="flex flex-col gap-1">
                <div className="flex justify-between">
                  <p className="font-bold">BANK NAME</p>
                  <p>{bank.Bank}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">ACCOUNT NO</p>
                  <p>{bank.accountNo}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">IFSC CODE</p>
                  <p>{bank.IFSC}</p>
                </div>

                <div className="flex justify-between">
                  <p className="font-bold">BRANCH</p>
                  <p>{bank.Branch}</p>
                </div>
              </div>
            </div>
            <div className="flex flex-col border-r border-ring p-2 justify-between">
              <div className="flex flex-col gap-2">
                <div className="flex justify-between">
                  <p className="font-bold">Freight Charges</p>
                  <p>{totalAmount.toFixed(2)}</p>
                </div>
                <div className="flex gap-2 justify-between">
                  <p className="font-bold">Transport Mode</p>
                  <p className="text-left">{invoiceInfo.transportMode}</p>
                </div>

                <div className="flex gap-2 justify-between">
                  <p className="font-bold">Vehicle No</p>
                  <p className="text-left">{invoiceInfo.vehicleNo}</p>
                </div>

                <div className="flex gap-2 justify-between">
                  <p className="font-bold">Date & Time Supply</p>
                  <p className="text-left">{invoiceInfo.supplyDateTime}</p>
                </div>

                <div className="flex gap-2 justify-between">
                  <p className="font-bold">Place of Supply</p>
                  <p className="text-left">{invoiceInfo.placeOfSupply}</p>
                </div>
              </div>
            </div>
            <div className="flex flex-col p-2 justify-between">
              <div className="flex flex-col gap-1">
                <div className="flex justify-between">
                  <p className="font-bold">Taxable Amount</p>
                  <p>{totalGST.toFixed(2)}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">Total CGST (2.5%)</p>
                  <p>{cgst.toFixed(2)}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">Total SGST (2.5%)</p>
                  <p>{sgst.toFixed(2)}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">Total IGST (2.5%)</p>
                  <p>{totalGST.toFixed(2)}</p>
                </div>
                <hr className="text-ring" />
                <div className="flex justify-between">
                  <p className="font-bold">Total GST Amount</p>
                  <p>{totalGST.toFixed(2)}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">Other Charges</p>
                  <p>{totalGST.toFixed(2)}</p>
                </div>
                <div className="flex justify-between">
                  <p className="font-bold">Round Off</p>
                  <p>{roundedTotal.toFixed(2)}</p>
                </div>
                <hr className="text-ring" />
                <div className="flex justify-between">
                  <p className="font-bold text-lg">Grand Total</p>
                  <p className="text-lg">{roundedTotal.toFixed(2)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Grand Total Section */}
          <div className="w-full border-t border-ring">
            <div className=" flex gap-2 border-ring p-2">
              <p className="font-bold">Amount in words :</p>
              <p className="">{grandTotalInWords}</p>
            </div>
          </div>
          <div className="w-full border-t border-ring">
            <div className="grid gap-2 border-ring p-2">
              <div>
                <p className="font-bold underline">Declaration</p>
                <p className="">
                  We declare that this invoice shows the actual price of the
                  goods described and that all particulars are true and correct.
                </p>
              </div>
            </div>
          </div>
          {/* Footer */}
          <div className="w-full grid grid-cols-3 border-t border-ring">
            {/* First column - align left */}
            <div className="flex flex-col items-start justify-end">
              <p className="mt-6 text-left p-2">Customer Signature</p>
            </div>

            {/* Second column - align center */}
            <div className="flex flex-col items-center justify-end">
              <p className="mt-6 text-center p-2">Checked By</p>
            </div>

            {/* Third column - align right */}
            <div className="flex flex-col items-end justify-between">
              <p className="text-right p-2">For {client.name}</p>
              <p className="mt-6 text-right p-2">Authorised Signatory</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default PrintFormat2;
