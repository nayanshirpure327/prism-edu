import { useQuery } from "@tanstack/react-query";
import { careersAPI } from "@/lib/api";

export function useCareers(params?: any) {
  return useQuery({
    queryKey: ["careers", params],
    queryFn: async () => {
      const res = await careersAPI.listCareers(params);
      return res.data;
    },
  });
}

export function useCareer(slug: string) {
  return useQuery({
    queryKey: ["career", slug],
    queryFn: async () => {
      const res = await careersAPI.getCareer(slug);
      return res.data;
    },
    enabled: !!slug,
  });
}
