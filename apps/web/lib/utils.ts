import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency: string = "USD") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount);
}

export function formatPercentage(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "percent",
    minimumFractionDigits: 0,
    maximumFractionDigits: 1,
  }).format(value / 100);
}

export function formatDuration(months: number) {
  if (months < 12) {
    return `${months} months`;
  }
  const years = Math.floor(months / 12);
  const rem = months % 12;
  return `${years} year${years > 1 ? "s" : ""}${
    rem > 0 ? ` ${rem} month${rem > 1 ? "s" : ""}` : ""
  }`;
}

export function getInitials(name: string) {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .substring(0, 2);
}

export function getGradeColor(percentage: number) {
  if (percentage >= 90) return "text-green-600 dark:text-green-400";
  if (percentage >= 75) return "text-blue-600 dark:text-blue-400";
  if (percentage >= 60) return "text-yellow-600 dark:text-yellow-400";
  return "text-red-600 dark:text-red-400";
}

export function truncate(text: string, length: number) {
  if (text.length <= length) return text;
  return text.substring(0, length) + "...";
}
