import Homehero from '../../../../../public/assets/svg/home-hero.svg'

function Services() {
  return (
   <div className='py-10'>
    
     <div className='px-5 lg:px-[12%] grid mt-5 lg:grid-cols-2 gap-15'>
        <div className='flex justify-center items-center'>
          <img src={Homehero} className='w-[70%] lg:w-full' alt='img' />
        </div>
        <div className='flex flex-col justify-center gap-8'>
          <div>
          <h1 className='text-xl md:text-3xl my-3 font-bold' >ERP Services We Offer</h1>
           <ul className="list-disc pl-5 flex flex-col gap-2">
                <li><span className='font-bold'>Implementation & Deployment:</span> We handle the complete setup of ERP—on cloud or on-premise—with user access control, email alerts, backup, and SSL configuration</li>
                <li><span className='font-bold'>Module Customization:</span> Customize modules like Sales, Inventory, Accounting, HR, and Manufacturing to suit your unique workflow.</li>
                <li><span className='font-bold'>Tally Integration:</span> Bridge ERP with Tally for GST filing, financial reports, and accounting sync.</li>
                <li><span className='font-bold'>WooCommerce & eCommerce Integration:</span> Automate sales, stock, and invoices between your online store and ERP.</li>
                <li><span className='font-bold'>Training & Support:</span> Get in-depth training for staff, and ongoing technical support via call, email, or remote tools.</li>
            </ul>
          </div>
        </div>
      </div>
       <div className='p-5 mb-5 lg:px-[12%]'>
          <div className='flex flex-col gap-8 '>
            <div className='text-xl md:text-2xl font-bold mt-4'>Our Technical Expertise – Powering End-to-End ERP Customization & Automation</div>
            <p className='text-justify'>At <span className='font-semibold'>Tech Media</span>, we combine deep domain knowledge with robust technical skills to deliver <span className='font-semibold'>fully customized ERP and automation solutions</span>. Our multidisciplinary team is equipped to handle complex business needs, integrating multiple technologies for seamless performance, scalability, and growth.</p>
          </div>

          <h3 className='text-xl my-4 font-bold'>Our Core Competencies:</h3>
          
          <div className='flex flex-col gap-3'>
            <h2 className='text-lg font-semibold mt-4'>ERPNext</h2>
            <p className='text-justify'>We specialize in complete ERPNext deployment, customization, and integration—tailored to your industry. From workflow automation to custom module development, we align ERPNext with your exact business processes.</p>
          </div>
         
         <div className='flex flex-col gap-3'>
            <h2 className='text-lg font-semibold mt-4'>Tally Integration</h2>
            <p className='text-justify'>We bridge ERPNext and Tally for real-time accounting sync, GST compliance, and seamless financial reporting—eliminating duplication and manual data entry.</p>
          </div>
          <div className='flex flex-col gap-3'>
            <h2 className='text-lg font-semibold mt-4'> .NET Development</h2>
            <p className='text-justify'>Our .NET experts build scalable business applications, custom APIs, and middleware to enhance your ERP ecosystem—ensuring smooth integration with legacy systems or third-party tools.</p>
          </div>
          <div className='flex flex-col gap-3'>
            <h2 className='text-lg font-semibold mt-4'>React & Vue.js (VU JS)</h2>
            <p className='text-justify'>We craft modern, responsive web portals and dashboards using React and Vue.js—perfect for building fast, intuitive front-end interfaces over your ERP or internal systems.</p>
          </div>
          <div className='flex flex-col gap-3'>
            <h2 className='text-lg font-semibold mt-4'>ZK Teko Biometric Integration</h2>
            <p className='text-justify'>We integrate ZK Teko biometric devices directly into ERPNext or custom attendance systems—enabling real-time HR automation, shift tracking, and employee performance insights.</p>
          </div>
          <div className='flex flex-col gap-3'>
            <h2 className='text-lg font-semibold mt-4'>Grandstream VoIP Call Log Integration</h2>
            <p className='text-justify'>We enable automatic capture and logging of call activity from Grandstream IP phones into ERPNext CRM—enhancing sales tracking, support tickets, and lead management with zero manual effort.</p>
          </div>
       </div>
       {/* <FooterLink />
      <Footer /> */}
     </div>
  )
}

export default Services