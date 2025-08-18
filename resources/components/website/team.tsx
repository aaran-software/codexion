type TeamMember = {
  image: string;
  name: string;
  designation: string;
  bio: string;
};

type TeamProps = {
  title?: string;
  description?: string;
  members: TeamMember[];
};

function Team({ title = "Meet Our Team", description, members }: TeamProps) {
  return (
    <section className="py-20 lg:px-[12%] px-5 flex flex-col gap-8 bg-background text-website-foreground">
      {/* Title */}
      <div className="text-center font-semibold text-4xl">{title}</div>

      {/* Description */}
      {description && (
        <div className="text-center md:w-[70%] block mx-auto">
          {description}
        </div>
      )}

      {/* Members Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-2 lg:grid-cols-4 sm:px-5 mt-10">
        {members.map((member, index) => (
          <div
            key={index}
            className="flex flex-col gap-3 mt-8 sm:mt-0 items-center justify-center"
          >
            <img
              src={member.image}
              alt={member.name}
              className="w-32 h-32 object-cover rounded-full shadow-md"
            />
            <div className="text-2xl font-semibold">{member.name}</div>
            <div className="text-md">{member.designation}</div>
            <div className="text-sm text-center px-2">{member.bio}</div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Team;
