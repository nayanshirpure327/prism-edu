type BrandLogoProps = {
  variant?: "horizontal" | "stacked";
  className?: string;
};

export function BrandLogo({ variant = "horizontal", className = "" }: BrandLogoProps) {
  const isStacked = variant === "stacked";

  return (
    <span
      className={`inline-flex shrink-0 items-center ${
        isStacked ? "flex-col gap-3 text-center" : "gap-3"
      } ${className}`}
    >
      <img
        src="/PrismEdu_logo.png"
        alt="Prism Edu Logo"
        className={`block object-contain ${isStacked ? "h-[72px] w-auto" : "h-10 w-auto"}`}
      />
      <span className={`flex flex-col ${isStacked ? "items-center" : "items-start"}`}>
        <span
          className={`whitespace-nowrap font-black leading-none tracking-tight text-[#12245a] ${
            isStacked ? "text-[30px]" : "text-2xl"
          }`}
        >
          PRISM<span className="text-[#5b46cf]">-EDU</span>
        </span>
        {isStacked && (
          <span className="mt-2 text-[10px] font-medium leading-4 text-[#46516e]">
            Predictive Risk & Intervention System
            <br />
            for Monitoring Education
          </span>
        )}
      </span>
    </span>
  );
}