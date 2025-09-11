import React from "react";

export type TableRow = {
  header: string;
  data: string[];
};

interface SpecTableProps {
  tableData: TableRow[]; 
}

const SpecTable: React.FC<SpecTableProps> = ({ tableData }) => {
  // Handle empty tableData gracefully
  if (!tableData || tableData.length === 0) {
    return <p className="text-center py-4">No data available</p>;
  }

  // Find max number of data cells
  const maxCols = Math.max(...tableData.map((row) => row.data.length));

  return (
    <div className="overflow-x-auto">
      <table className="table-auto border-collapse border border-ring/30 w-full text-left text-sm">
        <tbody>
          {tableData.map((row, rowIndex) => (
            <tr
              key={rowIndex}
              className={rowIndex % 2 === 0 ? "bg-primary text-primary-foreground" : ""}
            >
              {/* Header column */}
              <th className="border border-ring/30 px-4 py-2 text-lg bg-primary text-primary-foreground w-[20%] align-top">
                {row.header}
              </th>

              {/* Data cells */}
              {Array.from({ length: maxCols }).map((_, i) => (
                <td key={i} className="border border-gray-300 px-4 py-2">
                  {row.data[i] ?? "-"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SpecTable;
