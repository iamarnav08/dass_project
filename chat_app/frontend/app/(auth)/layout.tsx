'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import Particles from '@/components/HeroBg';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  const pathname = usePathname();

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

      {/* Auth Navbar */}
      <nav className="absolute inset-x-0 top-0 z-20 flex h-16 items-center justify-between bg-transparent px-6">
        <Link href="/" className="text-xl font-bold text-white hover:text-gray-200">
          OliveOrange
        </Link>
        <div className="flex items-center gap-4">
          <Link 
            href="/login" 
            className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              pathname === '/login' 
                ? 'bg-white text-gray-900' 
                : 'text-white hover:bg-white/10'
            }`}
          >
            Login
          </Link>
          <Link 
            href="/register" 
            className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
              pathname === '/register' 
                ? 'bg-white text-gray-900' 
                : 'text-white hover:bg-white/10'
            }`}
          >
            Register
          </Link>
        </div>
      </nav>

      {/* Auth content */}
      <div className="pointer-events-none relative z-10 flex min-h-screen items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="pointer-events-auto w-full max-w-md space-y-8 rounded-xl bg-gray-800/30 p-8 shadow-2xl backdrop-blur-sm">
          {children}
        </div>
      </div>
    </div>
  );
} 