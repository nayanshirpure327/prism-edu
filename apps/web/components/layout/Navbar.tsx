"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, User as UserIcon, Settings, LogOut } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"; // Assume we have this or fallback
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { getInitials } from "@/lib/utils";

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const links = [
    { name: "Dashboard", href: "/dashboard" },
    { name: "Careers", href: "/careers" },
    { name: "My Pathways", href: "/pathways" },
    { name: "Institutions", href: "/institutions" },
    { name: "Scholarships", href: "/scholarships" },
    { name: "Funding & Loans", href: "/loans" },
    { name: "What-If Simulator", href: "/scenarios" },
    { name: "Decision Matrix", href: "/decision-matrix" },
  ];

  return (
    <nav className="border-b bg-background sticky top-0 z-40 w-full h-16 flex items-center">
      <div className="container mx-auto px-4 h-full flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <img src="/prism-logo.svg" alt="PRISM-EDU logo" className="h-14 w-auto" />
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center space-x-6">
          {user ? (
            <div className="flex items-center gap-4">
               {/* Dropping standard links from top nav to favor sidebar for dashboard, 
                   but we can keep a few or just the avatar */}
               <div className="flex items-center space-x-4">
                <Avatar className="h-8 w-8 cursor-pointer">
                  <AvatarFallback>{getInitials(user.firstName + " " + user.lastName)}</AvatarFallback>
                </Avatar>
                <Button variant="ghost" size="sm" onClick={logout}>
                  <LogOut className="w-4 h-4 mr-2" />
                  Logout
                </Button>
               </div>
            </div>
          ) : (
            <div className="space-x-4">
              <Link href="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link href="/register">
                <Button>Get Started</Button>
              </Link>
            </div>
          )}
        </div>

        {/* Mobile toggle */}
        <button
          className="md:hidden p-2"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="absolute top-16 left-0 w-full bg-background border-b shadow-lg md:hidden flex flex-col p-4 space-y-4">
          {user ? (
            <>
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`text-sm font-medium ${
                    pathname === link.href ? "text-primary" : "text-muted-foreground"
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  {link.name}
                </Link>
              ))}
              <Button variant="outline" className="w-full justify-start" onClick={() => { logout(); setIsOpen(false); }}>
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link href="/login" onClick={() => setIsOpen(false)}>
                <Button variant="ghost" className="w-full justify-start">Login</Button>
              </Link>
              <Link href="/register" onClick={() => setIsOpen(false)}>
                <Button className="w-full justify-start">Get Started</Button>
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
