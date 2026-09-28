"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch"; // Assuming we have or will mock this, let's just use input type checkbox for now if switch is not imported
import { formatCurrency } from "@/lib/utils";

export default function ScenarioBuilderPage() {
  return (
    <div className="space-y-6">
      <PageHeader 
        title="Scenario: If I get the Tech Scholarship" 
        action={<Button>Save Changes</Button>}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-6 lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Adjust Variables</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <label className="text-sm font-medium mb-2 block">Academic Performance</label>
                <div className="flex justify-between text-xs text-muted-foreground mb-2">
                  <span>Current: 85%</span>
                  <span>Target: 95%</span>
                </div>
                <Slider defaultValue={[95]} min={0} max={100} step={1} />
              </div>
              
              <div>
                <label className="text-sm font-medium mb-2 block">Budget Increase/Decrease</label>
                <div className="flex justify-between text-xs text-muted-foreground mb-2">
                  <span>Base: $50,000</span>
                  <span>+20%</span>
                </div>
                <Slider defaultValue={[20]} min={-50} max={100} step={5} />
              </div>

              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Add Scholarship ($25k)</label>
                <input type="checkbox" defaultChecked className="w-4 h-4 accent-primary" />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Impact Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="p-4 border rounded-lg">
                  <div className="text-sm text-muted-foreground">New Total Cost</div>
                  <div className="text-2xl font-bold text-green-600">
                    {formatCurrency(85000)} <span className="text-sm line-through text-muted-foreground">{formatCurrency(120000)}</span>
                  </div>
                </div>
                <div className="p-4 border rounded-lg">
                  <div className="text-sm text-muted-foreground">Pathway Viability</div>
                  <div className="text-2xl font-bold text-primary">Highly Feasible</div>
                </div>
              </div>
              
              <h3 className="font-semibold mb-4">Affected Pathways</h3>
              <div className="space-y-4">
                <div className="p-4 bg-muted/50 rounded-lg border flex justify-between items-center">
                  <div>
                    <h4 className="font-medium">Software Engineer Path</h4>
                    <p className="text-sm text-muted-foreground">Financial constraint removed.</p>
                  </div>
                  <div className="text-green-600 font-bold">+15% Match</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
