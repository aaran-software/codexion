import FloatingInput from "../../../resources/components/input/FloatingInput";
import Button from "../../../resources/components/button/Button";
import CustomTextArea from "../../../resources/components/input/CustomTextArea";
import NotificationCard from "../../../resources/components/alert/NotificationCard";
import { useState } from "react";

export default function App() {
  const [message] = useState([
    {
      date: "2025-07-22T09:30:00Z",
      title: "New Comment on Task",
      description: "Alice commented on the task 'Design Review'.",
      user: {
        name: "Alice Johnson",
        avatar: "/avatars/alice.png",
      },
      icon: <i className="text-blue-500 ri-message-3-line" />,
    },
    {
      date: "2025-07-21T14:00:00Z",
      title: "New Task Assigned",
      description: "You've been assigned to the task 'API Integration'.",
      user: {
        name: "System",
        initial: "S",
      },
      icon: <i className="text-green-500 ri-task-line" />,
    },
    {
      date: "2025-07-20T18:45:00Z",
      title: "Meeting Reminder",
      description: "Project sync scheduled for tomorrow at 10 AM.",
      user: {
        name: "Calendar Bot",
        avatar: "/avatars/calendar.png",
      },
      icon: <i className="text-yellow-500 ri-calendar-event-line" />,
    },
    {
      date: "2025-07-20T18:45:00Z",
      title: "Meeting Reminder",
      description: "Project sync scheduled for tomorrow at 10 AM.",
      user: {
        name: "Calendar Bot",
        avatar: "/avatars/calendar.png",
      },
      icon: <i className="text-yellow-500 ri-calendar-event-line" />,
    },
    {
      date: "2025-07-20T18:45:00Z",
      title: "Meeting Reminder",
      description: "Project sync scheduled for tomorrow at 10 AM.",
      user: {
        name: "Calendar Bot",
        avatar: "/avatars/calendar.png",
      },
      icon: <i className="text-yellow-500 ri-calendar-event-line" />,
    },
    {
      date: "2025-07-19T11:20:00Z",
      title: "New File Uploaded",
      description: "Bob uploaded 'wireframe-v2.pdf' to the Design folder.",
      user: {
        name: "Bob Martin",
        initial: "B",
      },
      icon: <i className="text-purple-500 ri-upload-cloud-line" />,
    },
    {
      date: "2025-07-18T08:15:00Z",
      title: "Server Downtime Notice",
      description: "Scheduled maintenance from 2 AM to 4 AM UTC.",
      user: {
        name: "DevOps",
        avatar: "/avatars/devops.png",
      },
      icon: <i className="text-red-500 ri-error-warning-line" />,
    },
  ]);
  return (
    <div className="h-screen p-10 flex py-20 flex-col text-xl gap-5">
      <h1 className="mb-4 text-center">Chat Here</h1>

      <div className="flex flex-col gap-3 w-full mx-auto flex-1">
        <FloatingInput id={"title"} label={"Title"} err={""} />

        <CustomTextArea
          id="message"
          placeholder="Write your message here..."
          className="flex-1 min-h-[400px]"
          onChange={(val) => console.log("Message:", val)}
        />

        <Button
          label={"Submit"}
          className="border border-ring/40 w-max ml-auto bg-green-500 text-white rounded-md"
        />
      </div>

      <div>
        {/* show message with timeline */}
        <div className="w-full">
          <NotificationCard items={message} />
        </div>

        {/* reply section */}
        <div className="flex flex-col mt-5 gap-5 pb-20">
          <FloatingInput id={"title"} label={"reply"} err={""} />
          <Button
            label={"Reply"}
            className="border border-ring/40 w-max ml-auto bg-update text-white rounded-md"
          />
        </div>
      </div>
    </div>
  );
}
