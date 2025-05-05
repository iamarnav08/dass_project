"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Particles from '../components/HeroBg';
import GooeyNav from '../components/GooeyNav';
import { FaHome, FaInfoCircle, FaEnvelope } from 'react-icons/fa';

const items = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  { label: "Contact", href: "/contact" },
];

export default function LandingPage() {
  const router = useRouter();

  return (
    <div className="relative size-full h-screen overflow-hidden">
      {/* Particles in the background */}
      <div className="absolute inset-0 z-0">
        <Particles
          particleColors={['#ffffff', '#ffffff']}
          particleCount={200}
          particleSpread={7}
          speed={0.1}
          particleBaseSize={100}
          moveParticlesOnHover={true}
          alphaParticles={false}
          disableRotation={false}
        />
      </div>
      
      {/* Content layer */}
      <div className="pointer-events-none relative z-10 flex size-full flex-col items-center justify-center">
        <h1 className="pointer-events-auto text-4xl font-bold text-white">Welcome to <br/> OliveOrange</h1>
        <p className="pointer-events-auto text-lg text-white">Use the power of LLMs to study</p>
        <div className="group pointer-events-auto mt-6">
          <button
            onClick={() => router.push('/login')}
            className="relative inline-block cursor-pointer rounded-xl bg-gray-800 p-px font-semibold leading-6 text-white shadow-2xl shadow-zinc-900 transition-transform duration-300 ease-in-out hover:scale-105 active:scale-95"
          >
            <span
              className="absolute inset-0 rounded-xl bg-gradient-to-r from-teal-400 via-blue-500 to-purple-500 p-[2px] opacity-0 transition-opacity duration-500 group-hover:opacity-100"
            ></span>
            <span className="relative z-10 block rounded-xl bg-gray-950 px-6 py-3">
              <div className="relative z-10 flex items-center space-x-2">
                <span className="transition-all duration-500 group-hover:translate-x-1">Let&apos;s get started</span>
                <svg
                  className="size-6 transition-transform duration-500 group-hover:translate-x-1"
                  data-slot="icon"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    clipRule="evenodd"
                    d="M8.22 5.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L11.94 10 8.22 6.28a.75.75 0 0 1 0-1.06Z"
                    fillRule="evenodd"
                  ></path>
                </svg>
              </div>
            </span>
          </button>
        </div>
      </div>
      
      {/* Navigation - adjust container to eliminate shadow effect */}
      <div className="absolute inset-x-0 top-4 z-20 flex justify-center">
        <div className="bg-transparent">
          <GooeyNav items={items} initialActiveIndex={0} />
        </div>
      </div>
    </div>
  );
}