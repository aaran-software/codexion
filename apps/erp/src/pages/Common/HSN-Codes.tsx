import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import common from "../../../public/common.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function HSNCode() {
  return (
    <div>
      <TableForm
        formName="HSN Codes"
        formApi={formApi}
        jsonPath={common}
        fieldPath="common.hsncode"
        multipleEntry={false}
      />
    </div>
  );
}

export default HSNCode;
