import { useState } from "react";
import GlobalSearch from "../../components/input/search-box";
import Timeline from "../../components/timeline/timeline";
import React from "react";

const samplePost = {
  title: "How to Build a Responsive Blog Layout with Tailwind CSS",
  description:
    "In this guide, we’ll walk you through the steps to build a clean, responsive blog layout using Tailwind CSS and React. You'll learn how to structure components, apply spacing, and ensure mobile-first responsiveness...",
  coverImage: "/assets/tomato-3919426_1280.jpg",
  author: {
    name: "John Doe",
    avatar: "/assets/product/bb6501.png",
  },
  date: "August 3, 2025",
  category: "Frontend Development",
  tags: ["React", "Tailwind CSS", "UI Design"],
};

const recentPosts = [
  {
    title: "10 Tips for Writing Clean React Code",
    author: "Jane Smith",
    date: "July 30, 2025",
    thumbnail: "/assets/tomato-3919426_1280.jpg",
  },
  // Add more recent post objects here...
];

const initialComments = [
  {
    date: "2025-08-04",
    title: "User signed up",
    description: "Muthu created an account using email.",
    user: { name: "Muthu", initial: "M" },
    icon: <span>🎉</span>,
  },
  {
    date: "2025-08-04",
    title: "Profile updated",
    description: "Changed profile picture and bio.",
    user: { name: "Muthu", avatar: "/images/muthu.jpg" },
    icon: <span>📝</span>,
  },
  {
    date: "2025-08-03",
    title: "Password changed",
    description: "User updated password for security.",
    user: { name: "Muthu", initial: "M" },
    icon: <span>🔒</span>,
  },
  {
    date: "2025-08-01",
    title: "Email verified",
    description: "User clicked verification link.",
    user: { name: "Muthu", initial: "M" },
    icon: <span>✅</span>,
  },
];
function BlogLayout1() {
  const post = samplePost;

  const [comments, setComments] = useState(initialComments);
  const [newComment, setNewComment] = useState("");

  const handleSubmit = () => {
    if (!newComment.trim()) return;
    const newEntry = {
      date: new Date().toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
      }),
      title: "Password changed",
      description: "User updated password for security.",
      user: { name: "Muthu", initial: "M" },
      icon: <span>🔒</span>,
    };
    setComments([newEntry, ...comments]);
    setNewComment("");
  };
  return (
    <div>
      {/* Banner Section */}
      <div className="relative h-[50vh] md:h-[70vh] w-full">
        <img
          src="/assets/Benefits Application 2.jpg"
          alt="Sample"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-foreground/60" />
        <div className="absolute inset-0 flex items-center">
          <div className="md:w-2/3 px-5 lg:px-[10%] text-white space-y-4">
            <h1 className="text-2xl lg:text-4xl font-bold animate__animated animate__fadeIn animate__fast">
              Blogs
            </h1>
            <p className="text-sm sm:text-md lg:text-lg text-justify animate__animated animate__fadeIn animate__slow">
              Explore insightful articles, practical tips, and fresh
              perspectives on topics that matter — curated to inform, inspire,
              and ignite conversation.
            </p>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-[70%_30%] gap-8 mt-5 px-5 md:px-[10%]">
        {/* Blog Post */}
        <div className="flex flex-col gap-6 lg:overflow-y-auto scrollbar-hide pr-2">
          <img
            src={post.coverImage}
            alt="Blog Cover"
            className="rounded-xl w-full object-cover"
          />

          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <img
              src={post.author.avatar}
              className="rounded-full w-7 h-7 object-scale-down"
              alt="Author"
            />
            <p className="font-semibold text-black">{post.author.name}</p>
            <span>•</span>
            <p>{post.date}</p>
          </div>

          <h1 className="text-4xl font-bold text-gray-900 leading-tight">
            {post.title}
          </h1>

          <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
            <p className="font-medium">Category:</p>
            <span className="px-3 py-1 bg-foreground/10 rounded-full">
              {post.category}
            </span>
            <p className="font-medium ml-4">Tags:</p>
            {post.tags.map((tag, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-foreground/10 rounded-full"
              >
                #{tag}
              </span>
            ))}
          </div>

          <p className="text-lg text-gray-700 leading-relaxed mt-3">
            {post.description}
          </p>

          <div className="mt-10 border-t pt-6 space-y-6">
            <h2 className="text-2xl font-semibold">Comments</h2>

            <Timeline items={comments} showCollapse isHeading={false} />

            {/* Comment Input */}
            <div className="mt-6 space-y-3">
              <textarea
                className="w-full border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                rows={4}
                placeholder="Write a comment..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
              />
              <button
                onClick={handleSubmit}
                className="bg-primary text-white px-5 py-2 rounded-md hover:bg-primary/90 transition"
              >
                Submit Comment
              </button>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="flex flex-col gap-6 h-full pr-1 lg:border-l lg:pl-5 border-ring/30">
          <hr className="lg:hidden border-ring/30" />
          <GlobalSearch />
          <h2 className="text-xl font-semibold border-b pb-2">Recent Posts</h2>

          {recentPosts.map((recent, idx) => (
            <div
              key={idx}
              className="grid grid-cols-[30%_70%] gap-4 items-start"
            >
              <img
                src={recent.thumbnail}
                alt="Thumbnail"
                className="rounded-md w-full object-scale-down aspect-video"
              />
              <div className="flex flex-col">
                <h3 className="text-lg font-bold text-gray-800 line-clamp-2">
                  {recent.title}
                </h3>
                <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                  <p className="font-medium">{recent.author}</p>
                  <span>•</span>
                  <p>{recent.date}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default BlogLayout1;
