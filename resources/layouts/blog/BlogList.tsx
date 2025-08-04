import { useNavigate } from "react-router-dom";
import GlobalSearch from "../../components/input/search-box";

const blogs = [
  {
    id: 1,
    title: "Benefits of Cocopeat in Modern Farming",
    description: "Cocopeat improves water retention, aeration, and root health, making it ideal for sustainable agriculture.",
    author: "Muthukumaran R.",
    date: "Aug 3, 2025",
    image: "/assets/product/bb6501.png",
    category: "Agriculture",
    tags: ["Cocopeat", "Farming", "Soil Health"],
    likes: 12,
  },
  {
    id: 2,
    title: "5 Organic Substrates You Should Know",
    description: "Discover top organic growing mediums and how they compare to cocopeat in performance and sustainability.",
    author: "Divya K.",
    date: "Jul 28, 2025",
    image: "/assets/product/bb6501.png",
    category: "Organic Farming",
    tags: ["Substrates", "Organic", "Eco Farming"],
    likes: 8,
  },
];

const categories = [...new Set(blogs.map(blog => blog.category))];
const tags = [...new Set(blogs.flatMap(blog => blog.tags))];

function BlogList() {
  const navigate = useNavigate();

  const handleBlog = (id: number) => {
    navigate(`/blog/${id}`);
  };

  return (
    <div className="">
      {/* Hero Section */}
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
              Explore insightful articles, practical tips, and fresh perspectives on topics that matter — curated to inform, inspire, and ignite conversation.
            </p>
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="grid lg:grid-cols-[70%_30%] gap-5 px-5 md:px-[10%] mt-10">
        {/* Blog List */}
        <div className="space-y-5">
          {blogs.map((blog) => (
            <div
              key={blog.id}
              onClick={() => handleBlog(blog.id)}
              className="grid grid-cols-[40%_60%] gap-5 p-3 border border-ring/30 rounded-md hover:shadow cursor-pointer transition"
            >
              <img src={blog.image} alt={blog.title} className="object-scale-down w-full h-full" />
              <div className="flex flex-col justify-between pr-4">
                <div>
                  <h2 className="text-xl font-bold line-clamp-2">{blog.title}</h2>
                  <p className="text-sm line-clamp-2 md:line-clamp-3 mt-1 text-muted-foreground">{blog.description}</p>
                </div>
                <div className="mt-2 text-xs text-muted-foreground flex flex-wrap gap-2">
                  <span className="font-semibold">{blog.author}</span>
                  <span>{blog.date}</span>
                  <span className="bg-primary/10 px-2 rounded text-primary">{blog.category}</span>
                  <span>👍 {blog.likes}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar */}
        <div className="flex flex-col gap-6 lg:border-l lg:pl-5 border-ring/30">
          <hr className="lg:hidden border-ring/30" />
          <GlobalSearch />

          {/* Categories */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Categories</h3>
            <ul className="space-y-1 text-sm text-muted-foreground">
              {categories.map((cat, idx) => (
                <li key={idx} className="hover:text-primary cursor-pointer">
                  • {cat}
                </li>
              ))}
            </ul>
          </div>

          {/* Tags */}
          <div>
            <h3 className="text-lg font-semibold mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {tags.map((tag, idx) => (
                <span
                  key={idx}
                  className="text-xs bg-muted px-2 py-1 rounded hover:bg-primary hover:text-white cursor-pointer"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BlogList;
