import ButtonDropdown from "../../Components/Button/ButtonDropdown";
import ImageButton from "../../Components/Button/ImageBtn";
import CommonTable, {
  type ApiList,
  type Column,
  type TableRowData,
} from "../../Components/common/commontable";
import Filter from "../../Components/common/Filter";
import Drawer from "../../Components/Drawer/Drawer";
import { exportToCSV } from "../../Components/External/ExportToCSV";
import AnimateButton from "../../Components/Input/animatebutton";
import Button from "../../Components/Input/Button";
import DropdownRead from "../../Components/Input/Dropdown-read";
import Pagination from "../../Components/Pagination/Pagination";
import { useEffect, useMemo, useRef, useState } from "react";
import CommonForm, {
  type FieldGroup,
} from "../../Components/common/commonform";
import { useReactToPrint } from "react-to-print";
import Print from "../External/Print";
import apiClient from "../../pages/app/codexsun/api/apiClients";
type FormLayoutProps = {
  groupedFields: FieldGroup[];
  head: Column[];
  formApi: ApiList;
  printableFields: string[];
  data?: any[];
};

function FormLayout({
  groupedFields,
  head,
  formApi,
  printableFields,
  data
}: FormLayoutProps) {
  // useEffect(() => {
  //   apiClient
  //     .get(formApi.read) // fetch up to 1000 customers
  //     .then(async (res: { data: { data: any } }) => {
  //       const customerList = res.data.data;

  //       // Fetch full details of each customer in parallel
  //       const detailedData = await Promise.all(
  //         customerList.map(
  //           (cust: any) =>
  //             apiClient
  //               .get(`${formApi.read}/${encodeURIComponent(cust.name)}`)
  //               .then((res: { data: { data: any } }) => res.data.data)
  //               .catch(() => null) // handle errors gracefully
  //         )
  //       );

  //       // Clean nulls and format into table rows
  //       const rows = detailedData.filter(Boolean).map((c: any) => ({
  //         id: c.name,
  //         customer_name: c.customer_name,
  //         status: c.status || "",
  //         customer_group: c.customer_group || "",
  //         customer_type: c.customer_type || "",
  //       }));

  //       setTableData(rows);
  //     })
  //     .catch((err: any) => {
  //       console.error("❌ Failed to fetch Customers:", err);
  //     });
  // }, []);
useEffect(() => {
  if (Array.isArray(data)) {
    setTableData(data); // ✅ Use data from props
  } else {
    // Fallback to API fetching
    apiClient.get(formApi.read)
      .then(async (res: { data: { data: any } }) => {
        const customerList = res.data.data;
        const detailedData = await Promise.all(
          customerList.map((cust: any) =>
            apiClient
              .get(`${formApi.read}/${encodeURIComponent(cust.name)}`)
              .then((res: { data: { data: any } }) => res.data.data)
              .catch(() => null)
          )
        );
        const rows = detailedData.filter(Boolean).map((c: any) => ({
          id: c.name,
          customer_name: c.customer_name,
          status: c.status || "",
          customer_group: c.customer_group || "",
          customer_type: c.customer_type || "",
        }));
        setTableData(rows);
      })
      .catch((err: any) => {
        console.error("❌ Failed to fetch data:", err);
      });
  }
}, [data, formApi.read]);

  const [tableData, setTableData] = useState<TableRowData[]>([]);

  const [filters, setFilters] = useState<Record<string, string>>({});
  const [filterDrawerOpen, setFilterDrawerOpen] = useState(false);
  const [visibleColumns, setVisibleColumns] = useState<string[]>(
    head.map((h) => h.key)
  );
  const [formOpen, setFormOpen] = useState(false);
  const [editData, setEditData] = useState<any>({});
  const [editId, setEditId] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(20);

  const filteredData = useMemo(() => {
    return tableData.filter((row) =>
      head.every((h) => {
        const key = h.key.toLowerCase();
        if (!filters[key] || key === "action") return true;
        return String(row[key] ?? "")
          .toLowerCase()
          .includes(filters[key].toLowerCase());
      })
    );
  }, [filters, tableData]);

  const handleCreate = () => {
    setEditData({});
    setEditId(null); // updated
    setFormOpen(true);
  };

  const handleFormSubmit = (formData: any[] | any) => {
    const updated = [...tableData];

    if (Array.isArray(formData)) {
      formData.forEach((entry) => {
        const index = updated.findIndex((d) => d.id === entry.id);
        if (index !== -1) {
          updated[index] = entry; // update with new value
        } else {
          updated.push(entry); // add if new
        }
      });
    } else {
      if (editId !== null) {
        // Editing single row
        const index = updated.findIndex((d) => d.id === editId);
        if (index !== -1) {
          updated[index] = { ...updated[index], ...formData };
        }
      } else {
        // Creating new single row
        updated.push({
          id: `perm-${Date.now()}-${Math.random()
            .toString(36)
            .substring(2, 5)}`,
          ...formData,
        });
      }
    }

    setTableData(updated);
    setFormOpen(false);
    setEditId(null);
    setEditData({});
  };

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * rowsPerPage;
    return filteredData.slice(start, start + rowsPerPage);
  }, [filteredData, currentPage, rowsPerPage]);

  const handleEdit = (rowData: any) => {
    if (Array.isArray(rowData)) {
      // Bulk edit
      setEditData(rowData); // ✅ already works
    } else {
      setEditData(rowData);
      setEditId(rowData.id);
    }
    setFormOpen(true);
  };

  const handleDelete = (index: number) => {
    const updated = [...tableData];
    updated.splice(index, 1);
    setTableData(updated);
  };
  const handleDeleteSelected = (ids: string[]) => {
    const updated = tableData.filter((row) => !ids.includes(row.id));
    setTableData(updated);
  };

  const generatePageSizeOptions = (total: number): number[] => {
    const base = Math.max(Math.floor(total * 0.1), 1);
    const steps = [1, 5, 10, 15, 20];
    const options: number[] = [];
    for (const step of steps) {
      const val = base * step;
      if (val <= total) options.push(val);
    }
    return options;
  };

  const printRef = useRef<HTMLDivElement>(null);
  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: "receipt",
  });
  const [printColumn] = useState<string[]>(
    printableFields.map((field: any) => field.key)
  );

  const printHead = useMemo(() => {
    return printableFields.map((field: any) => field.label);
  }, [printableFields]);

  const printBody = useMemo(() => {
    return paginatedData.map((row) =>
      printColumn.map((key) => String(row[key] ?? ""))
    );
  }, [paginatedData, printColumn]);
  return (
    <div className="w-full p-2 lg:pr-5">
      {/* Table header items */}
      <div ref={printRef} className="hidden print:block p-5">
        <Print
          head={printHead}
          body={printBody}
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
      </div>
      <div className="flex justify-between gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <ImageButton
            className="bg-update p-2 text-white"
            icon="filter"
            onClick={() => setFilterDrawerOpen(!filterDrawerOpen)}
          />
          {Object.entries(filters)
            .filter(([key, value]) => value && key !== "action")
            .map(([key, value]) => (
              <div
                key={key}
                className="flex items-center gap-1 px-2 text-xs rounded-full bg-muted text-muted-foreground border border-ring"
              >
                <span className="capitalize">{key}</span>: <span>{value}</span>
                <ImageButton
                  icon="close"
                  onClick={() =>
                    setFilters((prev) => {
                      const updated = { ...prev };
                      delete updated[key];
                      return updated;
                    })
                  }
                  className="text-xs p-2 font-bold text-delete hover:text-destructive"
                />
              </div>
            ))}
        </div>
        <div className="flex gap-2 items-center">
          <ButtonDropdown
            icon="column"
            columns={head
              .filter((h) => h.key !== "id")
              .map((h) => ({ key: h.key, label: h.label }))}
            visibleColumns={visibleColumns}
            onChange={setVisibleColumns}
            excludedColumns={["id"]}
            className="block m-auto"
          />
          <ImageButton
            icon="export"
            className="p-2"
            onClick={() =>
              exportToCSV(
                filteredData,
                head.map((h) => h.key),
                `purchase.csv`
              )
            }
          />
          <ImageButton icon="print" className="p-2" onClick={handlePrint} />
          <AnimateButton
            label="Create"
            className="bg-create"
            mode="create"
            onClick={handleCreate}
          />
        </div>
      </div>

      {/* form for create and edit */}
      {formOpen && (
        <CommonForm
          groupedFields={groupedFields} // ✅ use groupedFields here
          isPopUp
          formOpen={formOpen}
          setFormOpen={setFormOpen}
          formName="Client"
          successMsg="Form submitted successfully"
          faildMsg="Form submission failed"
          initialData={Array.isArray(editData) ? {} : editData}
          onSubmit={handleFormSubmit}
          api={formApi}
        />
      )}

      {/* Purchase Table */}
      <div className="mt-5">
        <CommonTable
          head={head.filter((h) => visibleColumns.includes(h.key))}
          body={paginatedData}
          onEdit={handleEdit}
          onCreate={handleCreate}
          currentPage={currentPage}
          rowsPerPage={rowsPerPage}
          totalCount={filteredData.length}
          onPageChange={setCurrentPage}
          onDelete={handleDelete}
          onDeleteSelected={handleDeleteSelected}
          onCellClick={(key, value) => {
            setFilters((prev) => ({ ...prev, [key]: value }));
            setFilterDrawerOpen(true);
          }}
          filterOnColumnClick={filterDrawerOpen}
          multipleEntry={false}
          api={formApi}
        />
      </div>

      {/* number of page and pagination */}
      <div className="mt-4 flex flex-col gap-3 md:flex-row justify-between items-center text-sm text-muted-foreground">
        <div className="flex items-center gap-2">
          <label htmlFor="rows-per-page" className="whitespace-nowrap">
            Records per page:
          </label>
          <DropdownRead
            id="page"
            items={generatePageSizeOptions(filteredData.length).map(String)}
            err=""
            // label='pages'
            className="w-30"
            onChange={(value) => {
              const selectedValue = Array.isArray(value) ? value[0] : value;
              const parsed = parseInt(selectedValue, 10);
              if (!isNaN(parsed)) {
                setRowsPerPage(parsed);
              }
            }}
            value={String(rowsPerPage)}
            placeholder={""}
            label={""}
          />
        </div>

        <p>
          {Math.min((currentPage - 1) * rowsPerPage + 1, filteredData.length)}–
          {Math.min(currentPage * rowsPerPage, filteredData.length)} of{" "}
          {filteredData.length} products
        </p>

        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(filteredData.length / rowsPerPage)}
          onPageChange={setCurrentPage}
        />
      </div>

      {/* filter drawer */}
      <Drawer
        isOpen={filterDrawerOpen}
        onClose={() => setFilterDrawerOpen(false)}
        position="bottom"
        title="Filters"
      >
        <Filter
          head={head
            .filter((h) => visibleColumns.includes(h.key))
            .map((h) => h.key)}
          filters={filters}
          onFilterChange={(key, value) =>
            setFilters((prev) => ({ ...prev, [key]: value }))
          }
        />
        <div className="flex justify-end gap-3 mt-5">
          <Button
            label="Clear"
            className="text-delete-foreground bg-delete"
            onClick={() => {
              setFilters({});
              setFilterDrawerOpen(false);
            }}
            children={undefined}
          />

          <Button
            label="Apply changes"
            className="bg-update text-update-foreground"
            onClick={() => setFilterDrawerOpen(false)}
            children={undefined}
          />
        </div>
      </Drawer>
    </div>
  );
}

export default FormLayout;
