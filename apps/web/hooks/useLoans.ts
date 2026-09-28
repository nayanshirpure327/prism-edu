import { useQuery } from "@tanstack/react-query";
import { loansAPI } from "@/lib/api";

export function useLoans(params?: any) {
  return useQuery({
    queryKey: ["loans", params],
    queryFn: async () => {
      const res = await loansAPI.listLoanProducts(params);
      return res.data;
    },
  });
}
