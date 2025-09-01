import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "../../../../../resources/components/avatar";
import Accordion from "../../../../../resources/components/accordion/Accordion";
import NestedAccordion from "../../../../../resources/components/Accordion/Nested-Accordion";

function AccordionComponent() {
  return (
    <div className="w-[60%]">
      <Avatar className="size-10">
        <AvatarImage src="/assets/user.png" alt="Jay Patel" />
        <AvatarFallback delayMs={200}>JP</AvatarFallback>
      </Avatar>

      <Accordion
        title="With Arrow"
        type="chevron"
        items={[
          {
            question: "What is React?",
            answer: "A JS library for building UI.",
          },
          {
            question: "What is TSX?",
            answer: "A syntax extension for React + TypeScript.",
          },
        ]}
      />
      <Accordion
        title="Plus to Cross"
        type="cross"
        items={[
          {
            question: "What is React?",
            answer: "A JS library for building UI.",
          },
          {
            question: "What is TSX?",
            answer: "A syntax extension for React + TypeScript.",
          },
        ]}
      />
      <Accordion
        title="Plus to Minus"
        type="plus"
        items={[
          {
            question: "What is React?",
            answer: "A JS library for building UI.",
          },
          {
            question: "What is TSX?",
            answer: "A syntax extension for React + TypeScript.",
          },
        ]}
      />
      <NestedAccordion
        title="FAQs"
        items={[
          {
            question: "Accordion",
            answer: [
              {
                question: "Sub accordion",
                answer: "This is the first item's accordion body.",
              },
              {
                question: "Sub accordion",
                answer: "This is the second item's accordion body.",
              },
              {
                question: "Sub accordion",
                answer: "This is the third item's accordion body.",
              },
            ],
          },
          {
            question: "Accordion",
            answer: "This is the second item's accordion body.",
          },
          {
            question: "Accordion",
            answer: "This is the third item's accordion body.",
          },
        ]}
      />
    </div>
  );
}

export default AccordionComponent;
