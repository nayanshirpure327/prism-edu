"use client";

import { useState } from "react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Search, MapPin, Building2, CheckSquare, Square } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

const mockInstitutions = [
  { id: "1", slug: "mit", name: "Massachusetts Institute of Technology", country: "USA", city: "Cambridge", type: "University", ranking: 1, programs: 120, tuitionRange: "$55k - $60k" },
  { id: "2", slug: "stanford", name: "Stanford University", country: "USA", city: "Stanford", type: "University", ranking: 2, programs: 95, tuitionRange: "$56k - $62k" },
  { id: "3", slug: "oxford", name: "University of Oxford", country: "UK", city: "Oxford", type: "University", ranking: 3, programs: 150, tuitionRange: "£30k - £40k" }
];

export default function InstitutionsPage() {
  const [selected, setSelected] = useState<string[]>([]);
  const router = useRouter();

  const toggleSelect = (id: string) => {
    setSelected(prev => 
      prev.includes(id) 
        ? prev.filter(x => x !== id) 
        : prev.length < 3 ? [...prev, id] : prev
    );
  };

  return (
    <div className="space-y-6 relative pb-20">
      <PageHeader 
        title="Institutions" 
        description="Search and compare universities and colleges worldwide."
      />

      <div className="flex gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search institutions..." className="pl-9" />
        </div>
        <Button variant="outline">Filters</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockInstitutions.map((inst) => {
          const isSelected = selected.includes(inst.id);
          return (
            <Card key={inst.id} className={`transition-all ${isSelected ? 'ring-2 ring-primary' : ''}`}>
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="w-12 h-12 bg-muted rounded flex items-center justify-center">
                    <Building2 className="w-6 h-6 text-muted-foreground" />
                  </div>
                  <button onClick={() => toggleSelect(inst.id)} className="text-muted-foreground hover:text-primary">
                    {isSelected ? <CheckSquare className="w-6 h-6 text-primary" /> : <Square className="w-6 h-6" />}
                  </button>
                </div>
                <h3 className="text-lg font-bold line-clamp-1 mb-1">{inst.name}</h3>
                <div className="flex items-center gap-1 text-sm text-muted-foreground mb-4">
                  <MapPin className="w-4 h-4" /> {inst.city}, {inst.country}
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Global Ranking</span>
                    <span className="font-semibold">#{inst.ranking}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Tuition Range</span>
                    <span className="font-semibold">{inst.tuitionRange}</span>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="p-6 pt-0">
                <Link href={`/institutions/${inst.slug}`} className="w-full">
                  <Button variant="secondary" className="w-full">View Details</Button>
                </Link>
              </CardFooter>
            </Card>
          );
        })}
      </div>

      {selected.length > 1 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 bg-card border shadow-lg rounded-full px-6 py-3 flex items-center gap-4 z-50 animate-in slide-in-from-bottom-5">
          <span className="font-medium">{selected.length} selected for comparison</span>
          <Button onClick={() => router.push(`/institutions/compare?ids=${selected.join(',')}`)}>
            Compare Now
          </Button>
        </div>
      )}
    </div>
  );
}
