import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { profileAPI } from "@/lib/api";

export function useProfile() {
  const queryClient = useQueryClient();

  const profileQuery = useQuery({
    queryKey: ["profile"],
    queryFn: async () => {
      const res = await profileAPI.getProfile();
      return res.data;
    },
  });

  const updateProfileMutation = useMutation({
    mutationFn: (data: any) => profileAPI.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  const submitWizardMutation = useMutation({
    mutationFn: ({ step, data }: { step: number; data: any }) => 
      profileAPI.submitWizardStep(step, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["profile"] });
    },
  });

  return {
    profile: profileQuery.data,
    isLoading: profileQuery.isLoading,
    error: profileQuery.error,
    updateProfile: updateProfileMutation.mutateAsync,
    submitWizardStep: submitWizardMutation.mutateAsync,
    isUpdating: updateProfileMutation.isPending || submitWizardMutation.isPending,
  };
}
