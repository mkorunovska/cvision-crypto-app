import React from 'react';

const AccountBtns = () => {
  return <div className='flex items-center font-medium'>
    <a className='hover:text-blue/60 transition' href='#'>Login</a>
    <span className='mx-4 text-white/20'>|</span>
   <button className='btn h-[40px] px-5 text-base hover:bg-blue/60 hover:text-white'>Register</button>
    
  </div>
};

export default AccountBtns;
