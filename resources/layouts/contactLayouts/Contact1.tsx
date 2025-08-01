import {FaHome, FaPhoneAlt} from 'react-icons/fa';
import {MdEmail} from 'react-icons/md';

type SocialLink = {
    href: string;
    img: string;
    alt: string;
};

type ContactProps = {
    title?: string;
    image?: string;
    address: string;
    phone: string;
    email: string;
    socialLinks: SocialLink[];
};

export default function Contact1({
                                     title = "Contact Us",
                                     image = "/assets/svg/contact.svg",
                                     address,
                                     phone,
                                     email,
                                     socialLinks,
                                 }: ContactProps) {
    return (
        <div className="p-6 mt-20">
            <h1 className="sr-only">{title}</h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left Image Section */}
                <div className="flex flex-col items-center text-center space-y-4 relative">
                    <h1 className="text-3xl font-bold text-foreground">{title}</h1>
                    <img
                        className="w-60 h-60 object-contain"
                        src={image}
                        alt="portfolio contact"
                    />
                    {/*<div className="absolute inset-0 bg-foreground/20"></div>*/}
                </div>

                {/* Form Section */}
                <form className="flex flex-col space-y-4">
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
                        className="bg-update hover:bg-create text-create-foreground py-2 px-6 rounded-md font-semibold"
                    >
                        Submit
                    </button>
                </form>

                {/* Address & Social Section */}
                <div className="space-y-6 text-white">
                    <div className="flex items-start space-x-3">
                        <FaHome className="text-2xl block my-auto text-foreground"/>
                        <div>
                            <h3 className="text-foreground font-semibold">Address</h3>
                            <p className="text-foreground/70">{address}</p>
                        </div>
                    </div>

                    <div className="flex items-start space-x-3">
                        <FaPhoneAlt className="text-2xl block my-auto text-foreground"/>
                        <div>
                            <h3 className="text-foreground font-semibold">Phone</h3>
                            <a href={`tel:${phone}`} className="text-foreground/70">
                                {phone}
                            </a>
                        </div>
                    </div>

                    <div className="flex items-start space-x-3">
                        <MdEmail className="text-2xl block my-auto text-foreground"/>
                        <div>
                            <h3 className="text-foreground font-semibold">Email</h3>
                            <a href={`mailto:${email}`} className="text-foreground/70">
                                {email}
                            </a>
                        </div>
                    </div>

                    <div className="flex gap-4 mt-4">
                        {socialLinks.map(({href, img, alt}) => (
                            <a key={alt} href={href} target="_blank" rel="noreferrer">
                                <img
                                    src={img}
                                    alt={alt}
                                    className="w-10 h-10 p-2 hover:scale-110 transition-transform"
                                />
                            </a>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
