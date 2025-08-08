import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import master from "../../../public/master.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function Contacts() {
  return (
    <div>
      <TableForm
        formName="Contacts"
        formApi={formApi}
        jsonPath={master}
        fieldPath="master.contact"
        multipleEntry={false}
      />
    </div>
  );
}

export default Contacts;
