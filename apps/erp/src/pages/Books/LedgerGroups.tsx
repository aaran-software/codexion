
import TableForm from "../../../../../resources/layouts/Form/TableForm";
import { ApiList } from "../../../../../resources/components/common/commonform";
import Books from "../../../public/Books.json";

const formApi: ApiList = {
  create: "/api/payment",
  read: "/api/payment",
  update: "/api/payment",
  delete: "/api/payment",
};

function LedgerGroup() {
  return (
    <div>
      <TableForm
        formName="Ledger Group"
        formApi={formApi}
        jsonPath={Books}
        fieldPath="books.ledgergroup"
        multipleEntry={false}
      />
    </div>
  );
}

export default LedgerGroup;
