import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import Invoice from "../../../public/Invoice.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function Payment() {
  return (
    <div>
      <TableForm
        formName="Payment"
        formApi={formApi}
        jsonPath={Invoice}
        fieldPath="invoice.payment"
        multipleEntry={false}
      />
    </div>
  );
}

export default Payment;
