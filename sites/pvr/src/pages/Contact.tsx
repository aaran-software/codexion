import Contact2 from "../../../../resources/UIBlocks/contact/Contact2";
function Contact() {
  return (
    <div className="lg:px-[10%] mt-20 lg:mt-30">
      <Contact2
          addresses={`No: 3/306-A, Thandradevi Pattinam,
Paramakudi-623707
Ramnad District.`}
          email={[{ label: "demo@gmail.com", value: "demo@gmail.com" }]}
          phone={[{ label: "+91 98760 12345", value: "919876012345" }]}
          subTitle="Get In Touch With Us"
          description="Lorem ipsum dolor sit amet consectetur adipisicing elit. Eligendi error excepturi cum quod provident ipsam."
        />
    </div>
  );
}

export default Contact;
