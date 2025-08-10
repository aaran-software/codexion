
interface ContactType {
  id: "whatsapp" | "phone" | "email" | "instagram" | string;
  contact: string;
  imgPath: string;
  defaultMessage?: string;
  className?:string

}

interface FloatContactProps {
  contacts: ContactType[];
  className?:string
}

const platformColors: Record<string, string> = {
  whatsapp: "#25D366",
  phone: "#4CAF50",
  email: "#EA4335",
  instagram: "linear-gradient(45deg, #F58529, #DD2A7B, #8134AF, #515BD4)",
};

function FloatContact({ contacts, className }: FloatContactProps) {
  const handleClick = (contact: ContactType) => {
    if (contact.id === "whatsapp") {
      const encodedMsg = encodeURIComponent(contact.defaultMessage || "");
      const url = `https://wa.me/${contact.contact}${
        encodedMsg ? `?text=${encodedMsg}` : ""
      }`;
      window.open(url, "_blank");
    } else if (contact.id === "phone") {
      window.location.href = `tel:${contact.contact}`;
    } else if (contact.id === "email") {
      window.location.href = `mailto:${contact.contact}`;
    } else if (contact.id === "email") {
  const subject = encodeURIComponent("Product Inquiry"); // default subject
  const body = encodeURIComponent(contact.defaultMessage || "");
  const url = `mailto:${contact.contact}?subject=${subject}${
    body ? `&body=${body}` : ""
  }`;
  window.location.href = url;
} else {
      console.warn(`No handler for contact type: ${contact.id}`);
    }
  };

  return (
    <div className={`flex flex-col gap-5 ${className}`}>
      {contacts.map((item) => (
        <div key={item.id} className="relative group flex items-center">
          {/* Tooltip label */}
          <span
            className="absolute right-14 px-3 py-1 text-white text-sm rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 transition-all duration-300"
            style={{
              background:
                platformColors[item.id] || "rgba(0,0,0,0.7)",
            }}
          >
            {item.contact}
          </span>

          {/* Icon button */}
          <button
            onClick={() => handleClick(item)}
            className={`p-2 rounded-full shadow-md hover:scale-105 transition bg-white cursor-pointer ${item.className}`}
          >
            <img src={item.imgPath} alt={item.id} className="w-8 h-8" />
          </button>
        </div>
      ))}
    </div>
  );
}

export default FloatContact;
