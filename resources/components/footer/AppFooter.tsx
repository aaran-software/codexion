import {Link} from "react-router-dom";
import {CiFacebook} from "react-icons/ci";
import {FiTwitter} from "react-icons/fi";
import {FaInstagram} from "react-icons/fa";
import NewUpdate from "../../../resources/components/advertisment/NewUpdate";
import {useState} from "react";

const AppFooter: React.FC = () => {
    const [successMessage, setSuccessMessage] = useState("");
    const [showUpdate, setShowUpdate] = useState(false);

    const [resetKey, setResetKey] = useState(0); // add this

    const handleVisible = () => {
        setResetKey(prev => prev + 1);
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
                <div className="block my-auto text-background/50 pr-5 cursor-pointer" onClick={handleVisible}>
                    V 1.0.1
                </div>

            </div>

        </footer>
    );
};

export default AppFooter;
