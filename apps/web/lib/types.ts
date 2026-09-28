export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: "STUDENT" | "PARENT" | "COUNSELOR";
}

export interface StudentProfile {
  id: string;
  userId: string;
  dateOfBirth?: string;
  gender?: string;
  phone?: string;
  city?: string;
  country?: string;
  completionPercentage: number;
}

export interface AcademicRecord {
  id: string;
  subject: string;
  marks: number;
  totalMarks: number;
  grade: string;
  year: number;
}

export interface WorkPreference {
  id: string;
  teamVsIndividual: number;
  creativeVsAnalytical: number;
  indoorVsOutdoor: number;
}

export interface Assessment {
  id: string;
  title: string;
  description: string;
  type: "APTITUDE" | "INTEREST";
  questionCount: number;
  estimatedMinutes: number;
}

export interface AssessmentQuestion {
  id: string;
  text: string;
  type: "MCQ" | "RATING";
  options?: string[];
}

export interface AssessmentAttempt {
  id: string;
  assessmentId: string;
  status: "IN_PROGRESS" | "COMPLETED";
  startedAt: string;
  completedAt?: string;
}

export interface AssessmentResult {
  id: string;
  attemptId: string;
  scores: Record<string, number>;
  recommendations: string[];
}

export interface Career {
  id: string;
  title: string;
  industry: string;
  description: string;
  growthOutlook: "High" | "Medium" | "Low";
  salaryRangeMin: number;
  salaryRangeMax: number;
  requiredSkills: string[];
}

export interface Industry {
  id: string;
  name: string;
}

export interface Skill {
  id: string;
  name: string;
}

export interface Institution {
  id: string;
  name: string;
  country: string;
  city: string;
  type: "University" | "College" | "Institute";
  ranking?: number;
  description: string;
  establishedYear?: number;
}

export interface Program {
  id: string;
  institutionId: string;
  name: string;
  degree: string;
  durationMonths: number;
  tuitionFee: number;
  deadline?: string;
}

export interface ProgramRequirement {
  id: string;
  programId: string;
  requirementType: string;
  description: string;
}

export interface Scholarship {
  id: string;
  name: string;
  provider: string;
  amount: number;
  deadline: string;
  coverageType: string;
  eligibility: string;
}

export interface LoanProduct {
  id: string;
  provider: string;
  name: string;
  type: string;
  interestRateMin: number;
  interestRateMax: number;
  maxAmount: number;
  maxTenureMonths: number;
}

export interface Pathway {
  id: string;
  title: string;
  careerId: string;
  compatibilityScore: number;
  totalEstimatedCost: number;
  totalDurationMonths: number;
}

export interface PathwayStep {
  id: string;
  pathwayId: string;
  order: number;
  title: string;
  description: string;
  durationMonths: number;
  costEstimate: number;
  institutionId?: string;
  programId?: string;
}

export interface Scenario {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface ScenarioChange {
  id: string;
  scenarioId: string;
  type: string;
  value: any;
}

export interface DecisionMatrixResult {
  pathwayId: string;
  scores: Record<string, number>;
  totalScore: number;
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  read: boolean;
  createdAt: string;
}

export interface Report {
  id: string;
  title: string;
  generatedAt: string;
  sizeKb: number;
  downloadUrl: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

export interface ErrorResponse {
  error: string;
  details?: any;
}
