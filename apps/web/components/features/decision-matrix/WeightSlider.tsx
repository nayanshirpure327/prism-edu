import { Slider } from "@/components/ui/slider";

interface WeightSliderProps {
  label: string;
  value: number;
  onChange: (val: number) => void;
}

export function WeightSlider({ label, value, onChange }: WeightSliderProps) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between">
        <label className="text-sm font-medium">{label}</label>
        <span className="text-sm font-semibold text-primary">{value}%</span>
      </div>
      <Slider 
        value={[value]} 
        min={0} 
        max={100} 
        step={5} 
        onValueChange={([val]) => onChange(val)} 
      />
    </div>
  );
}
