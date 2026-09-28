"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EMICalculator } from "@/components/features/loans/EMICalculator";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function LoansPage() {
  return (
    <div className="space-y-6">
      <PageHeader 
        title="Funding & Loans" 
        description="Explore loan options and calculate your estimated repayments."
      />

      <Tabs defaultValue="calculator" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-3">
          <TabsTrigger value="calculator">Loan Calculator</TabsTrigger>
          <TabsTrigger value="products">Loan Products</TabsTrigger>
          <TabsTrigger value="estimator">Cost Estimator</TabsTrigger>
        </TabsList>
        
        <TabsContent value="calculator" className="mt-6">
          <EMICalculator />
        </TabsContent>

        <TabsContent value="products" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>EduTrust Global Loan</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Interest Rate</span>
                  <span className="font-medium">8.5% - 10%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Max Amount</span>
                  <span className="font-medium">$150,000</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Tenure</span>
                  <span className="font-medium">Up to 10 years</span>
                </div>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Apply on Lender Website</Button>
              </CardFooter>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="estimator" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Cost Estimator</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">Input your expected costs here to calculate your total funding gap.</p>
              {/* Form implementation skipped for brevity, matching mock */}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
