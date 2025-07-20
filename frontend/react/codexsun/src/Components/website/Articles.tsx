// Articles.tsx
import { useState } from 'react';
import sample1 from '../../assets/sample1.jpg';
import Button from '../Input/Button';

type Article = {
  image: string;
  title: string;
  description: string;
  path: string;
};

function Articles() {
  const [articles] = useState<Article[]>([
    {
      image: sample1,
      title: 'The Best Place to Invest Your Money',
      description: 'Torem orem ipsum dolor sit amet, Tetur adipiscing elit. Atempor scelerisque olor sit mauris',
      path: '/blog',
    },
    {
      image: sample1,
      title: 'The Best Place to Invest Your Money',
      description: 'Torem orem ipsum dolor sit amet, Tetur adipiscing elit. Atempor scelerisque olor sit mauris',
      path: '/blog',
    },
    {
      image: sample1,
      title: 'The Best Place to Invest Your Money',
      description: 'Torem orem ipsum dolor sit amet, Tetur adipiscing elit. Atempor scelerisque olor sit mauris',
      path: '/blog',
    },
    {
      image: sample1,
      title: 'The Best Place to Invest Your Money',
      description: 'Torem orem ipsum dolor sit amet, Tetur adipiscing elit. Atempor scelerisque olor sit mauris',
      path: '/blog',
    },
  ]);

  return (
    <section className='py-20 lg:px-[12%] px-5 flex flex-col gap-8 bg-website-background text-website-foreground'>
      <div className='text-center font-bold text-4xl'>Latest Posts & Articles</div>
      <div className='text-center mt-8 md:w-[70%] block mx-auto'>
        Mirem ipsum dolor sit amet, consectetur adipiscing elit. Sapien, sit sed accumsan, viverra sociis ullamcorper aenean fermentum.
      </div>

      <div className='grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-3 lg:grid-cols-4 px-5 mt-5'>
        {articles.map((article, index) => (
          <div key={index} className='flex flex-col gap-3 p-3 mt-8 sm:mt-0'>
            <img src={article.image} alt='' />
            <div className='text-2xl lg:text-xl font-bold line-clamp-1 lg:line-clamp-2'>{article.title}</div>
            <div className='text-lg line-clamp-2 lg:line-clamp-3'>{article.description}</div>
            <Button label='Read More' path={article.path} className='bg-gray-200 w-max text-black px-4' children={undefined} />
          </div>
        ))}
      </div>
    </section>
  );
}

export default Articles;
