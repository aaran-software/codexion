# 📘 Accordion Component Documentation

### 📌 Overview

The `Accordion` component provides a collapsible section UI, commonly used for FAQs or content toggles.
It supports **three icon variants** (`cross`, `chevron`, `plus`) to indicate expanded/collapsed state.

---

### ⚙️ Props

| Prop    | Type                                     | Default      | Description                                    |
| ------- | ---------------------------------------- | ------------ | ---------------------------------------------- |
| `title` | `string`                                 | `undefined`  | Optional heading for the accordion group.      |
| `items` | `{ question: string; answer: string }[]` | **Required** | List of accordion items.                       |
| `type`  | `"cross" \| "chevron" \| "plus"`         | `"cross"`    | Icon style used for expand/collapse indicator. |

---

### 🔎 Code Walkthrough

#### 1. Imports & Interfaces

```tsx
import { useRef, useState } from "react"

interface AccordionItem {
  question: string
  answer: string
}

interface AccordionProps {
  title?: string
  items: AccordionItem[]
  type?: "cross" | "chevron" | "plus"
}
```

* `useRef` and `useState` are imported from React.
* `AccordionItem` defines the shape of each FAQ entry.
* `AccordionProps` describes what the component accepts: optional `title`, required `items`, and icon `type`.

---

#### 2. State & Refs

```tsx
const [activeAccordion, setActiveAccordion] = useState<string>("")
const contentRefs = useRef<Record<string, HTMLDivElement | null>>({})
```

* `activeAccordion` holds the currently opened accordion ID.
* `contentRefs` is a dictionary of refs to each accordion content, used for smooth `maxHeight` animations.

---

#### 3. Toggle Handler

```tsx
const toggleAccordion = (id: string) => {
  setActiveAccordion((prev) => (prev === id ? "" : id))
}
```

* If the clicked item is already open → close it.
* Otherwise → set it as the new active accordion.

---

#### 4. Rendering Wrapper & Title

```tsx
<div>
  {title && (
    <div className="mb-2 text-lg font-medium py-5 text-neutral-700 dark:text-neutral-200">
      {title}
    </div>
  )}
```

* Optionally renders a **title heading** if provided.

---

#### 5. Accordion Items

```tsx
<div className="relative w-full mx-auto overflow-hidden text-sm font-normal border border-border divide-y divide-border rounded-md bg-background text-foreground">
  {items.map((item, index) => {
    const id = `accordion-${index}`
    const isActive = activeAccordion === id
```

* Loops through `items`.
* Creates a **unique ID** per accordion (`accordion-0`, `accordion-1`, …).
* Checks whether the item is **currently active**.

---

#### 6. Accordion Button

```tsx
<button
  onClick={() => toggleAccordion(id)}
  className="flex items-center justify-between w-full p-4 text-left select-none hover:text-foreground/90 transition-colors"
>
  <span>{item.question}</span>
  {/* Icon variant goes here */}
</button>
```

* Each item renders a clickable button.
* On click → toggles the accordion.
* Shows the **question** text.

---

#### 7. Icon Variants

```tsx
{type === "chevron" && (/* rotates arrow */)}
{type === "plus" && (/* plus-to-cross animation */)}
{type === "cross" && (/* rotating cross */)}
```

* Different icons are conditionally rendered depending on the `type` prop.
* Animations handled with **Tailwind CSS transitions**.

---

#### 8. Content Section

```tsx
<div
  ref={(el) => { contentRefs.current[id] = el }}
  style={{
    maxHeight: isActive ? `${contentRefs.current[id]?.scrollHeight}px` : "0px",
  }}
  className="transition-all duration-300 ease-in-out overflow-hidden"
>
  <div className="p-4 pt-0 opacity-80">{item.answer}</div>
</div>
```

* Uses `maxHeight` inline style to animate open/close smoothly.
* Stores each `div` reference inside `contentRefs`.
* Renders the **answer** inside with padding.

---

### 🚀 Usage Example

```tsx
import Accordion from "./Accordion"

const faqItems = [
  { question: "What is React?", answer: "React is a JavaScript library for building UI." },
  { question: "What is Tailwind CSS?", answer: "Tailwind is a utility-first CSS framework." },
]

export default function Example() {
  return <Accordion title="FAQ" items={faqItems} type="chevron" />
}

```

---



# 📘 NestedAccordion Component Documentation

### 📌 Overview

The `NestedAccordion` is an **expandable FAQ-style component** that supports **multi-level nesting**.
Unlike the basic `Accordion`, each item’s `answer` can be either:

* A **string** (normal text)
* An **array of child accordion items** (recursive nesting)

This makes it useful for **hierarchical data** like categories, topics, or multi-level FAQs.

---

### ⚙️ Props

| Prop    | Type                                                        | Default      | Description                                                                   |
| ------- | ----------------------------------------------------------- | ------------ | ----------------------------------------------------------------------------- |
| `title` | `string`                                                    | `undefined`  | Optional heading displayed above the accordion.                               |
| `items` | `{ question: string; answer: string \| AccordionData[] }[]` | **Required** | Accordion items. Each item can either have text or another list of sub-items. |

---

### 🔎 Code Walkthrough

#### 1. Imports & Type Definitions

```tsx
import { useState } from "react";

interface AccordionData {
  question: string;
  answer: string | AccordionData[];
}

interface NestedAccordionProps {
  title?: string;
  items: AccordionData[];
}
```

* `AccordionData` type allows `answer` to be **string or nested items**.
* `NestedAccordionProps` ensures the component receives a title and items.

---

#### 2. Root Component Wrapper

```tsx
export default function NestedAccordion({ title, items }: NestedAccordionProps) {
  return (
    <div className="space-y-2">
      {title && (
        <div className="font-semibold text-lg text-foreground py-2">{title}</div>
      )}

      <div className="rounded-lg border border-border divide-y divide-border bg-background text-foreground">
        <AccordionGroup items={items} />
      </div>
    </div>
  );
}
```

* Renders the **title** if provided.
* Wraps items inside a **styled container**.
* Delegates rendering to the **recursive `AccordionGroup`** component.

---

#### 3. AccordionGroup (Recursive Renderer)

```tsx
function AccordionGroup({ items }: { items: AccordionData[] }) {
  const [openId, setOpenId] = useState<string | null>(null);
```

* Manages which item is **currently expanded** with `openId`.
* Can only have **one open item per group** at a time.

---

#### 4. Looping Through Items

```tsx
{items.map((item, index) => {
  const id = `${item.question}-${index}`;
  const isOpen = openId === id;
  const hasChildren = Array.isArray(item.answer);
```

* Each item gets a **unique ID** (`question + index`).
* `isOpen` determines if the current item is expanded.
* `hasChildren` checks if the answer is a **nested array**.

---

#### 5. Accordion Toggle Button

```tsx
<button
  className="hs-accordion-toggle py-3 px-4 inline-flex items-center gap-x-3 w-full font-medium text-start text-foreground hover:text-foreground/90 transition-colors"
  aria-expanded={isOpen}
  aria-controls={`collapse-${id}`}
  onClick={() => setOpenId(isOpen ? null : id)}
>
  {isOpen ? <MinusIcon size={16} /> : <PlusIcon size={16} />}
  {item.question}
</button>
```

* Button toggles open/close state.
* `aria-expanded` + `aria-controls` improve **accessibility**.
* Displays **plus/minus icons** depending on state.

---

#### 6. Content Section

```tsx
<div
  id={`collapse-${id}`}
  className={`hs-accordion-content transition-all duration-300 ease-in-out overflow-hidden ${
    isOpen ? "block" : "hidden"
  }`}
  role="region"
  aria-labelledby={`heading-${id}`}
>
  {hasChildren ? (
    <div className="ml-5">
      <AccordionGroup items={item.answer as AccordionData[]} />
    </div>
  ) : (
    <div className="px-4 pb-4 pl-10 text-foreground/70">
      <em>{item.answer as any}</em>
    </div>
  )}
</div>
```

* Content expands only if `isOpen`.
* If the item has children → recursively renders **another `AccordionGroup`** (nested accordion).
* Otherwise, displays a **simple text answer**.

---

#### 7. Plus / Minus Icons

```tsx
function PlusIcon({ size }: { size: number }) { ... }
function MinusIcon({ size }: { size: number }) { ... }
```

* SVG icons for expand/collapse states.
* Passed a `size` prop for flexible scaling.

---

### 🚀 Usage Example

```tsx
import NestedAccordion from "./NestedAccordion"

const nestedFaq = [
  {
    question: "General Questions",
    answer: [
      { question: "What is React?", answer: "A library for building UIs." },
      { question: "Is it open source?", answer: "Yes, maintained by Meta." },
    ],
  },
  {
    question: "Advanced",
    answer: [
      {
        question: "Nested Topics",
        answer: [
          { question: "Hooks", answer: "Functions like useState, useEffect, etc." },
          { question: "Context API", answer: "State management solution in React." },
        ],
      },
    ],
  },
]

export default function Example() {
  return <NestedAccordion title="FAQ" items={nestedFaq} />
}
```