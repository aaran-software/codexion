import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import transaction from "../../../public/transaction.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function AccountBooks() {
  return (
    <div>
      <TableForm
        formName="Account Books"
        formApi={formApi}
        jsonPath={transaction}
        fieldPath="transaction.account"
        multipleEntry={false}
      />
    </div>
  );
}

export default AccountBooks;
