import axios from "axios";
import { 
  User, 
  ApiResponse, 
  PaginatedResponse,
  StudentProfile,
  Assessment,
  AssessmentAttempt,
  AssessmentResult,
  Career,
  Institution,
  Scholarship,
  LoanProduct,
  Pathway,
  Scenario,
  DecisionMatrixResult,
  Report
} from "./types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (data: any) => api.post<{token: string, user: User}>('/api/auth/login', data),
  register: (data: any) => api.post<{token: string, user: User}>('/api/auth/register', data),
  getMe: () => api.get<User>('/api/auth/me'),
};

export const profileAPI = {
  getProfile: () => api.get<StudentProfile>('/api/profile'),
  updateProfile: (data: Partial<StudentProfile>) => api.put<StudentProfile>('/api/profile', data),
  submitWizardStep: (step: number, data: any) => api.post(`/api/profile/wizard/${step}`, data),
};

export const assessmentsAPI = {
  listAssessments: () => api.get<Assessment[]>('/api/assessments'),
  startAttempt: (id: string) => api.post<AssessmentAttempt>(`/api/assessments/${id}/attempts`),
  submitAnswers: (attemptId: string, answers: any) => api.post<AssessmentResult>(`/api/assessments/attempts/${attemptId}/submit`, { answers }),
  getResult: (id: string) => api.get<AssessmentResult>(`/api/assessments/results/${id}`),
};

export const careersAPI = {
  listCareers: (params?: any) => api.get<PaginatedResponse<Career>>('/api/careers', { params }),
  getCareer: (slug: string) => api.get<Career>(`/api/careers/${slug}`),
  searchCareers: (query: string) => api.get<Career[]>('/api/careers/search', { params: { q: query } }),
  saveCareer: (id: string) => api.post(`/api/careers/${id}/save`),
  getSavedCareers: () => api.get<Career[]>('/api/careers/saved'),
};

export const institutionsAPI = {
  listInstitutions: (params?: any) => api.get<PaginatedResponse<Institution>>('/api/institutions', { params }),
  getInstitution: (slug: string) => api.get<Institution>(`/api/institutions/${slug}`),
  searchInstitutions: (query: string) => api.get<Institution[]>('/api/institutions/search', { params: { q: query } }),
  compareInstitutions: (ids: string[]) => api.post<Institution[]>('/api/institutions/compare', { ids }),
};

export const scholarshipsAPI = {
  listScholarships: (params?: any) => api.get<PaginatedResponse<Scholarship>>('/api/scholarships', { params }),
  getScholarship: (id: string) => api.get<Scholarship>(`/api/scholarships/${id}`),
  matchScholarships: () => api.get<Scholarship[]>('/api/scholarships/match'),
};

export const loansAPI = {
  listLoanProducts: (params?: any) => api.get<PaginatedResponse<LoanProduct>>('/api/loans', { params }),
  calculateEMI: (data: any) => api.post<any>('/api/loans/calculate', data),
  compareLoanProducts: (ids: string[]) => api.post<LoanProduct[]>('/api/loans/compare', { ids }),
};

export const pathwaysAPI = {
  generatePathways: (data: any) => api.post<Pathway[]>('/api/pathways/generate', data),
  listPathways: () => api.get<Pathway[]>('/api/pathways'),
  getPathway: (id: string) => api.get<Pathway>(`/api/pathways/${id}`),
};

export const scenariosAPI = {
  createScenario: (data: any) => api.post<Scenario>('/api/scenarios', data),
  listScenarios: () => api.get<Scenario[]>('/api/scenarios'),
  cloneScenario: (id: string) => api.post<Scenario>(`/api/scenarios/${id}/clone`),
  compareScenarios: (id1: string, id2: string) => api.get<any>(`/api/scenarios/compare`, { params: { a: id1, b: id2 } }),
};

export const decisionMatrixAPI = {
  getMatrix: () => api.get<DecisionMatrixResult[]>('/api/matrix'),
  updateWeights: (weights: Record<string, number>) => api.post('/api/matrix/weights', { weights }),
};

export const reportsAPI = {
  generateReport: () => api.post<Report>('/api/reports/generate'),
  getReportStatus: (id: string) => api.get<Report>(`/api/reports/${id}`),
  downloadReport: (id: string) => api.get(`/api/reports/${id}/download`, { responseType: 'blob' }),
};

export default api;
