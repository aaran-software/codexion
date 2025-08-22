
---

# **ServicesCard Component Documentation**

## **Overview**

CardView is a React functional component built with TypeScript and Tailwind CSS. It is designed to render a **grid of service cards**, each displaying a title, description, and list of features.

---

## **Props**

### **CardViewProps**

| Prop Name | Type      | Description                                                                      |
| --------- | --------- | -------------------------------------------------------------------------------- |
| `items`   | `Items[]` | An array of service items to render. Each item represents a single service card. |

### **Items Type**

| Field         | Type       | Description                                          |
| ------------- | ---------- | ---------------------------------------------------- |
| `id`          | `number`   | Unique identifier for the service item.              |
| `title`       | `string`   | The title of the service.                            |
| `description` | `string`   | A short description explaining the service.          |
| `features`    | `string[]` | A list of key features or highlights of the service. |

---

## **Component Structure**

```tsx
const CardView: React.FC<CardViewProps> = ({ items }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:px-[12%] gap-6  mx-3">
      {items.map((item) => (
        <div key={item.id} className="bg-gradient-to-tr from-primary/20 to-background rounded-xl p-6 border border-ring/30 hover:shadow-2xl hover:border-0">
          <h3 className="text-lg font-bold mb-2">{item.id}. {item.title}</h3>
          <p className="text-foreground/70 mb-4 text-justify">{item.description}</p>
          <ul className="space-y-2">
            {item.features.map((feature, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-green-500 mr-2">✔</span>
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};
```

---

## **Usage**

### **1. Import the component**

```tsx
import CardView from './ServicesCard';
```

### **2. Create the service array**

```tsx
const service = [
  {
    id: 1,
    title: "UI/UX Design",
    description: "Interfaces that delight users and drive conversions. We design with outcomes in mind.",
    features: ["User flows that boost engagement.", "Mobile-first, award-worthy interfaces.", "Prototypes in 72 hours or less."],
  },
  {
    id: 2,
    title: "Brand Design",
    description: "Visual identities that command attention and build trust. Logos, style guides, and assets crafted to tell your story.",
    features: ["Logos with hidden storytelling.", "Visual identities built to scale.", "Style guides even your interns can use."],
  },
  {
    id: 3,
    title: "Webflow Development",
    description: "Websites that load fast, rank higher, and grow with you. No bloated code—just seamless Webflow experiences.",
    features: ["90+ PageSpeed scores guaranteed.", "SEO-optimized out of the box.", "Editable CMS for non-tech teams."],
  },
  {
    id: 4,
    title: "No-Code Development",
    description: "Launch functional MVPs without engineering headaches. Solutions in weeks, not months.",
    features: ["Bubble/FlutterFlow MVPs in 4 weeks.", "Complex workflows without engineers.", "API integrations that actually work."],
  },
];
```

### **3. Render the component**

```tsx
<CardView items={service} />
```

---

## **Styling**

* Uses **Tailwind CSS** for styling.
* Grid layout is **responsive**:

  * 1 column on mobile (`grid-cols-1`)
  * 2 columns on medium screens (`md:grid-cols-2`)
  * 4 columns on large screens (`lg:grid-cols-4`)
* Cards have **rounded corners**, **shadow**, and **padding**.
* Feature list uses a **checkmark icon** (✔) with green color for visual emphasis.

---

## **Advantages**

1. **Reusable** – Can render any number of service cards.
2. **Responsive** – Grid adjusts to screen size.
3. **Clean API** – Only requires an array of items.
4. **Self-contained** – All mapping logic is inside `CardView`.

---
