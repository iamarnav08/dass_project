'use client';

import { useEffect, useState } from "react";
import Link from "next/link";
import { Navbar, DarkThemeToggle, Button } from "flowbite-react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";

interface MainNavbarProps {
  activeLink: string;
}

export default function MainNavbar({ activeLink }: MainNavbarProps) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated());
  }, []);
  
  const handleSignOut = async () => {
    try {
      await authService.logout();
      setIsAuthenticated(false);
      router.push('/login');
    } catch (error) {
      console.error('Failed to logout:', error);
    }
  };

  return (
    <Navbar fluid>
      <Navbar.Brand as={Link} href="/">
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Back</span>
      </Navbar.Brand>
      <div className="flex md:order-2">
        <DarkThemeToggle />
        {isAuthenticated ? (
          <Button onClick={handleSignOut} color="red">
            Logout
          </Button>
        ) : (
          <div className="flex gap-2">
            <Button as={Link} href="/login" color="gray">
              Login
            </Button>
            <Button as={Link} href="/register" color="blue">
              Register
            </Button>
          </div>
        )}
        <Navbar.Toggle />
      </div>
      <Navbar.Collapse>
        {isAuthenticated ? (
          <>
            <Navbar.Link href="/chat" active={activeLink === "chat"}>
              Chat
            </Navbar.Link>
            <Navbar.Link href="/" active={activeLink === "dashboard"}>
              Dashboard
            </Navbar.Link>
            <Navbar.Link href="/sell" active={activeLink === "sell"}>
              Sell
            </Navbar.Link>
            <Navbar.Link href="/market" active={activeLink === "market"}>
              Market
            </Navbar.Link>
            <Navbar.Link href="/orders" active={activeLink === "orders"}>
              Orders
            </Navbar.Link>
            <Navbar.Link href="/deliver" active={activeLink === "deliver"}>
              Deliver
            </Navbar.Link>
            <Navbar.Link href="/cart" active={activeLink === "cart"}>
              Cart
            </Navbar.Link>
            <Navbar.Link href="/support" active={activeLink === "support"}>
              Support
            </Navbar.Link>
          </>
        ) : null}
      </Navbar.Collapse>
    </Navbar>
  );
}