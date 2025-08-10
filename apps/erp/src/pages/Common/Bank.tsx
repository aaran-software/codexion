import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import common from "../../../public/common.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function Bank() {
  return (
    <div>
      <TableForm
        formName="Account Books"
        formApi={formApi}
        jsonPath={common}
        fieldPath="common.bank"
        multipleEntry={false}
      />
    </div>
  );
}

export default Bank;
