
import { FaMapMarkerAlt, FaPhoneAlt, FaEnvelope } from "react-icons/fa";
interface ContactInfo {
  address?: string;
  phone?: string[];
  email?: string[];
}

interface PortfolioContactProps {
  contact: ContactInfo;
}

function PortfolioContact({ contact }: PortfolioContactProps) {
  const contactDetails = [
   { type: "address", value: contact.address, icon: <FaMapMarkerAlt size={28} /> },
    { type: "phone", value: contact.phone?.join(", "), phones: contact.phone, icon: <FaPhoneAlt size={28} /> },
    { type: "email", value: contact.email?.join(", "), emails: contact.email, icon: <FaEnvelope size={28} /> },
  ].filter((item) => item.value);

  return (
    <div className="px-4 md:px-[10%]">
      <h1 className="text-5xl font-bold py-10 text-center">
        Have Any Questions?
      </h1>

      {/* Map + Form */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="flex items-center">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3914.688007214001!2d77.33172007452157!3d11.136597752448083!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba9065f168ee73d%3A0x3d454757d01e842f!2sMahavishnu%20Nagar%2C%20Pitchampalayam%20Pudur%2C%20Tiruppur%2C%20Chettipalayam%2C%20Tamil%20Nadu%20641603!5e0!3m2!1sen!2sin!4v1755594962938!5m2!1sen!2sin"
            width="600"
            height="450"
            loading="lazy"
            className="w-full rounded-lg shadow-lg"
          ></iframe>
        </div>

        <div className="border border-ring/30 bg-background rounded-lg p-5 shadow-2xl">
          <form className="flex flex-col space-y-4 border border-ring/30 rounded-lg p-5">
            <div>
              <label htmlFor="name" className="text-foreground text-lg">
                Name
              </label>
              <input
                type="text"
                name="name"
                required
                className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white text-black"
              />
            </div>
            <div>
              <label htmlFor="email" className="text-foreground text-lg">
                Email
              </label>
              <input
                type="email"
                name="email"
                required
                className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white text-black"
              />
            </div>
            <div>
              <label htmlFor="message" className="text-foreground text-lg">
                Message
              </label>
              <textarea
                name="message"
                required
                className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-white text-black"
                rows={5}
              />
            </div>
            <button
              type="button"
              className="bg-primary hover:bg-hover text-create-foreground py-2 px-6 rounded-md font-semibold cursor-pointer"
            >
              Submit
            </button>
          </form>
        </div>
      </div>

      {/* Contact Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-20">
        {contactDetails.map((item, index) => (
          <div
            key={index}
            className="flex flex-col items-center justify-center p-6 bg-white shadow-2xl rounded-lg border border-gray-200"
          >
            <div className="text-3xl bg-primary p-4 mb-5 text-white rounded-full">{item.icon}</div>

            {item.type === "phone" && item.phones ? (
              <div className="flex flex-col items-center space-y-1 mt-2">
                {item.phones.map((ph, i) => (
                  <a
                    key={i}
                    href={`tel:${ph}`}
                    className="text-gray-600 hover:text-primary cursor-pointer"
                  >
                    {ph}
                  </a>
                ))}
              </div>
            ) : item.type === "email" && item.emails ? (
              <div className="flex flex-col items-center space-y-1 mt-2">
                {item.emails.map((em, i) => (
                  <a
                    key={i}
                    href={`mailto:${em}`}
                    className="text-gray-600 hover:text-primary cursor-pointer"
                  >
                    {em}
                  </a>
                ))}
              </div>
            ) : (
              <p className="text-gray-600 text-center mt-2">{item.value}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PortfolioContact;
