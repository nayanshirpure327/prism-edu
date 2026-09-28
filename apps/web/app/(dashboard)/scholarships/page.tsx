"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatCurrency } from "@/lib/utils";
import { Calendar, Globe, Zap } from "lucide-react";

export default function ScholarshipsPage() {
  const scholarships = [
    {
      id: "1",
      name: "Global Tech Innovators Scholarship",
      provider: "Tech Foundation",
      amount: 25000,
      deadline: "2026-10-15",
      coverageType: "Full Tuition",
      eligibility: "Computer Science majors, GPA > 3.5",
      status: "eligible"
    },
    {
      id: "2",
      name: "Women in STEM Grant",
      provider: "STEM Alliance",
      amount: 10000,
      deadline: "2026-11-01",
      coverageType: "Partial",
      eligibility: "Female students in STEM fields",
      status: "check-eligibility"
    }
  ];

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Scholarship Finder" 
        description="Discover funding opportunities matched to your profile."
        action={<Button><Zap className="w-4 h-4 mr-2"/> Match with Profile</Button>}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {scholarships.map((s) => (
          <Card key={s.id} className="flex flex-col">
            <CardHeader>
              <div className="flex justify-between items-start mb-2">
                <Badge variant={s.status === 'eligible' ? 'success' : 'secondary'}>
                  {s.status === 'eligible' ? 'Eligible' : 'Check Eligibility'}
                </Badge>
                <div className="text-sm font-medium flex items-center text-orange-600 bg-orange-50 px-2 py-1 rounded">
                  <Calendar className="w-3 h-3 mr-1" />
                  Oct 15
                </div>
              </div>
              <CardTitle className="text-xl line-clamp-2">{s.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{s.provider}</p>
            </CardHeader>
            <CardContent className="flex-1">
              <div className="text-2xl font-bold text-primary mb-4">
                {formatCurrency(s.amount)}
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex items-start gap-2">
                  <span className="text-muted-foreground min-w-[70px]">Coverage:</span>
                  <span className="font-medium">{s.coverageType}</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-muted-foreground min-w-[70px]">Eligibility:</span>
                  <span className="font-medium line-clamp-2">{s.eligibility}</span>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full">View Details</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
