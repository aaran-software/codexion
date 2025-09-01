import Timeline from "../../../../../resources/UIBlocks/timeline/Timeline";
import { BookIcon } from "lucide-react";

const timelineData = [
  {
    date: "2023-08-01",
    title: 'Created "Preline in React" task',
    description: "Find more detailed instructions here.",
    user: {
      name: "James Collins",
      avatar: "https://images.unsplash.com/photo-1659482633369-9fe69af50bfb?...",
    },
    icon: <BookIcon className="size-4 mt-1" />,
  },
  {
    date: "2023-08-01",
    title: "Release v5.2.0 quick bug fix 🐞",
    user: {
      name: "Alex Gregarov",
      initial: "A",
    },
  },
  {
    date: "2023-07-31",
    title: "Take a break ⛳️",
    description: "Just chill for now... 😉",
  },
];

export default function TimelineComponent() {
  return <Timeline items={timelineData} showCollapse />;
}
