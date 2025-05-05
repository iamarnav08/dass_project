"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Particles from '../../components/HeroBg';
import GooeyNav from '../../components/GooeyNav';
import { Button, Card, Label, TextInput } from "flowbite-react";

const items = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  { label: "Contact", href: "/contact" }
];

export default function ContactPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [emailValid, setEmailValid] = useState<boolean | null>(null);

  const validateEmail = (email: string) => {
    const re = /\S+@\S+\.\S+/;
    return re.test(email);
  }

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    setEmailValid(validateEmail(value));
  };

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
  };

  const handleMessageChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    console.log({ name, email, message });
  };

  return (
    <div className="relative h-screen w-full overflow-hidden">
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
        <div className="pointer-events-auto w-full max-w-md px-4">
          <Card className="bg-white/90 dark:bg-gray-800/90 shadow-lg backdrop-blur-sm p-8">
            <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white text-center">
              Contact Us
            </h1>
            <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
              <div>
                <div className="mb-2 block">
                  <Label htmlFor="name" value="Your name" />
                </div>
                <TextInput 
                  id="name" 
                  type="text" 
                  placeholder="John Doe" 
                  required 
                  value={name}
                  onChange={handleNameChange}
                />
              </div>
              <div>
                <div className="mb-2 block">
                  <Label htmlFor="email" value="Your email" />
                </div>
                <TextInput 
                  id="email" 
                  type="email" 
                  placeholder="name@example.com" 
                  required 
                  value={email}
                  onChange={handleEmailChange}
                  color={emailValid === false ? "failure" : emailValid === true ? "success" : undefined}
                  helperText={emailValid === false ? "Please enter a valid email address" : ""}
                />
              </div>
              <div>
                <div className="mb-2 block">
                  <Label htmlFor="message" value="Message" />
                </div>
                <textarea
                  id="message"
                  className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                  rows={6}
                  placeholder="Your message..."
                  value={message}
                  onChange={handleMessageChange}
                  required 
                />
              </div>
              <button type="submit" className="btn btn-blue">Submit</button>
            </form>
          </Card>
        </div>
      </div>
      
      {/* Navigation - adjust container to eliminate shadow effect */}
      <div className="absolute inset-x-0 top-4 z-20 flex justify-center">
        <div className="bg-transparent">
          <GooeyNav items={items} initialActiveIndex={2} />
        </div>
      </div>
    </div>
  );
}