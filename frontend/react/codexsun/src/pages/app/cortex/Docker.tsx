import { useEffect, useState } from "react";
import Button from "../../../Components/Input/Button";
import FloatingInput from "../../../Components/Input/FloatingInput";

function Docker() {
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:4000";


// declare input fields

  const [fields,setFields] = useState([
    { id: "1", label: "Project 1", err: "" ,endpoint:"/api/product" , value: "" },
    { id: "1", label: "Project 2", err: "" ,endpoint:"" , value: "" },
    { id: "1", label: "Project 3", err: "" ,endpoint:"" , value: "" },

  ]);

//   handle api 
  const handleApi=(api: string)=>{
    useEffect(()=>{
        fetch(`${API_URL}/${api}`)
        .then()
        .catch()
    },[])
  }
   const handleChange = (index: number, newValue: string) => {
    const updatedFields = [...fields];
    updatedFields[index].value = newValue;
    setFields(updatedFields);
  };
  return (
    <div className="flex gap-5 flex-col">
      {fields.map((field,index) => (
        <div className="flex gap-3">
          <FloatingInput err={field.err} id={field.id} label={field.label}  onChange={(e) => handleChange(index, e.target.value)} />
          <Button label={"Build"} onClick={()=>{handleApi(field.endpoint)}} className="border border-ring/30" />
        </div>
      ))}
    </div>
  );
}

export default Docker;
