import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import master from "../../../public/master.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function Styles() {
  return (
    <div>
      <TableForm
        formName="Styles"
        formApi={formApi}
        jsonPath={master}
        fieldPath="master.style"
        multipleEntry={false}
      />
    </div>
  );
}

export default Styles;
