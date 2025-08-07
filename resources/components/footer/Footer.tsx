import { Link } from "react-router-dom";
import { CiFacebook } from "react-icons/ci";
import { FiTwitter } from "react-icons/fi";
import { FaInstagram } from "react-icons/fa";
import NewUpdate from "../../../resources/components/advertisment/NewUpdate";
import { useState } from "react";

const Footer: React.FC = () => {
  const [successMessage, setSuccessMessage] = useState("");
  const [showUpdate, setShowUpdate] = useState(false);

  const [resetKey, setResetKey] = useState(0); // add this

  const handleVisible = () => {
    setResetKey((prev) => prev + 1);
    setShowUpdate(true);
  };

  const handleCloseUpdate = () => {
    setShowUpdate(false);
  };

  const handleUpdateStatus = (message: string) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(""), 3000); // auto-clear
  };
  return (
    <footer className="bg-neutral-900  text-white text-sm mt-5">
      <div className="grid grid-cols-1 px-[5%] sm:grid-cols-2 md:grid-cols-4 gap-6 py-10">
        {/* About */}
        <div>
          <h5 className="font-bold mb-2">About</h5>
          <ul className="space-y-1">
            <li>
              <Link to="/contactus" className="hover:underline text-white">
                Contact Us
              </Link>
            </li>
            <li>
              <Link to="/aboutus" className="hover:underline text-white">
                About Us
              </Link>
            </li>
          </ul>
        </div>

        {/* Help */}
        <div>
          <h5 className="font-bold mb-2">Link</h5>
          <ul className="space-y-1">
            <li>
              <Link to="/payment" className="hover:underline text-white">
                Blog
              </Link>
            </li>
            <li>
              <Link to="/FAQ" className="hover:underline text-white">
                FAQ
              </Link>
            </li>
          </ul>
        </div>

        {/* Consumer Policy */}
        <div>
          <h5 className="font-bold mb-2">Consumer Policy</h5>
          <ul className="space-y-1">
            <li>
              <Link to="/termsofuse" className="hover:underline text-white">
                Terms of Use
              </Link>
            </li>
            <li>
              <Link to="/security" className="hover:underline text-white">
                Security
              </Link>
            </li>
            <li>
              <Link to="/privacy" className="hover:underline text-white">
                Privacy
              </Link>
            </li>
          </ul>
          <p className="mt-3">
            Phone:{" "}
            <a href="tel:+12125557890" className="underline">
              9843179905
            </a>
            <br />
            Email:{" "}
            <a href="mailto:support@vibevault.com" className="underline">
              support@techmedia.in
            </a>
          </p>
        </div>
        {/* Address */}
        <div>
          <h5 className="font-bold mb-2">Address</h5>
          <p className="text-white leading-6">
            <span className="font-bold text-lg">Tech Media</span>,
            <br />
            436 Avinashi Road,
            <br />
            Near CITU Office,
            <br />
            Tiruppur, Tamil Nadu 641 603
          </p>
          <h6 className="mt-3 font-semibold">www.techmedia.in</h6>
          <h6 className="mt-3 font-semibold">info@techmedia.in</h6>

          <h6 className="mt-3 font-semibold">Social:</h6>
          <div className="flex gap-3 mt-1">
            <CiFacebook className="w-8 h-8 p-1 hover:-translate-y-1 transition-transform cursor-pointer" />
            <FiTwitter className="w-8 h-8 p-1 hover:-translate-y-1 transition-transform cursor-pointer" />
            <FaInstagram className="w-8 h-8 p-1 hover:-translate-y-1 transition-transform cursor-pointer" />
          </div>
        </div>
      </div>
      {showUpdate && (
        <NewUpdate
          key={resetKey}
          id="new update"
          title="🚀 New Update Available!"
          description="We’ve introduced major improvements and features. Check it out now!"
          api="/api/update"
          onClose={handleCloseUpdate}
          onStatus={handleUpdateStatus} // 🔁 NEW PROP
        />
      )}

      {successMessage && (
        <div className="fixed bottom-4 right-4 bg-green-100 text-green-800 px-4 py-2 rounded shadow-md z-50">
          {successMessage}
        </div>
      )}
      <div className="flex flex-row justify-between border-t border-white/10">
        <div></div>
        <div className="text-center py-3 bg-neutral-900 ">
          &copy; 2024 Tech Media. All Rights Reserved.
        </div>
        <div
          className="block my-auto text-background/50 pr-5 cursor-pointer"
          onClick={handleVisible}
        >
          V 1.0.1
        </div>
      </div>
    </footer>
  );
};

export default Footer;
