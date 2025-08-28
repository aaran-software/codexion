import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import Invoice from "../../../public/Invoice.json";

const formApi: ApiList = {
  create: "/api/resource/Sales Invoice",
  read: "/api/resource/Sales Invoice",
  update: "/api/resource/Sales Invoice",
  delete: "/api/resource/Sales Invoice",
};

function Sales() {
  return (
    <div>
      <TableForm
        formName="Sales"
        formApi={formApi}
        jsonPath={Invoice}
        fieldPath="invoice.sales"
        multipleEntry={true}
      />
    </div>
  );
}

export default Sales;
