import { useQuery } from "@tanstack/react-query";
import { scholarshipsAPI } from "@/lib/api";

export function useScholarships(params?: any) {
  return useQuery({
    queryKey: ["scholarships", params],
    queryFn: async () => {
      const res = await scholarshipsAPI.listScholarships(params);
      return res.data;
    },
  });
}
