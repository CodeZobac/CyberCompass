/* eslint-disable react/no-unescaped-entities */
'use client';

import { useState } from 'react';
import Head from 'next/head';
import { signIn } from 'next-auth/react';

const LoginSignupForm = () => {
  const [isActive, setIsActive] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleRegisterClick = () => {
    setIsActive(true);
  };

  const handleLoginClick = () => {
    setIsActive(false);
  };

  const handleSignIn = async () => {
      setIsLoading(true);
      try {
        await signIn('google', { callbackUrl: '/' });
      } catch (error) {
        console.error('Authentication error:', error);
      } finally {
        setIsLoading(false);
      }
    };

  return (
    <>
      <Head>
        <title>Login/Signup Form</title>
        <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet' />
      </Head>
      
      <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-[#e2e2e2] to-[#c9d6ff]">
        <div 
          className={`relative w-[850px] h-[550px] bg-white mx-5 rounded-[30px] shadow-md overflow-hidden ${isActive ? 'active' : ''}`}
        >
          {/* Login Form */}
          <div 
            className={`absolute right-0 w-1/2 h-full bg-white flex items-center text-gray-800 text-center p-10 z-10 transition-all duration-600 ease-in-out delay-[1200ms] ${
              isActive ? 'right-1/2' : ''
            }`}
          >
            <form className="w-full">
              <h1 className="text-4xl mb-4">Login</h1>
              <div className="relative my-[30px]">
                <input 
                  type="text" 
                  placeholder="Username" 
                  required
                  className="w-full py-[13px] pl-5 pr-[50px] bg-[#eee] rounded-lg border-none outline-none text-base text-gray-800 font-medium"
                />
                <i className='bx bxs-user absolute right-5 top-1/2 transform -translate-y-1/2 text-xl'></i>
              </div>
              <div className="relative my-[30px]">
                <input 
                  type="password" 
                  placeholder="Password" 
                  required
                  className="w-full py-[13px] pl-5 pr-[50px] bg-[#eee] rounded-lg border-none outline-none text-base text-gray-800 font-medium"
                />
                <i className='bx bxs-lock-alt absolute right-5 top-1/2 transform -translate-y-1/2 text-xl'></i>
              </div>
              <div className="-mt-[15px] mb-[15px]">
                <a href="#" className="text-sm text-gray-800">Forgot Password?</a>
              </div>
              <button 
                type="submit" 
                className="w-full h-12 bg-[#7494ec] rounded-lg shadow-sm border-none cursor-pointer text-base text-white font-semibold"
              >
                Login
              </button>
              <p className="text-sm my-[15px]">or login with social platforms</p>
              <div className="flex justify-center">
                <a onClick={handleSignIn} className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-google'></i>
                </a>
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-facebook'></i>
                </a>
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-github'></i>
                </a>
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-linkedin'></i>
                </a>
              </div>
            </form>
          </div>

          {/* Register Form */}
          <div 
            className={`absolute right-0 w-1/2 h-full bg-white flex items-center text-gray-800 text-center p-10 z-10 transition-all duration-600 ease-in-out delay-[1200ms] ${
              isActive ? 'visible' : 'invisible'
            }`}
          >
            <form className="w-full">
              <h1 className="text-4xl mb-4">Registration</h1>
              <div className="relative my-[30px]">
                <input 
                  type="text" 
                  placeholder="Username" 
                  required
                  className="w-full py-[13px] pl-5 pr-[50px] bg-[#eee] rounded-lg border-none outline-none text-base text-gray-800 font-medium"
                />
                <i className='bx bxs-user absolute right-5 top-1/2 transform -translate-y-1/2 text-xl'></i>
              </div>
              <div className="relative my-[30px]">
                <input 
                  type="email" 
                  placeholder="Email" 
                  required
                  className="w-full py-[13px] pl-5 pr-[50px] bg-[#eee] rounded-lg border-none outline-none text-base text-gray-800 font-medium"
                />
                <i className='bx bxs-envelope absolute right-5 top-1/2 transform -translate-y-1/2 text-xl'></i>
              </div>
              <div className="relative my-[30px]">
                <input 
                  type="password" 
                  placeholder="Password" 
                  required
                  className="w-full py-[13px] pl-5 pr-[50px] bg-[#eee] rounded-lg border-none outline-none text-base text-gray-800 font-medium"
                />
                <i className='bx bxs-lock-alt absolute right-5 top-1/2 transform -translate-y-1/2 text-xl'></i>
              </div>
              <button 
                type="submit" 
                className="w-full h-12 bg-[#7494ec] rounded-lg shadow-sm border-none cursor-pointer text-base text-white font-semibold"
              >
                Register
              </button>
              <p className="text-sm my-[15px]">or register with social platforms</p>
              <div className="flex justify-center">
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-google'></i>
                </a>
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-facebook'></i>
                </a>
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-github'></i>
                </a>
                <a href="#" className="inline-flex p-[10px] border-2 border-[#ccc] rounded-lg text-2xl text-gray-800 mx-2">
                  <i className='bx bxl-linkedin'></i>
                </a>
              </div>
            </form>
          </div>

          {/* Toggle Box */}
          <div className="absolute w-full h-full">
            <style jsx>{`
              .toggle-box::before {
                content: '';
                position: absolute;
                left: ${isActive ? '50%' : '-250%'};
                width: 300%;
                height: 100%;
                background: #7494ec;
                border-radius: 150px;
                z-index: 2;
                transition: 1.8s ease-in-out;
              }
              
              @media screen and (max-width: 650px) {
                .toggle-box::before {
                  left: 0;
                  top: ${isActive ? '70%' : '-270%'};
                  width: 100%;
                  height: 300%;
                  border-radius: 20vw;
                }
              }
            `}</style>
            <div className="toggle-box">
              {/* Left Toggle Panel */}
              <div 
                className={`absolute left-0 w-1/2 h-full text-white flex flex-col justify-center items-center z-20 transition-all duration-600 ease-in-out ${
                  isActive ? 'left-[-50%] delay-[600ms]' : 'delay-[1200ms]'
                }`}
              >
                <h1 className="text-4xl">Welcome Back!</h1>
                <p className="text-sm my-5 mb-5">Don't have an account?</p>
                <button 
                  onClick={handleRegisterClick}
                  className="w-40 h-[46px] bg-transparent border-2 border-white rounded-lg text-white font-semibold"
                >
                  Register
                </button>
              </div>
              
              {/* Right Toggle Panel */}
              <div 
                className={`absolute w-1/2 h-full text-white flex flex-col justify-center items-center z-20 transition-all duration-600 ease-in-out ${
                  isActive ? 'right-0 delay-[1200ms]' : 'right-[-50%] delay-[600ms]'
                }`}
              >
                <h1 className="text-4xl">Hello Welcome!</h1>
                <p className="text-sm my-5 mb-5">Already have an account?</p>
                <button 
                  onClick={handleLoginClick}
                  className="w-40 h-[46px] bg-transparent border-2 border-white rounded-lg text-white font-semibold"
                >
                  Login
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Media Queries */}
      <style jsx>{`
        @media screen and (max-width: 650px) {
          .active .form-box {
            right: 0;
            bottom: 30%;
          }
          
          .form-box {
            bottom: 0;
            width: 100%;
            height: 70%;
          }
          
          .toggle-panel {
            width: 100%;
            height: 30%;
          }
          
          .toggle-panel.toggle-left {
            top: 0;
          }
          
          .active .toggle-panel.toggle-left {
            left: 0;
            top: -30%;
          }
          
          .toggle-panel.toggle-right {
            right: 0;
            bottom: -30%;
          }
          
          .active .toggle-panel.toggle-right {
            bottom: 0;
          }
        }
        
        @media screen and (max-width: 400px) {
          .form-box {
            padding: 20px;
          }
          
          .toggle-panel h1 {
            font-size: 30px;
          }
        }
      `}</style>
    </>
  );
};

export default LoginSignupForm;
