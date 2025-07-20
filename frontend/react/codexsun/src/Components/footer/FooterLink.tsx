import facebook from '../../assets/svg/facebook.svg';
import x from '../../assets/svg/x.svg';
import pinterest from '../../assets/svg/pinterest.svg';
import youtube from '../../assets/svg/youtube.svg';
import linkedin from '../../assets/svg/linkedin.svg';
import { useState } from 'react';

function FooterLink() {
  const [link]=useState([
    {link:"http://flipkart.com/",icon:facebook},
    {link:"http://flipkart.com/",icon:x},
    {link:"http://flipkart.com/",icon:pinterest},
    {link:"http://flipkart.com/",icon:youtube},
    {link:"http://flipkart.com/",icon:linkedin},
  ])
  return (
    <div className='flex justify-center gap-5 border-t border-gray-900'>
      {
        link.map((link,idx)=>(
           <a key={idx} target='_blank' href={link.link}>
            <img className='w-10 p-2 sm:w-20 sm:p-6' src={link.icon} alt='Facebook' />
          </a>
        ))
      }
    </div>
  );
}

export default FooterLink;
