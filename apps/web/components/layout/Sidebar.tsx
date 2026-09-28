"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  Briefcase, 
  Map, 
  Building2, 
  GraduationCap, 
  Landmark,
  LineChart,
  GitCompare,
  Settings,
  FileText
} from "lucide-react";

const sidebarLinks = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Profile", href: "/profile", icon: Settings },
  { name: "Careers", href: "/careers", icon: Briefcase },
  { name: "My Pathways", href: "/pathways", icon: Map },
  { name: "Institutions", href: "/institutions", icon: Building2 },
  { name: "Scholarships", href: "/scholarships", icon: GraduationCap },
  { name: "Funding & Loans", href: "/loans", icon: Landmark },
  { name: "What-If Simulator", href: "/scenarios", icon: LineChart },
  { name: "Decision Matrix", href: "/decision-matrix", icon: GitCompare },
  { name: "Reports", href: "/reports", icon: FileText },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 border-r h-[calc(100vh-4rem)] bg-card overflow-y-auto hidden md:block shrink-0">
      <div className="flex flex-col py-4 gap-1 px-2">
        {sidebarLinks.map((link) => {
          const isActive = pathname.startsWith(link.href);
          const Icon = link.icon;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive 
                  ? "bg-primary/10 text-primary" 
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <Icon className="w-4 h-4" />
              {link.name}
            </Link>
          );
        })}
      </div>
    </div>
  );
}
