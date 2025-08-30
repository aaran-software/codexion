import { JSX, useState } from "react";
import SafeToWords from "../../global/external/safeToWords";
import PrintHeader from "../../components/print/PrintHeader";
import PrintFooter from "../../components/print/PrintFooter";
import PrintInvoiceTable from "../../components/print/PrintInvoiceTable";
export interface PrintInvoiceInfo {
  invoiceNo: string;
  invoiceDate: string;
  transportMode: string;
  vehicleNo: string;
  supplyDateTime: string;
  placeOfSupply: string;
  IRN?: string;
}
export interface PrintBank {
  accountNo: string;
  IFSC: string;
  Bank: string;
  Branch: string;
}
export interface PrintCustomerAddress {
  address1: string;
  address2: string;
  address3: string;
  GSTIN: string;
}

interface PrintProps {
  head: string[];
  body: string[][];
  alignments?: ("left" | "center" | "right")[];
  client: {
    name: string;
    address: PrintAddress;
    phone: number;
    email: string;
    gstinNo: string;
  };
  bank: PrintBank;
  logo: string;
  customerName: string;
  BillAddress: PrintCustomerAddress;
  ShipingAddress: PrintCustomerAddress;
  totalColumns?: string[];
  invoiceInfo: PrintInvoiceInfo;
}
export interface PrintAddress {
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

  // Pagination setup
const pages: string[][][] = [];

if (computedBody.length <= 12) {
  // Case 1: All items fit in 1 page (≤12)
  pages.push(computedBody);
} else {
  let i = 0;

  // First page → up to 27 items
  const firstPageSize = Math.min(23, computedBody.length);
  pages.push(computedBody.slice(i, i + firstPageSize));
  i += firstPageSize;

  // Subsequent pages
  while (i < computedBody.length) {
    const remaining = computedBody.length - i;

    if (remaining <= 12) {
      // Last page → ≤12 items
      pages.push(computedBody.slice(i));
      i = computedBody.length;
    } else {
      // Middle pages → 27 items
      pages.push(computedBody.slice(i, i + 23));
      i += 23;
    }
  }
}

// ✅ If last page has more than 12 items, add an extra blank page for footer
const lastPage = pages[pages.length - 1];
if (lastPage.length > 12) {
  pages.push([]); // empty page only for footer
}


  return (
    <div className="w-full">
   {pages.map((pageRows, pageIndex) => {
  const isLastPage = pageIndex === pages.length - 1;
  const isEmptyFooterPage = pageRows.length === 0;

  return (
    <div
      key={pageIndex}
      className={`page border border-ring w-full ${pageIndex > 0 ? " mt-10" : ""} text-[10px]`}
    >
      <PrintHeader
        client={client}
        logo={logo}
        invoiceInfo={invoiceInfo}
        customerName={customerName}
        BillAddress={BillAddress}
        ShipingAddress={ShipingAddress}
      />

      <PrintInvoiceTable
        head={head}
        body={body}
        pageRows={pageRows}
        alignments={alignments}
         itemsPerPage={
    isEmptyFooterPage ? 10 : 
    pageIndex === 0 ? 23 : // first page
    (isLastPage ? 10 : 23) // last or middle pages
  }
        shouldShowTotal={shouldShowTotal}
        totalColumns={totalColumns}
        totals={totals}
        isLastPage={isLastPage}
      />

      {(isLastPage || isEmptyFooterPage) && (
        <PrintFooter
          bank={bank}
          totalAmount={totalAmount}
          cgst={cgst}
          sgst={sgst}
          totalGST={totalGST}
          roundedTotal={roundedTotal}
          grandTotalInWords={grandTotalInWords}
          client={client}
          invoiceInfo={invoiceInfo}
        />
      )}
    </div>
  );
})}

    </div>
  );
}

export default PrintFormat2;
