"use client";

import { useState } from "react";
import { PageHeader } from "@/components/common/PageHeader";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search } from "lucide-react";
import { CareerCard } from "@/components/features/careers/CareerCard";
import { Career } from "@/lib/types";

// Mock data
const mockCareers: Career[] = [
  {
    id: "software-engineer",
    title: "Software Engineer",
    industry: "Technology",
    description: "Design and build software.",
    growthOutlook: "High",
    salaryRangeMin: 70000,
    salaryRangeMax: 150000,
    requiredSkills: ["Programming", "Problem Solving", "Teamwork"],
  },
  {
    id: "data-scientist",
    title: "Data Scientist",
    industry: "Technology",
    description: "Analyze data for insights.",
    growthOutlook: "High",
    salaryRangeMin: 80000,
    salaryRangeMax: 160000,
    requiredSkills: ["Statistics", "Python", "Machine Learning"],
  },
  {
    id: "marketing-manager",
    title: "Marketing Manager",
    industry: "Business",
    description: "Lead marketing campaigns.",
    growthOutlook: "Medium",
    salaryRangeMin: 60000,
    salaryRangeMax: 120000,
    requiredSkills: ["Communication", "SEO", "Strategy"],
  }
];

export default function CareersPage() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Career Explorer" 
        description="Discover and filter careers based on industry, growth, and salary."
      />

      <div className="flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Search careers..." 
            className="pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="w-full md:w-[200px]">
          <Select defaultValue="all">
            <SelectTrigger>
              <SelectValue placeholder="Industry" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Industries</SelectItem>
              <SelectItem value="tech">Technology</SelectItem>
              <SelectItem value="business">Business</SelectItem>
              <SelectItem value="healthcare">Healthcare</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockCareers.filter(c => c.title.toLowerCase().includes(searchTerm.toLowerCase())).map(career => (
          <CareerCard key={career.id} career={career} />
        ))}
      </div>
    </div>
  );
}
