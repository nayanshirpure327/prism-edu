import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { pathwaysAPI } from "@/lib/api";

export function usePathways() {
  return useQuery({
    queryKey: ["pathways"],
    queryFn: async () => {
      const res = await pathwaysAPI.listPathways();
      return res.data;
    },
  });
}

export function usePathway(id: string) {
  return useQuery({
    queryKey: ["pathway", id],
    queryFn: async () => {
      const res = await pathwaysAPI.getPathway(id);
      return res.data;
    },
    enabled: !!id,
  });
}

export function useGeneratePathway() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: any) => pathwaysAPI.generatePathways(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["pathways"] });
    },
  });
}
