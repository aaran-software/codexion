import {useEffect, useState} from "react";
import Button from "../../../../resources/components/button/Button";
import FloatingInput from "../../../../resources/components/input/floating-input";
import Radio_group from "../../../../resources/components/radioGroup/radio_group";

function DockerCreate() {
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
            <h1 className="text-3xl font-bold text-create">Create New Project</h1>
            <div className="flex w-full items-end gap-3">
                <div className="flex-1">
                    <FloatingInput err={""} id={"name"} label={"Site Name"}/>
                </div>
                <Button label={"Check"} className="border border-ring/30  bg-create text-create-foreground"/>
            </div>

            <FloatingInput err={""} id={"name"} label={"Port"}/>
            <h3>Choose Database</h3>
            <Radio_group name={"db"} options={[{value: "mariadb", label: 'mariadb:3306'}, {
                value: "mariadb",
                label: 'mariadb:5746'
            }]}/>
            <FloatingInput err={""} id={"name"} label={"Port"}/>
            <h3>Choose Server</h3>

            <Radio_group name={"server"}
                         options={[{value: "enginx", label: 'Enginx'}, {value: "traefik", label: 'Traefik'}]}/>
            <FloatingInput err={""} id={"name"} label={"Dockerfile"}/>
            <Button label={"Submit"} className="border border-ring/30 bg-create text-create-foreground"/>
        </div>
    );
}

export default DockerCreate;
