"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { formatCurrency } from "@/lib/utils";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function EMICalculator() {
  const [principal, setPrincipal] = useState(50000);
  const [rate, setRate] = useState(8.5);
  const [tenure, setTenure] = useState(60); // months

  const calculateEMI = () => {
    const r = rate / (12 * 100);
    const emi = (principal * r * Math.pow(1 + r, tenure)) / (Math.pow(1 + r, tenure) - 1);
    return emi;
  };

  const emi = calculateEMI();
  const totalRepayment = emi * tenure;
  const totalInterest = totalRepayment - principal;

  const chartData = Array.from({ length: tenure / 12 }, (_, i) => ({
    year: `Year ${i + 1}`,
    balance: Math.max(0, principal - (principal / (tenure/12)) * (i+1)),
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <Card>
        <CardHeader>
          <CardTitle>Loan Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium">Loan Amount (Principal)</label>
              <span className="font-semibold text-primary">{formatCurrency(principal)}</span>
            </div>
            <Slider 
              value={[principal]} 
              min={5000} 
              max={200000} 
              step={1000}
              onValueChange={([val]) => setPrincipal(val)} 
            />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium">Interest Rate (p.a.)</label>
              <span className="font-semibold text-primary">{rate}%</span>
            </div>
            <Slider 
              value={[rate]} 
              min={1} 
              max={20} 
              step={0.1}
              onValueChange={([val]) => setRate(val)} 
            />
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium">Tenure (Months)</label>
              <span className="font-semibold text-primary">{tenure} mo</span>
            </div>
            <Slider 
              value={[tenure]} 
              min={12} 
              max={120} 
              step={12}
              onValueChange={([val]) => setTenure(val)} 
            />
          </div>
        </CardContent>
      </Card>

      <Card className="bg-primary/5 border-primary/20">
        <CardContent className="p-6">
          <div className="text-center mb-6">
            <h3 className="text-lg font-medium text-muted-foreground">Estimated Monthly EMI</h3>
            <div className="text-5xl font-bold text-primary mt-2">{formatCurrency(emi)}</div>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between pb-2 border-b">
              <span className="text-muted-foreground">Principal Amount</span>
              <span className="font-medium">{formatCurrency(principal)}</span>
            </div>
            <div className="flex justify-between pb-2 border-b">
              <span className="text-muted-foreground">Total Interest</span>
              <span className="font-medium">{formatCurrency(totalInterest)}</span>
            </div>
            <div className="flex justify-between pb-2 border-b font-semibold">
              <span>Total Repayment</span>
              <span>{formatCurrency(totalRepayment)}</span>
            </div>
          </div>
          
          <div className="mt-8 h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <XAxis dataKey="year" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="balance" stroke="#7c3aed" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          
          <p className="text-xs text-center text-muted-foreground mt-4">
            * This is an estimate. Actual terms vary by lender.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
