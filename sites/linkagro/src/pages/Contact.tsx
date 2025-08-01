import React from 'react'
import Contact1 from '../../../../resources/layouts/contactLayouts/Contact1'

function Contact() {
    return (
        <div>
            <Contact1
                address="Tamilnadu"
                phone="+91 0000000000"
                email="linkagroexports@gmail.com"
                socialLinks={[
                    {
                        href: 'https://www.instagram.com/kumaranraja_22/',
                        img: '/assets/svg/instagram.svg',
                        alt: 'Instagram',
                    },
                    {
                        href: 'https://www.linkedin.com/in/muthukumaran-r/',
                        img: '/assets/svg/linkedin.svg',
                        alt: 'LinkedIn',
                    },
                    {
                        href: 'https://www.facebook.com/kumaranraja22/',
                        img: '/assets/svg/facebook.svg',
                        alt: 'Facebook',
                    },
                    {
                        href: 'https://wa.me/919543439311?text=Hi there!',
                        img: '/assets/svg/whatsapp.svg',
                        alt: 'WhatsApp',
                    },
                ]}
            />

        </div>
    )
}

export default Contact