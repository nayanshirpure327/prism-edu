"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Building2, MapPin, Globe, Award } from "lucide-react";
import Link from "next/link";

export default function InstitutionDetailsPage() {
  const inst = {
    name: "Massachusetts Institute of Technology",
    country: "USA",
    city: "Cambridge",
    type: "University",
    ranking: 1,
    programs: 120,
    establishedYear: 1861,
    description: "MIT is a world-class research university known for its rigorous academic programs and cutting-edge research in science, engineering, and technology."
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-6 items-start">
        <div className="w-24 h-24 bg-muted rounded-xl flex items-center justify-center shrink-0">
          <Building2 className="w-12 h-12 text-muted-foreground" />
        </div>
        <div className="flex-1">
          <h1 className="text-3xl font-bold">{inst.name}</h1>
          <div className="flex flex-wrap items-center gap-4 mt-2 text-muted-foreground">
            <span className="flex items-center gap-1"><MapPin className="w-4 h-4"/> {inst.city}, {inst.country}</span>
            <span className="flex items-center gap-1"><Globe className="w-4 h-4"/> {inst.type}</span>
            <span className="flex items-center gap-1"><Award className="w-4 h-4"/> Ranked #{inst.ranking}</span>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Save</Button>
          <Button>Apply Now</Button>
        </div>
      </div>

      <Tabs defaultValue="about" className="w-full">
        <TabsList>
          <TabsTrigger value="about">About</TabsTrigger>
          <TabsTrigger value="programs">Programs</TabsTrigger>
          <TabsTrigger value="admissions">Admissions</TabsTrigger>
        </TabsList>
        
        <TabsContent value="about" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="leading-relaxed text-muted-foreground">{inst.description}</p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                <div className="p-4 border rounded-lg text-center">
                  <div className="text-2xl font-bold">{inst.establishedYear}</div>
                  <div className="text-sm text-muted-foreground">Established</div>
                </div>
                <div className="p-4 border rounded-lg text-center">
                  <div className="text-2xl font-bold">{inst.programs}</div>
                  <div className="text-sm text-muted-foreground">Programs</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="programs" className="mt-6">
          <Card>
            <CardContent className="p-0">
              <div className="divide-y">
                {[
                  { name: "BSc Computer Science", duration: "4 Years", tuition: "$55,000/yr" },
                  { name: "MSc Data Science", duration: "2 Years", tuition: "$60,000/yr" }
                ].map((prog, i) => (
                  <div key={i} className="p-4 flex justify-between items-center hover:bg-muted/50">
                    <div>
                      <h4 className="font-semibold">{prog.name}</h4>
                      <p className="text-sm text-muted-foreground">{prog.duration} • {prog.tuition}</p>
                    </div>
                    <Button variant="outline" size="sm">Details</Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="admissions" className="mt-6">
          <Card>
            <CardContent className="p-6 text-muted-foreground">
              Admission requirements content here.
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
