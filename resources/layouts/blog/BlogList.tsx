import { useNavigate } from "react-router-dom";
import GlobalSearch from "../../components/input/search-box";

function BlogList() {
    const navigate=useNavigate();
    const handleBlog = (id:any) =>{
        navigate(`/blog/${id}`)
    }
  return (
    <div className="">
      <div className="relative h-[50vh] md:h-[70vh] w-full">
        {/* Background Image */}
        <img
          src="/assets/Benefits Application 2.jpg"
          alt="Sample"
          className="h-full w-full object-fit"
        />

        {/* Overlay */}
        <div className="absolute inset-0 bg-foreground/60"></div>

        {/* Text Content */}
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

      <div className="grid lg:grid-cols-[70%_30%] gap-5 px-5 md:px-[10%] mt-10">
        <div >
          <div className="grid grid-cols-[40%_60%] gap-5 mb-5 cursor-pointer" onClick={()=>{handleBlog(1)}}>
            <img src="/assets/product/bb6501.png" alt="" />
            <div className="flex flex-col">
              <h1 className="text-3xl font-bold line-clamp-2">Title</h1>
              <h1 className="text-xl  line-clamp-2">Description</h1>
              <div className="flex gap-2">
                <p className="font-semibold">name</p>
                <p>date</p>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-[40%_60%] gap-5 cursor-pointer">
            <img src="/assets/product/bb6501.png" alt="" />
            <div className="flex flex-col">
              <h1 className="text-3xl font-bold line-clamp-2">Title</h1>
              <h1 className="text-xl  line-clamp-2">Description</h1>
              <div className="flex gap-2">
                <p className="font-semibold">name</p>
                <p>date</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col gap-5 lg:border-l lg:pl-5 border-ring/30">
        <hr className="text-ring/30 lg:hidden" />
          <GlobalSearch />
          <div className="grid grid-cols-[30%_70%] gap-5">
            <img src="/assets/product/bb6501.png" alt="" />
            <div className="flex flex-col">
              <h1 className="text-xl font-bold line-clamp-2">Title</h1>
              <div className="flex gap-2">
                <p className="font-semibold">name</p>
                <p>date</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BlogList;
