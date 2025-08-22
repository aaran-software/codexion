
---

# 📘 FooterPortfolio Component Documentation

## Overview

The `FooterPortfolio` component is a **customizable footer section** for a website.
It displays company details, navigation links, contact info, and legal links, all passed via **props**.

---

## ✨ Props

The component accepts the following props:

| Prop        | Type                                 | Description                                                          | Example                                                                     |
| ----------- | ------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `address`   | `string[]`                           | List of address lines to be displayed in the footer.                 | `["address", "street", "Coimbatore", "Tamil Nadu, India."]`                 |
| `contact`   | `string[]`                           | Contact information (e.g., email, phone).                            | `["info@techmedia.in", "9843213500"]`                                       |
| `company`   | `{ label: string; link: string; }[]` | List of company-related links.                                       | `[{ label: "Home", link: "/home" }, { label: "About", link: "/about" }]`    |
| `project`   | `{ label: string; link: string; }[]` | List of project/product links.                                       | `[{ label: "Billing", link: "/" }, { label: "Portfolio", link: "/about" }]` |
| `legal`     | `{ label: string; link: string; }[]` | Legal-related links (Privacy Policy, T\&C, etc.).                    | `[{ label: "Privacy Policy", link: "/" }]`                                  |
| `brandName` | `string`                             | The company/brand name to display at the bottom of the footer.       | `"Tech Media"`                                                              |
| `year`      | `number`                             | The copyright year. Can be passed manually or generated dynamically. | `2025`                                                                      |

---

## 🛠️ Example Usage

```tsx
import FooterPortfolio from "./FooterPortfolio";

export default function App() {
  return (
    <div>
      {/* Main content here */}

      <FooterPortfolio
        address={[
          "123 Main Street",
          "Coimbatore, Tamil Nadu, India",
          "PIN - 641001",
        ]}
        contact={["support@techmedia.in", "+91 9843213500"]}
        company={[
          { label: "Home", link: "/" },
          { label: "About Us", link: "/about" },
          { label: "Contact", link: "/contact" },
          { label: "Services", link: "/services" },
        ]}
        project={[
          { label: "Billing", link: "/billing" },
          { label: "Portfolio", link: "/portfolio" },
        ]}
        legal={[
          { label: "Privacy Policy", link: "/privacy" },
          { label: "Terms & Conditions", link: "/terms" },
        ]}
        brandName="Tech Media"
        year={new Date().getFullYear()}
      />
    </div>
  );
}
```

---

## 🎨 Expected UI Layout

* **Left side** → Address & Contact info.
* **Middle columns** → Company, Project, and Legal links.
* **Bottom** → Brand name with © copyright.

---

## ✅ Notes

* No default values are used. You must provide all props explicitly.
* `year` can be dynamically generated using `new Date().getFullYear()`.
* You can style the component with Tailwind/SCSS as needed.

---
