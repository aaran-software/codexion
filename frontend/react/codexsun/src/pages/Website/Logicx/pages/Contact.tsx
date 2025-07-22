import contact from '../../../../../public/assets/svg/contact.svg';
import { useState } from 'react';

function Contact() {
  const [address]=useState([
    {
      title:"Address",
      body:"Moon Street , 446 Jupiter, JP 44600"
    },
     {
      title:"Email",
      body:"info@logicx.in"
    },
     {
      title:"Phone",
      body:"9843213500"
    },
     {
      title:"Time",
      body:"Mon - Sat : 9AM - 6PM"
    },
  ])
  return (
    <section>
      {/* Address Section */}
       <section className="px-5 lg:px-[12%] py-10">
        <h1 className="text-xl md:text-3xl font-bold text-center pb-10">Contact ERP Experts | LogicX Coimbatore</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 pt-10 lg:grid-cols-4 gap-8">
          {address.map((item, idx) => (
            <div
              key={idx}
              className="flex items-start gap-4 p-4 rounded-lg shadow-md bg-gray-50"
            >
              {/* Optional icon placeholder */}
              <div className="w-2 h-8 bg-green-600 rounded" aria-hidden="true" />
              <div className='flex flex-col gap-3'>
                <p className="text-lg font-medium text-gray-700">{item.title}</p>
                <p className="text-sm font-medium text-gray-700">{item.body}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Call to Action Section */}
      <div className=' mt-10 py-20 flex flex-col gap-10 bg-website-background text-website-foreground'>
        <img src={contact} className='w-50 block mx-auto' alt='contact illustration' />
        <div className='text-center font-semibold text-xl md:text-3xl'>Let’s Talk ERP</div>
        <div className='md:w-[70%] block mx-auto text-center p-5'>
          Call us at 98432 13500 or email info@logicx.in for a free demo or consultation.
        </div>
        <div className='flex justify-center'>
          <a href='tel:98432 13500' className='bg-gradient-to-r from-[#23aa70] to-[#0e854f] text-gray-50 px-10 py-4 text-xl hover:bg-gradient-to-r hover:from-[#23aa70] hover:to-[#23aa70] rounded-md'>CALL US NOW</a>
        </div>
      </div>

      {/* Google Maps Section */}
      <iframe
        className='w-full h-[400px]'
        src='https://www.google.com/maps/embed?pb=!1m22!1m8!1m3!1d7173.442386232486!2d-74.0104808!3d40.7243502!3m2!1i1024!2i768!4f13.1!4m11!3e6!4m3!1m2!1d40.724699799999996!2d-74.01058809999999!4m5!1s0x89c259f389c1fd55%3A0x1968536fe3b90b3f!2s456%20Washington%20St.%20Luxury%20Apartments%20456%20Washington%20St%20New%20York%2C%20NY%2010013%20United%20States!3m2!1d40.724350199999996!2d-74.0104808!5e1!3m2!1sen!2sin!4v1749819751191!5m2!1sen!2sin'
        style={{ border: 0 }}
        allowFullScreen
        loading='lazy'
        referrerPolicy='no-referrer-when-downgrade'
      ></iframe>
{/* 
      <FooterLink />
      <Footer /> */}
    </section>
  );
}

export default Contact;
