import { useQuery } from "@tanstack/react-query";
import { institutionsAPI } from "@/lib/api";

export function useInstitutions(params?: any) {
  return useQuery({
    queryKey: ["institutions", params],
    queryFn: async () => {
      const res = await institutionsAPI.listInstitutions(params);
      return res.data;
    },
  });
}

export function useInstitution(slug: string) {
  return useQuery({
    queryKey: ["institution", slug],
    queryFn: async () => {
      const res = await institutionsAPI.getInstitution(slug);
      return res.data;
    },
    enabled: !!slug,
  });
}
