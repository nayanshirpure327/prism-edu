"use client";

import { useAuth } from "@/lib/auth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Map, Briefcase, CheckCircle, Clock } from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const { user } = useAuth();
  
  // Mock data for display
  const profileCompletion = 65;
  const stats = [
    { label: "Profile Completion", value: "65%", icon: CheckCircle },
    { label: "Assessments Done", value: "1/2", icon: Clock },
    { label: "Pathways Generated", value: "3", icon: Map },
    { label: "Saved Careers", value: "5", icon: Briefcase },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Welcome back, {user?.firstName}!</h1>
          <p className="text-muted-foreground">Here is an overview of your career journey.</p>
        </div>
        <Link href="/pathways">
          <Button>Generate New Pathway</Button>
        </Link>
      </div>

      {profileCompletion < 100 && (
        <Card className="border-primary/20 bg-primary/5">
          <CardContent className="p-6 flex flex-col md:flex-row items-center gap-6">
            <div className="flex-1 space-y-2">
              <h3 className="text-lg font-semibold">Complete your profile</h3>
              <p className="text-sm text-muted-foreground">
                You need to complete your academic and financial preferences to get accurate pathway recommendations.
              </p>
              <Progress value={profileCompletion} className="h-2 mt-4" />
            </div>
            <Link href="/profile/wizard">
              <Button variant="default">Continue Setup</Button>
            </Link>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <Card key={i}>
              <CardContent className="p-6 flex items-center gap-4">
                <div className="p-3 bg-primary/10 text-primary rounded-lg">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Recent Pathways</CardTitle>
            <CardDescription>Your recently generated career pathways.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { name: "Software Engineer", comp: 92, steps: 4 },
                { name: "Data Scientist", comp: 85, steps: 5 },
              ].map((pathway, i) => (
                <div key={i} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                  <div>
                    <h4 className="font-medium">{pathway.name}</h4>
                    <p className="text-sm text-muted-foreground">{pathway.steps} steps required</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-sm font-bold text-green-600">{pathway.comp}% Match</div>
                    </div>
                    <Link href={`/pathways/${i}`}>
                      <Button variant="outline" size="sm">View</Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Upcoming Deadlines</CardTitle>
            <CardDescription>Don't miss these dates.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-3 border rounded-lg bg-orange-50 dark:bg-orange-950/20 border-orange-200">
                <div className="text-xs font-bold text-orange-600 mb-1">IN 5 DAYS</div>
                <h4 className="text-sm font-medium">Global Tech Scholarship</h4>
                <p className="text-xs text-muted-foreground mt-1">Application closes Oct 15</p>
              </div>
              <div className="p-3 border rounded-lg">
                <div className="text-xs font-bold text-primary mb-1">IN 2 WEEKS</div>
                <h4 className="text-sm font-medium">MIT Fall Admission</h4>
                <p className="text-xs text-muted-foreground mt-1">Application closes Oct 30</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
