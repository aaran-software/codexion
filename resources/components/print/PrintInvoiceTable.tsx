import React from "react";

interface PrintInvoiceProps {
  head: string[];
  body: string[][];
  alignments?: ("left" | "center" | "right")[];
  totalColumns: string[];
  pageRows: string[][];
  itemsPerPage: number;
  shouldShowTotal: boolean;
  totals: Record<string, number>;
}
export const columnWidths: Record<string, string> = {
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
function PrintInvoiceTable({
  head,
  pageRows,
  alignments,
  itemsPerPage,
  shouldShowTotal,
  totalColumns,
  totals,
}: PrintInvoiceProps) {
  return (
    <div>
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
            let requiredLines = Math.ceil(itemName.length / charsPerLine) || 1;
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
    </div>
  );
}

export default PrintInvoiceTable;
