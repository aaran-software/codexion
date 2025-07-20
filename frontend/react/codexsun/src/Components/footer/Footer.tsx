import { Link } from "react-router-dom";
import { CiFacebook } from "react-icons/ci";
import { FiTwitter } from "react-icons/fi";
import { FaInstagram } from "react-icons/fa";

const Footer: React.FC = () => {
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
          <h5 className="font-bold mb-2">Help</h5>
          <ul className="space-y-1">
            <li>
              <Link to="/payment" className="hover:underline text-white">
                Payments
              </Link>
            </li>
            <li>
              <Link to="/shipping" className="hover:underline text-white">
                Shipping
              </Link>
            </li>
            <li>
              <Link to="/Cancelandrefund" className="hover:underline text-white">
                Cancellation & Returns
              </Link>
            </li>
            <li>
              <Link to="/FAQ" className="hover:underline text-white">
                FAQ
              </Link>
            </li>
          </ul>
        </div>

        {/* Address */}
        <div>
          <h5 className="font-bold mb-2">Address</h5>
          <p className="text-white leading-6">
            MAZSONE,<br />
            123 Fashion Avenue,<br />
            Suite 456 New York,<br />
            NY 10001 United States
          </p>
          <h6 className="mt-3 font-semibold">Social:</h6>
          <div className="flex gap-3 mt-1">
            <CiFacebook className="w-8 h-8 p-1 hover:-translate-y-1 transition-transform cursor-pointer" />
            <FiTwitter className="w-8 h-8 p-1 hover:-translate-y-1 transition-transform cursor-pointer" />
            <FaInstagram className="w-8 h-8 p-1 hover:-translate-y-1 transition-transform cursor-pointer" />
          </div>
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
            Phone: <a href="tel:+12125557890" className="underline">+1 (212) 555-7890</a><br />
            Email: <a href="mailto:support@vibevault.com" className="underline">support@vibevault.com</a>
          </p>
        </div>
      </div>

      <div className="flex flex-row justify-between border-t border-white/10">
        <div></div>
        <div className="text-center py-3 bg-neutral-900 ">
        &copy; 2024 Tech Media. All Rights Reserved.
      </div> 
      <div className="block my-auto text-background/50 pr-5">
        V 1.0.1
      </div>
      </div>
    </footer>
  );
};

export default Footer;
