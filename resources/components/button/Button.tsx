import React, { forwardRef } from 'react';
import { Link } from 'react-router-dom';

type ButtonProps = {
  label: string;
  path?: string;
  className?: string;
  onClick?: () => void;
  children?: React.ReactNode;
} & React.ButtonHTMLAttributes<HTMLButtonElement>;

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ label, path, className = '', onClick, children, ...rest }, ref) => {
    if (path) {
      return (
        <Link
          to={path}
          onClick={onClick}
          className={`${className} px-4 py-2 rounded-md inline-block`}
        >
          {children || label}
        </Link>
      );
    }

    return (
      <button
        ref={ref}
        onClick={onClick}
        className={`${className} px-4 py-2 rounded-md cursor-pointer`}
        {...rest}
      >
        {children || label}
      </button>
    );
  }
);

Button.displayName = "Button";
export default Button;
