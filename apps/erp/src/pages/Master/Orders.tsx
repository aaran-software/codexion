import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import master from "../../../public/master.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function Order() {
  return (
    <div>
      <TableForm
        formName="Order"
        formApi={formApi}
        jsonPath={master}
        fieldPath="master.order"
        multipleEntry={false}
      />
    </div>
  );
}

export default Order;
