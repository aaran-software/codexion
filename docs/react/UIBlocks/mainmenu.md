
---

# **Mainmenu Component Documentation**

## **Description**

`Mainmenu` is a dynamic React menu component for displaying product categories with nested submenus and a promotional card.
It supports multiple levels of submenus (`subMenu`, `subMenu2`, `subMenu3`, etc.) and displays a card with a title, description, and image for each category.

The component **does not require direct JSON import**; menu data is passed as a prop (`menuData`), which allows dynamic data fetching or passing from a parent component.

---

## **Props**

### `menuData` (required)

* **Type:** `MenuWrapper[]`
* **Description:** An array of menu items representing categories.
* **Structure:**

```ts
interface SubMenuItems {
  title: string;    // Display name of submenu item
  path?: string;    // URL path to navigate on click
}

interface SubMenuGroup {
  title: string;         // Submenu group title
  items: SubMenuItems[]; // Array of submenu items
}

interface CardItems {
  title: string;       // Card title
  description: string; // Card description
  image: string;       // Card image URL
}

type DynamicSubMenus = {
  [key: `subMenu${string}`]: SubMenuGroup | undefined;
};

export interface MenuItem extends DynamicSubMenus {
  name: string;    // Category name
  path: string;    // Category path for main navigation
  image: string;   // Category image URL
  alt: string;     // Alt text for image
  card: CardItems; // Card details
}

export interface MenuWrapper {
  menu: MenuItem;
}
```

### **Supported Submenu Keys**

* `subMenu`
* `subMenu2`
* `subMenu3`
* `subMenu4`
* `subMenu5`

> Each submenu contains a `title` and an array of `items`. The component will dynamically render any submenu that exists.

---

## **Usage Example**

```tsx
import React from "react";
import Mainmenu, { MenuWrapper } from "./Mainmenu";
import menuJson from "./menu.json"; // Example JSON file

const App = () => {
  // menuJson should have the structure:
  // { "Mainmenu": MenuWrapper[] }
  return (
    <div>
      <Mainmenu menuData={menuJson.Mainmenu} />
    </div>
  );
};

export default App;
```

### **Navigation**

* Clicking on a main category navigates to `/category/{category.path}`.
* Clicking on a submenu item navigates to `/category{submenuItem.path}`.

---

## **JSON Example**

```json
{
  "Mainmenu": [
    {
      "menu": {
        "name": "Laptops",
        "path": "Laptop",
        "image": "/assets/products/laptop.png",
        "alt": "Laptops image",
        "subMenu": {
          "title": "Laptop Types",
          "items": [
            { "title": "Laptop - Display", "path": "/Laptop - Display" },
            { "title": "Laptop -Carry case", "path": "/Laptop -Carry case" }
          ]
        },
        "subMenu2": {
          "title": "Memory",
          "items": [
            { "title": "Ram - Laptop DDR3", "path": "/Ram - Laptop DDR3" }
          ]
        },
        "subMenu3": {
          "title": "Accessories",
          "items": [
            { "title": "Laptop Bag - Asus", "path": "/Laptop Bag - Asus" }
          ]
        },
        "card": {
          "title": "Top Laptop Deals",
          "description": "Browse the latest laptops for work, gaming, or everyday use.",
          "image": "/assets/products/laptop.png"
        }
      }
    }
  ]
}
```

> You can expand the JSON with `Desktops`, `PC Hardwares`, `Printer`, `Camera`, etc., using the same structure. The component will render multiple categories and submenus automatically.

---

## **Key Features**

1. Dynamic rendering of **main categories** and **submenus**.
2. **Hover effect** shows submenu with card preview.
3. Supports **multiple levels of submenus** (`subMenu` to `subMenu5`).
4. **Flexible JSON** structure allows addition of new categories or submenus without modifying the component.
5. **Responsive positioning** of submenu to prevent overflow outside viewport.
6. Uses **React Portal** to render submenu above other content.

---
