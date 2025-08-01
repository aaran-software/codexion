import DynamicCard from "../../../../resources/components/card/DynamicCard";
import Carousel from "../../../../resources/components/carousel";
import Button from "../../../../resources/components/button/Button";
import Card2 from "../../../../resources/components/card/Card2";

function Home() {
    const images = [
        "/assets/Homepage3.jpg",
        "/assets/Homepage2.JPG",
        "/assets/Homepage1.jpg",
        "/assets/Homepage4.jpg",
    ];

    const product = [
        {
            image: "/assets/product/bb6501.jpg",
            title: "Creative Design",
        },
        {
            image: "/assets/product/coco-coins.jpg",
            title: "Tech Landing",
        },
        {
            image: "/assets/product/CoirFiber.jpeg",
            title: "E-commerce Showcase",
        },
        {
            image: "/assets/product/Cocopeat5kgBlock.png",
            title: "E-commerce Showcase",
        },
        {
            image: "/assets/product/Cocohuskchipsblock.jpeg",
            title: "E-commerce Showcase",
        },
        {
            image: "/assets/product/Cocodiscsseedling.jpg",
            title: "E-commerce Showcase",
        },
    ];

    const manufacture = [
        {
            image: "/assets/manufacturing/1 Coconut Husk Sourcing.jpg",
            title: "Creative Design",
        },
        {
            image: "/assets/manufacturing/2 Coconut Husk processing.jpg",
            title: "Tech Landing",
        },
        {
            image: "/assets/manufacturing/3 Filtering Fibers from Peat.jpg",
            title: "E-commerce Showcase",
        },
        {
            image: "/assets/manufacturing/4 Seived CocoPeat Separation.jpg",
            title: "E-commerce Showcase",
        },
        {
            image: "/assets/manufacturing/5 Washing Cocopeat.JPG",
            title: "E-commerce Showcase",
        },
        {
            image: "/assets/manufacturing/6 Drying.jpg",
            title: "E-commerce Showcase",
        },
    ];
    const company = [
        {
            title: 'Our Strength',
            body: 'High Quality Products - Right time delivery - Best price in the market – Tailor made services - 100% Positive Feedback'
        },
        {
            title: 'Our Process',
            body: 'Coconut Husk Feeding – Crushing – Separating Peat from Fiber – Peat Washing – Drying – Compressing as blocks'
        },
    ];
    return (
        <div className="">
            <Carousel autoSlide autoSlideInterval={4000} startIndex={0}>
                {images.map((src, index) => (
                    <img
                        key={index}
                        src={src}
                        alt={`Slide ${index + 1}`}
                        className="w-full h-[100vh] object-fit"
                    />
                ))}
            </Carousel>

            <div className="container mx-auto px-[10%]">
                <Card2 items={company} containerStyle={"grid-cols-1 sm:grid-cols-2"}/>
            </div>
            <div className="relative h-[80vh] mt-10 w-full">
                {/* Background Image */}
                <img
                    src="/assets/Homepage1.jpg"
                    alt="Sample"
                    className="h-full w-full object-fit"
                />

                {/* Overlay */}
                <div className="absolute inset-0 bg-foreground/60"></div>

                {/* Text Content */}
                <div className="absolute inset-0 flex items-center">
                    <div className="md:w-1/2 px-[10%] text-white space-y-4">
                        <h1 className="text-4xl font-bold">Link Agro Exports</h1>
                        <p className="text-lg">Link Agro Exports is a distinguished manufacturer and exporter of
                            high-quality coco peat products. Our plant is located in Uchipuli, Tamilnadu which is known
                            for its conducive climate for coconut cultivation, particularly for tender coconut (green
                            coconut). And this place has excellent ground water source. Hence this geographical
                            feasibility enables us producing good quality coir and coco-peat products.</p>
                        <Button
                            label="Read More"
                            path="/about"
                            className="border border-ring/40"
                        />
                    </div>
                </div>
            </div>

            <div className="px-[10%]">
                <h1 className="text-center font-bold text-4xl my-5">Our Products</h1>
                <DynamicCard
                    Card={product}
                    containerStyle="grid-cols-1 sm:grid-cols-2 md:grid-cols-3"
                />
            </div>

            <Button
                label="View More"
                path="/product"
                className="border border-ring/40 !rounded-full block mx-auto my-3 w-max"
            />


            <div className="px-[10%]">
                <h1 className="text-center font-bold text-4xl my-5">Manufacturing</h1>
                <DynamicCard
                    Card={manufacture}
                    containerStyle="grid-cols-1 sm:grid-cols-2 md:grid-cols-3"
                    // rounded
                />
            </div>
            <Button
                label="View More"
                path="/product"
                className="border border-ring/40 !rounded-full block mx-auto my-3 w-max"
            />
        </div>
    );
}

export default Home;
