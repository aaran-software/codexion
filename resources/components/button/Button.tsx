import React, { forwardRef } from "react";
import { Link } from "react-router-dom";

type CommonProps = {
  label?: string;
  className?: string;
  children?: React.ReactNode;
};

type ButtonAsLink = {
  path: string;
  onClick?: () => void;
} & CommonProps &
  Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, "href">;

type ButtonAsButton = {
  path?: undefined;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
} & CommonProps &
  React.ButtonHTMLAttributes<HTMLButtonElement>;

type ButtonProps = ButtonAsLink | ButtonAsButton;

// Main component
const Button = forwardRef<HTMLButtonElement | HTMLAnchorElement, ButtonProps>(
  ({ label, path, className = "", onClick, children, ...rest }, ref) => {
    const classes = `${className} px-4 py-2 rounded-md cursor-pointer`;

    if (path) {
      return (
        <Link
          ref={ref as React.Ref<HTMLAnchorElement>}
          to={path}
          onClick={onClick}
          className={classes}
          {...(rest as Omit<ButtonAsLink, "path">)}
        >
          {children || label}
        </Link>
      );
    }

    return (
      <button
        ref={ref as React.Ref<HTMLButtonElement>}
        onClick={onClick}
        className={classes}
        {...(rest as Omit<ButtonAsButton, "path">)}
      >
        {children || label}
      </button>
    );
  }
);

Button.displayName = "Button";
export default Button;
