import React, { useState, useEffect, type ReactNode } from 'react';
import { ChevronLeft, ChevronRight } from "react-feather";

interface CarouselProps {
    children: ReactNode | ReactNode[];
    autoSlide?: boolean;
    autoSlideInterval?: number;
    startIndex?: number;
}

const Carousel: React.FC<CarouselProps> = ({
    children,
    autoSlide = false,
    autoSlideInterval = 3000,
    startIndex = 0,
}) => {
    // Transform children into an array
    const slides = React.Children.toArray(children);
    const [curr, setCurr] = useState(startIndex);

    const prev = () =>
        setCurr((prev) =>
            prev === 0 ? slides.length - 1 : prev - 1
        );

    const next = () =>
        setCurr((prev) =>
            prev === slides.length - 1 ? 0 : prev + 1
        );

    useEffect(() => {
        if (!autoSlide) return;

        const slideInterval = setInterval(next, autoSlideInterval);
        return () => clearInterval(slideInterval);
    }, [autoSlide, autoSlideInterval]);

    return (
        <div className='overflow-hidden relative'>
            <div
                className='flex transition-transform ease-out duration-500'
                style={{ transform: `translateX(-${curr * 100}%)` }}>
                {slides.map((child, i) => (
                    <div
                        key={i}
                        className='flex-none w-full'
                    >
                        {child}
                    </div>
                ))}
            </div>

            {/* Navigation arrows */}
            <div className='absolute inset-0 flex items-center justify-between p-4 opacity-15'>
                <button
                    aria-label='Previous slide'
                    onClick={prev}
                    className='p-1 rounded-full shadow bg-gray-100/80 text-gray-800 hover:text-white hover:bg-gray-700'
                >
                    <ChevronLeft />
                </button>
                <button
                    aria-label='Next slide'
                    onClick={next}
                    className='p-1 rounded-full shadow bg-gray-100/80 text-gray-800 hover:text-white hover:bg-gray-700'
                >
                    <ChevronRight />
                </button>
            </div>

            {/* Indicator bullets */}
            <div className='absolute bottom-4 right-0 left-0 flex items-center justify-center gap-2'>
                {slides.map((_, i) => (
                    <div
                        key={i}
                        className={`transition-all w-2 h-2 rounded-full ${
                            curr === i ? "bg-gray-50 p-1" : "bg-gray-50/50"
                        }`}
                    />
                ))}
            </div>
        </div>
    );
}

export default Carousel;
