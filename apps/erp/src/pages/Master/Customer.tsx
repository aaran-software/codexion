import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import master from "../../../public/master.json";

const formApi: ApiList = {
  create: "/api/resource/Customer",
  read: "/api/resource/Customer",
  update: "/api/resource/Customer",
  delete: "/api/resource/Customer",
};

function Company() {
  return (
    <div className="pr-2">
      <TableForm
        formName="Customer"
        formApi={formApi}
        jsonPath={master}
        fieldPath="master.customer"
        multipleEntry={false}
      />
    </div>
  );
}

export default Company;
