import { useState } from "react";
import { Link } from "react-router-dom";
import { Link as ScrollLink } from "react-scroll";
import FooterLink from "./FooterLink";

function FooterPortfolio() {
  const [address]=useState([
    'address','street','Coimbatore,','pin code','Tamilnadu, India.',
  ])

  const [contact]=useState([
    'info@Techmedia.in','9843213500',
  ])
  const [company]=useState([
    {
      label:"Home",
      link:"home"
    },
    {
      label:"About",
      link:"about"
    },
    {
      label:"Contact",
      link:"contact"
    },
    {
      label:"Product",
      link:"industry"
    },
    {
      label:"Features",
      link:"services"
    },

  ])
  // Projects

   const [project]=useState([
    {
      label:"Billing",
      link:"/"
    },
    {
      label:"Portfolio",
      link:"/about"
    },

  ])


  const [legal]=useState([
    {
      label:"Privacy Policy",
      link:"/"
    },
    {
      label:"Terms & Conditions",
      link:"/about"
    },
    {
      label:"Return Policy",
      link:"/contact"
    },
    {
      label:"Accessibility",
      link:"/blog"
    },

  ])

  return (
   <div>
          <FooterLink />

     <footer className="bg-foreground pt-10">
      
      <div className="mb-5">
        <div className="grid grid-cols-2 md:grid-cols-4 p-5 lg:px-[12%] gap-5 text-background bg-foreground/90">
          <div className="flex flex-col gap-4">
            <div className="text-sm font-bold text-[#128d57]">Tech Media</div>
            <div className="flex flex-col gap-2">
              {
              address.map((address,idx)=>(
                <p className="text-sm" key={idx}>{address}</p>
              ))
            }
            </div>
              <div>
                 {
              contact.map((contact,idx)=>(
                <p className="text-sm" key={idx}>{contact}</p>
              ))
            }
              </div>
          </div>

         <div className="flex flex-col gap-4">
        <div className="text-sm font-bold text-[#128d57]">Tech Media</div>
        <div className="flex flex-col gap-2">
            {company.map((company, idx) => (
            <ScrollLink
                key={idx}
                to={company.link}
                smooth={true}
                duration={600}
                offset={-70}
                // spy={true}
                activeClass="text-[#6ab48d] border-l-4 border-[#6ab48d] pl-2"
                className="cursor-pointer text-white hover:text-[#6ab48d] transition-all duration-200 text-sm"
            >
                {company.label}
            </ScrollLink>
            ))}
        </div>
        </div>

{/* Projects */}
             <div className="flex flex-col gap-4">
            <div className="text-sm font-bold text-[#128d57]">Project</div>
                   <div className="flex flex-col gap-2">
              {
              project.map((project,idx)=>(
                <Link key={idx} className="flex flex-col text-sm" to={project.link}>{project.label}</Link>
              ))
            }
            </div>
          </div>
           <div className="flex flex-col gap-4">
            <div className="text-sm font-bold text-[#128d57]">Legal</div>
                  <div className="flex flex-col gap-2">
              {
              legal.map((legal,idx)=>(
                <Link key={idx} className="flex flex-col text-sm" to={legal.link}>{legal.label}</Link>
              ))
            }
            </div>
          </div>
        </div>
      </div>
      <div className="border-t border-gray-200 bg-foreground text-white">
        {/* <div className="flex">
           {
              link.map((link,idx)=>(
                <a key={idx} target='_blank' href={link.link}>
                  <img className='w-5 m-3' src={link.icon} alt='Facebook' />
                </a>
              ))
            }
        </div> */}
        <div className='text-sm text-center  px-2 py-7'>
          Copyright &copy; 2025 Tech Media. Powered by Aaran Software
        </div>
      </div>
   
    </footer>
   </div>
  );
}

export default FooterPortfolio;
