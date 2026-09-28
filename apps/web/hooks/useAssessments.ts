import { useQuery, useMutation } from "@tanstack/react-query";
import { assessmentsAPI } from "@/lib/api";

export function useAssessments() {
  return useQuery({
    queryKey: ["assessments"],
    queryFn: async () => {
      const res = await assessmentsAPI.listAssessments();
      return res.data;
    },
  });
}

export function useAssessmentAttempt(id: string) {
  return useMutation({
    mutationFn: () => assessmentsAPI.startAttempt(id),
  });
}

export function useAssessmentResult(id: string) {
  return useQuery({
    queryKey: ["assessment-result", id],
    queryFn: async () => {
      const res = await assessmentsAPI.getResult(id);
      return res.data;
    },
    enabled: !!id,
  });
}
