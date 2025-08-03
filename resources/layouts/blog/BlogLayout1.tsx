
import GlobalSearch from "../../components/input/search-box";
function BlogLayout1() {
  return (
    <div className="mt-25">
      <div className="grid lg:grid-cols-[70%_30%] gap-5 px-5 md:px-[10%]">
        <div className="flex flex-col gap-5">
          <img src='/assets/product/bb6501.png' alt="" />
          <div className="flex gap-2">
            <img src='/assets/product/bb6501.png' className="rounded-full w-6" alt="" />
            <p className="font-semibold">name</p>
            <p>date</p>
          </div>
          <h1 className="text-4xl font-bold line-clamp-2">Title</h1>
          <p>Description</p>
        </div>
        <div className="flex flex-col gap-5">
          <GlobalSearch />
          <div className="grid grid-cols-[30%_70%] gap-5">
            <img src='/assets/product/bb6501.png' alt="" />
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

export default BlogLayout1;
