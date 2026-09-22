import axios from 'axios';
import { PlanRequest, PlanResponse } from '../types/planner';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const checkHealth = async () => {
  const res = await apiClient.get('/health');
  return res.data;
};

export const createPlan = async (request: PlanRequest, sessionId?: string): Promise<PlanResponse> => {
  const url = sessionId ? `/api/planner/plan?session_id=${sessionId}` : '/api/planner/plan';
  const res = await apiClient.post<PlanResponse>(url, request);
  return res.data;
};

export const sendClarification = async (sessionId: string, clarification: string): Promise<PlanResponse> => {
  const res = await apiClient.post<PlanResponse>('/api/planner/clarify', {
    session_id: sessionId,
    clarification,
  });
  return res.data;
};

export const createTraceEventSource = (sessionId: string): EventSource => {
  return new EventSource(`${API_BASE_URL}/api/planner/${sessionId}/stream`);
};
