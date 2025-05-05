"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import GooeyNav from '@/components/GooeyNav';
import Particles from '@/components/HeroBg';

const items = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  { label: "Contact", href: "/contact" }
];

const spotlightItems = [
  {
    title: "Your journey to Knowledge is now AI assured",
    description: "Explore Features our AI assistant",
  },
  {
    title: "Your Questions, Answered",
    description: "Imagine you’re revising for your science exam, and you’re stuck on the concept of atomic structure. Simply type your question, and our AI-powered app will refer to your textbook to provide a detailed explanation. Not just text—we’ll show diagrams, examples, and related topics to make learning easier.",
  },
  {
    title: "Understands Your Syllabus",
    description: "Solves your problem",
  },
  {
    title: "Concise answers",
    description: "Answers precisely the questions drawn from NCERT class X social studies",
  },
  {
    title: "Decodes poem",
    description: "Our shakes sphere can digest poem drawn from NCERT class X English",
  },
  {
    title: "Struggling? Let the Bot Assist You",
    description: "Sometimes an answer isn’t enough. If you’re still unsure, the app identifies the topic and explains it step by step. Alternatively, it imposes adaptive questions to assess your understanding",
  },
  {
    title: "Step By Step",
    description: "Begins explaining the concept from the basics, breaking it into digestible parts.",
  },
  {
    title: "Offers simplified examples",
    description: "with direct references to concepts",
  },
  {
    title: "Switch to adaptive mode",
    description: "The bot asks progressively easier or more challenging questions.",
  },
  {
    title: "Gamified Learning Experience with Adaptive Testing",
    description: "Now that you have explored the topic, its time to put your knowledge to the test. Our app conducts adaptive tests tailored to your curriculum, adjusting questions difficulty as you progress.",
  },
];

export default function AboutPage() {
  const router = useRouter();
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      setMousePosition({ x: event.clientX, y: event.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className="relative h-screen w-full overflow-auto text-white">
      
      {/* Content layer */}
      <div className="relative mt-16 flex flex-wrap items-center justify-center gap-4 p-4 md:p-8">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {spotlightItems.map((item, index) => (
            <motion.div
              key={index}
              className="rounded-lg bg-gray-800 p-4 shadow-lg"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              style={{
                transform: `translate(${mousePosition.x * 0.05}px, ${mousePosition.y * 0.05}px)`,
              }}
            >
              <h3 className="text-lg font-bold md:text-xl">{item.title}</h3>
              <p className="text-sm md:text-base">{item.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

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
      
      {/* Navigation - adjust container to eliminate shadow effect */}
      <div className="absolute inset-x-0 top-4 z-20 flex justify-center">
        <div className="bg-transparent">
          <GooeyNav items={items} initialActiveIndex={1} />
        </div>
      </div>
    </div>
  );
}