"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check, X } from "lucide-react";

export default function CompareInstitutionsPage() {
  const institutions = [
    { name: "MIT", country: "USA", ranking: 1, tuition: "$55,000", acc: true },
    { name: "Stanford", country: "USA", ranking: 2, tuition: "$56,000", acc: true },
  ];

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Compare Institutions" 
        description="Side-by-side comparison of your selected institutions."
      />

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[600px]">
          <thead>
            <tr>
              <th className="p-4 border-b bg-muted/50 w-1/4">Features</th>
              {institutions.map((inst, i) => (
                <th key={i} className="p-4 border-b w-[37.5%]">
                  <h3 className="text-xl font-bold">{inst.name}</h3>
                  <p className="text-sm text-muted-foreground">{inst.country}</p>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="p-4 border-b font-medium text-muted-foreground">Global Ranking</td>
              {institutions.map((inst, i) => (
                <td key={i} className="p-4 border-b font-semibold">#{inst.ranking}</td>
              ))}
            </tr>
            <tr>
              <td className="p-4 border-b font-medium text-muted-foreground">Tuition / Year</td>
              {institutions.map((inst, i) => (
                <td key={i} className="p-4 border-b font-semibold">{inst.tuition}</td>
              ))}
            </tr>
            <tr>
              <td className="p-4 border-b font-medium text-muted-foreground">Accredited</td>
              {institutions.map((inst, i) => (
                <td key={i} className="p-4 border-b">
                  {inst.acc ? <Check className="text-green-500 w-5 h-5"/> : <X className="text-red-500 w-5 h-5"/>}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
