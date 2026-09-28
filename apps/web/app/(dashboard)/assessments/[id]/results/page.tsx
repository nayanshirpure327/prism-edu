"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";
import Link from "next/link";
import { useParams } from "next/navigation";

const data = [
  { subject: 'Logical', A: 85, fullMark: 100 },
  { subject: 'Verbal', A: 70, fullMark: 100 },
  { subject: 'Numerical', A: 92, fullMark: 100 },
  { subject: 'Spatial', A: 65, fullMark: 100 },
  { subject: 'Analytical', A: 88, fullMark: 100 },
];

export default function AssessmentResultsPage() {
  const params = useParams();

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Assessment Results" 
        description="Your detailed aptitude profile and career recommendations."
        action={
          <Link href="/careers">
            <Button>Explore Recommended Careers</Button>
          </Link>
        }
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Aptitude Radar</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name="Score" dataKey="A" stroke="#7c3aed" fill="#7c3aed" fillOpacity={0.5} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Top Aptitudes</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="p-3 bg-green-50 text-green-700 rounded border border-green-200">
                <div className="font-bold">Numerical (92%)</div>
                <div className="text-sm mt-1">Excellent at math and data.</div>
              </div>
              <div className="p-3 bg-blue-50 text-blue-700 rounded border border-blue-200">
                <div className="font-bold">Analytical (88%)</div>
                <div className="text-sm mt-1">Strong problem-solving skills.</div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Recommended Streams</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5 space-y-2 text-muted-foreground">
                <li>Computer Science & Engineering</li>
                <li>Data Science</li>
                <li>Finance & Accounting</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
