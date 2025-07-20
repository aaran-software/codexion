import { useState } from 'react';
import sample1 from '../../assets/sample1.jpg';

type TeamMember = {
  image: string;
  name: string;
  designation: string;
  bio: string;
};

function Team() {
  const [team] = useState<TeamMember[]>([
    {
      image: sample1,
      name: 'Desirae Dias',
      designation: 'CEO',
      bio: 'developer',
    },
    {
      image: sample1,
      name: 'Madelyn Torff',
      designation: 'Marketing Head',
      bio: 'developer',
    },
    {
      image: sample1,
      name: 'Tiana Gouse',
      designation: 'Project Manager',
      bio: 'developer',
    },
    {
      image: sample1,
      name: 'Livia Passaquin',
      designation: 'Director',
      bio: 'developer',
    },
  ]);

  return (
    <section className='py-20 lg:px-[12%] px-5 flex flex-col gap-8 bg-website-background text-website-foreground'>
      <div className='text-center font-semibold text-4xl'>Meet Our Teams</div>
      <div className='text-center mt- md:w-[70%] block mx-auto'>
        Plan & Pricing Lorem ipsum dolor sit amet consectetur adipisicing elit.
        Laborum omnis veniam nihil assumenda quas pariatur commodi accusantium alias inventore.
      </div>

      <div className='grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-2 lg:grid-cols-4 sm:px-5 mt-10'>
        {team.map((member, index) => (
          <div
            key={index}
            className='flex flex-col gap-3 mt-8 sm:mt-0 items-center justify-center'
          >
            <img src={member.image} alt='' />
            <div className='text-2xl font-semibold'>{member.name}</div>
            <div className='text-md'>{member.designation}</div>
            <div className='text-sm line-clamp-1'>{member.bio}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Team;
