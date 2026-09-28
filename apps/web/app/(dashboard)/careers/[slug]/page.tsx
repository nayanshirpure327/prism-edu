"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { Bookmark, Map } from "lucide-react";
import { useParams } from "next/navigation";
import Link from "next/link";

export default function CareerDetailsPage() {
  const params = useParams();
  
  // Mock career
  const career = {
    title: "Software Engineer",
    industry: "Technology",
    growthOutlook: "High",
    salaryRangeMin: 70000,
    salaryRangeMax: 150000,
    description: "Software Engineers design, develop, and test software and applications for computers. The main duties and responsibilities of software engineers include directing and participating in programming activities, monitoring, and evaluating system performance.",
    requiredSkills: ["JavaScript", "Python", "Data Structures", "System Design", "Communication"],
    subjects: ["Mathematics", "Computer Science", "Physics"],
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start gap-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="outline">{career.industry}</Badge>
            <Badge variant="success">{career.growthOutlook} Growth</Badge>
          </div>
          <h1 className="text-3xl font-bold">{career.title}</h1>
          <p className="text-xl text-primary font-semibold mt-2">
            {formatCurrency(career.salaryRangeMin)} - {formatCurrency(career.salaryRangeMax)} / yr
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline"><Bookmark className="w-4 h-4 mr-2" /> Save</Button>
          <Link href="/pathways">
            <Button><Map className="w-4 h-4 mr-2" /> Generate Pathway</Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>About this Career</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground leading-relaxed">
                {career.description}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Required Education Path</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-300 before:to-transparent">
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-slate-300 group-[.is-active]:bg-primary text-slate-500 group-[.is-active]:text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                    1
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded border shadow-sm bg-card">
                    <h4 className="font-bold text-foreground">High School</h4>
                    <p className="text-sm text-muted-foreground mt-1">Focus on Sciences and Mathematics.</p>
                  </div>
                </div>
                
                <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-slate-300 group-[.is-active]:bg-primary text-slate-500 group-[.is-active]:text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                    2
                  </div>
                  <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded border shadow-sm bg-card">
                    <h4 className="font-bold text-foreground">Bachelor's Degree</h4>
                    <p className="text-sm text-muted-foreground mt-1">BSc in Computer Science or related field.</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Key Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {career.requiredSkills.map((skill, i) => (
                  <Badge key={i} variant="secondary">{skill}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Recommended Subjects</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5 space-y-2 text-muted-foreground">
                {career.subjects.map((sub, i) => <li key={i}>{sub}</li>)}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
