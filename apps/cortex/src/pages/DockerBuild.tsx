import {useEffect, useState} from "react";
import Button from "../../../../resources/components/button/Button";
import FloatingInput from "../../../../resources/components/input/FloatingInput";
import RadioGroup from "../../../../resources/components/RadioGroup/RadioGroup";
import DropdownRead from "../../../../resources/components/input/Dropdown-read";

function DockerBuild() {
    const API_URL = "http://127.0.0.1:4000";


// declare input fields

    const [fields, setFields] = useState([
        {id: "1", label: "Project 1", err: "", endpoint: "/api/product", value: ""},
        {id: "1", label: "Project 2", err: "", endpoint: "", value: ""},
        {id: "1", label: "Project 3", err: "", endpoint: "", value: ""},

    ]);

//   handle api
    const handleApi = (api: string) => {
        useEffect(() => {
            fetch(`${API_URL}/${api}`)
                .then()
                .catch()
        }, [])
    }
    const handleChange = (index: number, newValue: string) => {
        const updatedFields = [...fields];
        updatedFields[index].value = newValue;
        setFields(updatedFields);
    };
    return (
        <div className="flex gap-5 flex-col p-5 md:px-[20%]">
            <h1 className="text-3xl font-bold text-update">Build Existing Project</h1>
            <div className="flex w-full items-end gap-3">
                <div className="flex-1">
                    <DropdownRead id={"site"} items={['cxsun','ecart']} label={"Site Name"} err={""} />
                </div>
                <Button label={"Check"} className="border border-ring/30 bg-create text-create-foreground"/>
            </div>

            <FloatingInput err={""} id={"name"} label={"Port"}/>
            <h3>Update Database</h3>
            <RadioGroup name={"db"} options={[{value: "mariadb", label: 'mariadb:3306'}, {
                value: "mariadb",
                label: 'mariadb:5746'
            }]}/>
            <FloatingInput err={""} id={"name"} label={"Port"}/>
            <h3>Update Server</h3>

            <RadioGroup name={"server"}
                        options={[{value: "enginx", label: 'Enginx'}, {value: "traefik", label: 'Traefik'}]}/>
            <FloatingInput err={""} id={"name"} label={"Dockerfile"}/>
            <Button label={"Build"} className="border border-ring/30 bg-update text-update-foreground"/>
        </div>
    );
}

export default DockerBuild;
