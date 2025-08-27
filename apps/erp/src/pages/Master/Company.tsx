import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import master from "../../../public/master.json";

const formApi: ApiList = {
  create: "/api/resource/Company",
  read: "/api/resource/Company",
  update: "/api/resource/Company",
  delete: "/api/resource/Company",
};

function Company() {
  return (
    <div className="pr-2">
      <TableForm
        formName="Company"
        formApi={formApi}
        jsonPath={master}
        fieldPath="master.company"
        multipleEntry={false}
      />
    </div>
  );
}

export default Company;
