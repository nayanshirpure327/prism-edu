import { BrandLogo } from "@/components/common/BrandLogo";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-prism-bg dark:bg-background flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <BrandLogo variant="stacked" className="mx-auto" />
          <p className="text-muted-foreground mt-2">Discover Your Perfect Career Path</p>
        </div>
        {children}
      </div>
    </div>
  );
}
