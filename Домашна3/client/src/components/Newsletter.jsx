import React from "react";

import NewsletterForm from "./NewsletterForm.jsx";

const Newsletter = () => {
  return (
    <section 
    className="py-[40px] lg:py-[88px] bg-blue-50 bg-cover mt-20">
      <div className="container mx-auto">
        <div className="flex flex-col lg:flex-row items-center justify-between bg-darkblue p-12
        rounded-2xl lg:bg-darkblue lg:bg-no-repeat lg:h-[216px]"
        data-aos='fade-down' 
        data-aos-delay='100' 
        >
          <div className="flex-1 w-full">
            <h3 className="h3 mb-4">Start now</h3>
            <p className="max-w-[348px] mb-8">Join now with CVision to get the latest news</p>
          </div>
          <NewsletterForm />
        </div>
      </div>
    </section>
  );
};

export default Newsletter;
