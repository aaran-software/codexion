import { useState } from "react";
import FileUpload from "../../../../Components/Input/FileInput";
import FloatingInput from "../../../../Components/Input/FloatingInput";
import DropdownRead from "../../../../Components/Input/Dropdown-read";
import Button from "../../../../Components/Input/Button";
import apiClient from "../api/apiClients";

function CustomizeLogo() {
  const [logoPath, setLogoPath] = useState<string>("");

  const id = "logo";

  const handleFileChange = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await apiClient.post("/upload-logo", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // Assuming backend returns: { path: "/uploads/logo.png" }
      setLogoPath(response.data.path);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div>
      <div className="px-[5%] flex flex-col gap-5">
        <h1 className="text-2xl font-bold py-4">Logo</h1>
        <FileUpload
          id={id}
          multiple={false}
          onChange={(files) => {
            if (files.length > 0) handleFileChange(files[0]);
          }}
        />
        <div>
          {/* logo preview */}
          <img src="" alt="" />
          {logoPath && (
            <p className="text-green-600 mt-2">Logo saved at: {logoPath}</p>
          )}
        </div>
        <FloatingInput id={"height"} label={"Logo height"} err={""} />
        <FloatingInput id={"font_size"} label={"Font Size"} err={""} />
        <FloatingInput id={"padding"} label={"Padding Top & Bottom"} err={""} />
        <FloatingInput id={"company_name"} label={"Company Name"} err={""} />
        <FloatingInput id={"color"} label={"Color"} err={""} />
        <DropdownRead
          id={"position"}
          items={["Top", "Middle", "Bottom"]}
          label={"vertical Align"}
          err={""}
        />

        <Button
          label={"Save Changes"}
          className="bg-update text-update-foreground w-max block ml-auto"
        />
      </div>
    </div>
  );
}

export default CustomizeLogo;
