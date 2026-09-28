import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatCurrency } from "@/lib/utils";
import { Briefcase, TrendingUp } from "lucide-react";
import Link from "next/link";
import { Career } from "@/lib/types";

export function CareerCard({ career }: { career: Career }) {
  return (
    <Card className="flex flex-col h-full hover:shadow-md transition-shadow">
      <CardContent className="p-6 flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-4">
          <div className="p-3 bg-primary/10 text-primary rounded-xl">
            <Briefcase className="w-6 h-6" />
          </div>
          {career.growthOutlook === "High" && (
            <Badge variant="success" className="flex items-center gap-1">
              <TrendingUp className="w-3 h-3" /> High Growth
            </Badge>
          )}
          {career.growthOutlook === "Medium" && (
            <Badge variant="secondary">Medium Growth</Badge>
          )}
          {career.growthOutlook === "Low" && (
            <Badge variant="warning">Low Growth</Badge>
          )}
        </div>
        <h3 className="text-xl font-bold mb-1 line-clamp-1">{career.title}</h3>
        <p className="text-sm text-muted-foreground mb-4">{career.industry}</p>
        
        <div className="mt-auto space-y-4">
          <div>
            <p className="text-xs text-muted-foreground mb-1">Avg. Salary</p>
            <p className="font-semibold text-primary">
              {formatCurrency(career.salaryRangeMin)} - {formatCurrency(career.salaryRangeMax)}
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            {career.requiredSkills.slice(0, 3).map((skill, i) => (
              <Badge key={i} variant="outline" className="text-xs font-normal">
                {skill}
              </Badge>
            ))}
            {career.requiredSkills.length > 3 && (
              <Badge variant="outline" className="text-xs font-normal">
                +{career.requiredSkills.length - 3}
              </Badge>
            )}
          </div>
        </div>
      </CardContent>
      <CardFooter className="p-6 pt-0">
        <Link href={`/careers/${career.id}`} className="w-full">
          <Button variant="outline" className="w-full group hover:bg-primary hover:text-primary-foreground">
            Explore Career
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
}
