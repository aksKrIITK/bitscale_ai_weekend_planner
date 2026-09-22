export interface PlanRequest {
  city: string;
  budget: number;
  available_time: string;
  mood: string;
  interests: string[];
  constraints: string[];
}

export interface TimelineItem {
  start: string;
  end: string;
  type: string;
  name: string;
  cost: number;
  why: string;
  area?: string;
  crowd_level?: string;
}

export interface ValidationStatus {
  budget_ok: boolean;
  time_ok: boolean;
  constraints_ok: boolean;
  details?: string[];
}

export interface FinalPlan {
  title: string;
  summary: string;
  total_cost: number;
  remaining_budget: number;
  total_duration_minutes: number;
  timeline: TimelineItem[];
  tradeoffs: string[];
  validation: ValidationStatus;
  is_fallback?: boolean;
  fallback_reason?: string;
}

export interface TraceEvent {
  node: string;
  status: 'running' | 'completed' | 'failed' | 'skipped';
  message: string;
  duration_ms: number;
  data?: Record<string, any>;
  timestamp?: number;
}

export interface PlanResponse {
  session_id: string;
  plan: FinalPlan | null;
  needs_clarification: boolean;
  clarification_question?: string;
  trace: TraceEvent[];
  is_mock_data: boolean;
}
