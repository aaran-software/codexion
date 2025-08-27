import EditableTable from "../../../../../resources/components/common/EditableTable"

function EditableTableComponent() {
  return (
    <div className="relative overflow-visible mx-5">
        <EditableTable 
            fields = {[
            { id: "fullName", label: "Full Name", type: "textinput", placeholder: "Enter full name" },
            { id: "userEmail", label: "User Email", type: "textinput", placeholder: "yourmail@example.com" },
            { id: "category", label: "Category", type: "dropdownread", options: ['Design', 'Marketing'], placeholder: "Choose category" },
            { id: "loginPass", label: "Login Password", type: "password", placeholder: "********" },
            { id: "brandsPreferred", label: "Preferred Brands", type: "dropdownreadmultiple", options: ['OnePlus', 'Realme', 'Pixel'], placeholder: "Pick brands" },
            { id: "deviceModels", label: "Device Models", type: "dropdownmultiple", options: ['x100', 'y200', 'z300'], placeholder: "Choose models" },
            { id: "primaryDevice", label: "Primary Device", type: "dropdown", options: ['Laptop', 'Tablet', 'Smartphone'], placeholder: "Select device" }
            ]}
        />
    </div>
  )
}

export default EditableTableComponent