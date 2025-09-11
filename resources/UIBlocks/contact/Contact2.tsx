import { useState } from "react";
import { MdEmail, MdPhone, MdLocationOn } from "react-icons/md";
import Alert from "../../components/alert/alert";

export interface KeyValue {
  label: string;
  value: string;
}

type ContactProps = {
  addresses: string;
  email: KeyValue[];
  phone: KeyValue[];
  subTitle?: string;
  title?: string;
  description?: string;
};

interface FormData {
  name: string;
  email: string;
  message: string;
}

export default function Contact1({
  title = "Contact Us",
  addresses,
  email,
  phone,
  subTitle,
  description
}: ContactProps) {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    message: "",
  });

  const [alertType, setAlertType] = useState<
    "success" | "update" | "delete" | "warning" | "failed"
  >("success");
  const [message, setMessage] = useState<string>("");
  const [showAlert, setShowAlert] = useState(false);

  // ✅ Handle input change
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // ✅ Handle form submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:5000/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (data.success) {
        setAlertType("success");
        setMessage("Message Sent Successfully!");
        setFormData({ name: "", email: "", message: "" }); // reset form
      } else {
        setAlertType("failed");
        setMessage("⚠️ Error sending message.");
      }
    } catch (err) {
      console.error(err);
      setAlertType("failed");
      setMessage("⚠️ Error sending message.");
    }
    setShowAlert(true);
  };

  return (
    <div className="relative overflow-hidden">
      <h1 className="sr-only">{title}</h1>

      {/* 🔔 Alert */}
      <div className="absolute top-3 right-0 z-50">
        <Alert
          type={alertType}
          message={message}
          show={showAlert}
          onClose={() => setShowAlert(false)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 relative z-10">
        {/* 📍 Address & Social Section */}
        <div className="space-y-8 px-2 text-foreground p-6 md:p-12 lg:px-20 py-20 bg-create-foreground/5 flex flex-col justify-center">
          <div className="flex justify-center flex-col gap-5">
            <p className="text-lg text-primary">{title}</p>
            <h1 className="text-2xl font-bold">{subTitle}</h1>
            <p className="text-foreground/80 text-sm">
              {description}
            </p>

            {/* Address */}
            <div className="flex items-start gap-3 mt-6 w-[70%]">
              <MdLocationOn className="text-highlight1-foreground text-4xl mt-1 p-1 shrink-0 bg-highlight1 rounded-md" />
              <div>
                <p className="font-bold">Our Location</p>
                <p>{addresses}</p>
              </div>
            </div>

            {/* Phone numbers */}
            {phone.map((ph, idx) => (
              <div key={idx} className="flex items-start gap-3 mt-4 w-[70%]">
                <MdPhone className="text-highlight1-foreground text-4xl mt-1 p-1 shrink-0 bg-highlight1 rounded-md" />
                <div>
                  <p className="font-bold">Phone Number</p>
                  <a href={`tel:${ph.value}`} className="cursor-pointer">
                    {ph.label}
                  </a>
                </div>
              </div>
            ))}

            {/* Emails */}
            {email.map((em, idx) => (
              <div key={idx} className="flex items-start gap-3 mt-4 w-[70%]">
                <MdEmail className="text-highlight1-foreground text-4xl mt-1 p-1 shrink-0 bg-highlight1 rounded-md" />
                <div>
                  <p className="font-bold">Email Address</p>
                  <a href={`mailto:${em.value}`} className="cursor-pointer">
                    {em.label}
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ✨ Form Section with decorations */}
        <div className="relative w-[80%] py-20 block mx-auto">
          {/* 🔸 Dotted Pattern (aligned below circle) */}
          <div className="absolute top-11 -right-8 grid grid-cols-3 gap-2 z-0">
            {Array.from({ length: 45 }).map((_, i) => (
              <span
                key={i}
                className="w-1 h-1 bg-orange-600 shadow rounded-full block"
              ></span>
            ))}
          </div>

          <div className="absolute top-11 right-1 grid grid-cols-7 gap-2">
            {Array.from({ length: 21 }).map((_, i) => (
              <span
                key={i}
                className="w-1 h-1 bg-orange-600 rounded-full block"
              ></span>
            ))}
          </div>

          <div className="absolute bottom-20 -left-8 grid grid-cols-4 gap-2 z-0">
            {Array.from({ length: 36 }).map((_, i) => (
              <span
                key={i}
                className="w-1 h-1 bg-orange-600 rounded-full block"
              ></span>
            ))}
          </div>

          <div className="absolute bottom-11 -left-8 grid grid-cols-10 gap-2">
            {Array.from({ length: 30 }).map((_, i) => (
              <span
                key={i}
                className="w-1 h-1 bg-orange-600 rounded-full block"
              ></span>
            ))}
          </div>

          <form
            className="relative flex flex-col space-y-4 py-5 px-8 bg-highlight1 text-highlight1-foreground rounded-lg shadow-lg z-10"
            onSubmit={handleSubmit}
          >
            <div>
              <label htmlFor="name" className="text-lg">
                Name
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white text-black"
              />
            </div>

            <div>
              <label htmlFor="email" className="text-lg">
                Email
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white text-black"
              />
            </div>

            <div>
              <label htmlFor="message" className="text-lg">
                Message
              </label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white text-black"
                rows={5}
              />
            </div>

            <button
              type="submit"
              aria-label="submit"
              className="bg-primary hover:bg-hover text-create-foreground py-2 px-6 rounded-md font-semibold cursor-pointer"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
