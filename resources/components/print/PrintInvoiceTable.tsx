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
   isLastPage: boolean;
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
  isLastPage
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
  {/* Case: At least one item */}
  {pageRows.length > 0 ? (
    <>
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

      {/* Fill remaining empty rows so table always has itemsPerPage rows */}
      {/* Fill remaining empty rows so table always has itemsPerPage rows */}
{Array.from({ length: Math.max(0, itemsPerPage - pageRows.length) }).map(
  (_, idx) => (
    <tr key={`empty-${idx}`}>
      {head.map((h, i) => (
        <td
          key={i}
          className={`border-x border-ring px-1 py-0 leading-tight text-center ${columnWidths[h] || "w-auto"}`}
          style={{ height: "30px" }}   // ✅ force height on cell
        >
          &nbsp;
        </td>
      ))}
      {shouldShowTotal && (
        <td
          className="border px-1 py-0 leading-tight text-right w-[120px]"
          style={{ height: "30px" }}   // ✅ also here
        >
          &nbsp;
        </td>
      )}
    </tr>
  )
)}

    </>
  ) : (
    // Case: No items at all → fill full page with empty rows
    Array.from({ length: itemsPerPage }).map((_, idx) => (
      <tr key={`empty-only-${idx}`} className="h-[30px]">
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
    ))
  )}
</tbody>


        {isLastPage && (
          // ✅ Show totals only on last page
          <tfoot className="border-t border-ring text-center">
            {totalColumns.length > 0 && (
              <tr className="font-bold bg-gray-100">
                {head.map((col, i) => {
                  const align = alignments?.[i] || "center";
                  const isTotalCol = totals[col] !== undefined;

                  const firstTotalIndex = head.findIndex((h) =>
                    totalColumns.includes(h)
                  );

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

                  return <td key={i}></td>;
                })}
              </tr>
            )}
          </tfoot>
        )  }
      </table>
    </div>
  );
}

export default PrintInvoiceTable;
