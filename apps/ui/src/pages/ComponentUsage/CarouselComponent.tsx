import { useState } from 'react';
import Carousel from '../../../../../resources/components/Carousel';

type ReviewType = {
  review: string;
  name: string;
  designation: string;
  image: string;
};

function CarouselComponent() {
  const [review] = useState<ReviewType[]>([
    {
      review:
        'Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Cras ultricies ligula sed magna dictum porta. Proin eget tortor risus.',
      name: 'Amelia Abelo',
      designation: 'Manager',
      image: '/assets',
    },
    {
      review:
        'Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Cras ultricies ligula sed magna dictum porta. Proin eget tortor risus.',
      name: 'Noah Johnson',
      designation: 'CEO',
      image: 'sample1',
    },
    {
      review:
        'Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Cras ultricies ligula sed magna dictum porta. Proin eget tortor risus.',
      name: 'Amelia Abelo',
      designation: 'Manager',
      image: 'sample1',
    },
  ]);

  return (
    <section className='lg:px-[12%] my-20 gap-10 px-5'>
      <div id='review' className='flex justify-center items-center gap-10 px-5 py-10 overflow-x-auto'>
      <div className='w-full max-w-3xl'>
        <Carousel autoSlide={false} autoSlideInterval={7000}>
          {review.map((item, index) => (
            <div
              key={index}
              className={`flex-grow-0  border border-ring/30 flex-shrink-0 w-full py-10 px-15 rounded-md ${
                index % 2 === 0 ? 'bg-card-background' : 'bg-[#17965f] text-card-background'
              }`}
            >
              <div>{item.review}</div>
              <div className='flex flex-row gap-3 mt-5'>
                <img className='w-15 h-15 rounded-full' src={item.image} alt='' />
                <div className='flex flex-col justify-center'>
                  <div className='text-2xl font-semibold capitalize'>{item.name}</div>
                  <div className='capitalize'>{item.designation}</div>
                </div>
              </div>
            </div>
          ))}
        </Carousel>
      </div>
    </div>

    </section>
  );
}

export default CarouselComponent;
 