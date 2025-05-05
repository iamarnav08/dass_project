'use client';

import Link from "next/link";
import { Navbar, DarkThemeToggle } from "flowbite-react";
import { usePathname } from "next/navigation";

export default function AuthNavbar() {
  const pathname = usePathname();
  
  // Check if this is a loading/processing page
  const isProcessingAuth = pathname?.startsWith('/auth/google/callback');
  
  return (
    <Navbar fluid>
      <Navbar.Brand as={Link} href="/">
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">OliveOrange</span>
      </Navbar.Brand>
      
      {isProcessingAuth && (
        <div className="ml-auto text-sm text-gray-500">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-500 mr-2"></div>
            Processing login
          </div>
        </div>
      )}
      
      <div className="ml-auto">
        <DarkThemeToggle />
      </div>
    </Navbar>
  );
}