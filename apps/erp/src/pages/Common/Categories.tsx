import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import common from "../../../public/common.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function Category() {
  return (
    <div>
      <TableForm
        formName="Category"
        formApi={formApi}
        jsonPath={common}
        fieldPath="common.category"
        multipleEntry={false}
      />
    </div>
  );
}

export default Category;
