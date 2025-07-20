import { useState } from 'react';
import { Link as ScrollLink } from 'react-scroll';
import logo from '../../assets/svg/logo.svg';
import { IoMdMenu } from "react-icons/io";
import { IoClose } from "react-icons/io5";
import Button from '../Input/Button';
// import { ModeToggle } from '../mode-toggle';

type MenuItem = {
  label: string;
  path: string;
};

function HeaderPortfolio() {
  const [menuVisible, setMenuVisible] = useState(false);

  const [menu] = useState<MenuItem[]>([
    { label: 'Home', path: 'home' },
    { label: 'About Us', path: 'about' },
    { label: 'Industry', path: 'industry' },
    { label: 'Services', path: 'services' },
    { label: 'Contact', path: 'contact' },
  ]);

  return (
    <div className='bg-white flex flex-row justify-between h-20 items-center px-5 py-2 md:py-4 w-full fixed top-0 left-0 z-50 shadow-md'>
      {/* Logo */}
      <div className='flex items-center gap-5'>
        <img src={logo} alt='Agency Logo' className='w-25 object-contain' />
      </div>

      {/* Desktop Menu */}
      <ul className='hidden md:flex flex-row justify-between gap-10 items-center'>
        {menu.map((item, index) => (
          <li key={index} className='relative group'>
            <ScrollLink
              to={item.path}
              smooth={true}
              duration={600}
              offset={-70}
              spy={true}
              activeClass="text-[#6ab48d] border-b-3 border-b-[#6ab48d]"
              className="cursor-pointer text-lg text-black hover:text-[#6ab48d] transition-all duration-200"
            >
              {item.label}
            </ScrollLink>
            <span className='absolute left-0 bottom-0 h-0.5 w-full transform scale-x-0 origin-left group-hover:scale-x-100 group-hover:bg-[#6ab48d] transition-transform duration-100 ease-in-out'></span>
          </li>
        ))}
      </ul>

      {/* Desktop Buttons */}
      <div className='md:flex gap-2 hidden'>
          <Button
            label='LOGIN'
            path='/login'
            className='bg-gradient-to-r from-[#23aa70] to-[#0e854f] text-gray-50 px-5 py-2 text-md hover:from-[#2cc984] hover:to-[#169c60]'
            children={undefined}
          />
        {/* <ModeToggle /> */}
      </div>

      {/* Mobile Menu Icon */}
      <div className='flex md:hidden' onClick={() => setMenuVisible(!menuVisible)}>
        <IoMdMenu size={25} />
      </div>

      {/* Mobile Menu Dropdown */}
      <ul
        className={`md:hidden transform transition-all duration-400 ease-in-out flex flex-col gap-5 w-full bg-black text-gray-50 p-4 absolute top-0 left-0 z-50 ${
          menuVisible ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0'
        }`}
      >
        {/* Close icon */}
        <div className='absolute right-0 top-0 mt-10 mr-5' onClick={() => setMenuVisible(false)}>
          <IoClose size={25} />
        </div>

        {/* Mode toggle */}
        {/* <div className='absolute left-0 top-0 mt-10 ml-5'>
          <ModeToggle />
        </div> */}

        {/* Mobile Links */}
        <div className='flex flex-col mt-16'>
          {menu.map((item, index) => (
            <ScrollLink
              key={index}
              to={item.path}
              smooth={true}
              duration={600}
              offset={-70}
              onClick={() => setMenuVisible(false)}
              className='border-b w-full border-gray-500 p-2 mt-5 hover:text-[#23aa70] last:border-b-0 cursor-pointer'
            >
              {item.label}
            </ScrollLink>
          ))}
        </div>

        {/* Login Button */}
        <div>
            <Button
              label='LOGIN'
              path='/login'
               onClick={() => setMenuVisible(false)}
              className='bg-gradient-to-r from-[#23aa70] to-[#0e854f] text-gray-50 px-5 py-2 text-md hover:from-[#2cc984] hover:to-[#169c60]'
              children={undefined}
            />
        </div>
      </ul>
    </div>
  );
}

export default HeaderPortfolio;
