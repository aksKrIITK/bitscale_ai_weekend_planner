import { useState, useRef, useEffect } from 'react';
import { PlanRequest, PlanResponse, FinalPlan, TraceEvent } from '../types/planner';
import { createPlan, sendClarification, createTraceEventSource } from '../services/api';

export const usePlanner = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [plan, setPlan] = useState<FinalPlan | null>(null);
  const [trace, setTrace] = useState<TraceEvent[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [needsClarification, setNeedsClarification] = useState(false);
  const [clarificationQuestion, setClarificationQuestion] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);

  const cleanupSSE = () => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  };

  useEffect(() => {
    return () => cleanupSSE();
  }, []);

  const handleCreatePlan = async (request: PlanRequest) => {
    setIsLoading(true);
    setError(null);
    setPlan(null);
    setTrace([]);
    setNeedsClarification(false);
    setClarificationQuestion(null);

    // Generate client-side session ID for SSE streaming correlation
    const activeSessionId = 'session_' + Math.random().toString(36).substring(2, 11);
    setSessionId(activeSessionId);

    // Start SSE listener
    cleanupSSE();
    try {
      const sse = createTraceEventSource(activeSessionId);
      eventSourceRef.current = sse;

      sse.addEventListener('trace', (e: MessageEvent) => {
        try {
          const eventData: TraceEvent = JSON.parse(e.data);
          setTrace((prev) => {
            // Deduplicate if already exists with same node & status
            const filtered = prev.filter(
              (p) => !(p.node === eventData.node && p.status === eventData.status)
            );
            return [...filtered, eventData];
          });
        } catch (err) {
          // Ignore JSON parse errors from SSE heartbeats
        }
      });

      sse.onerror = () => {
        cleanupSSE();
      };
    } catch (err) {
      // SSE connection error fallback
    }

    try {
      const response: PlanResponse = await createPlan(request, activeSessionId);

      if (response.needs_clarification && response.clarification_question) {
        setNeedsClarification(true);
        setClarificationQuestion(response.clarification_question);
      } else if (response.plan) {
        setPlan(response.plan);
      }

      // Merge trace from response if SSE missed anything
      if (response.trace && response.trace.length > 0) {
        setTrace((prev) => {
          const map = new Map();
          [...prev, ...response.trace].forEach((evt) => {
            map.set(`${evt.node}_${evt.status}`, evt);
          });
          return Array.from(map.values());
        });
      }
    } catch (err: any) {
      const errorMsg =
        err.response?.data?.detail ||
        err.message ||
        "We couldn't reach the planner right now. Please verify the backend is running.";
      setError(errorMsg);
    } finally {
      setIsLoading(false);
      cleanupSSE();
    }
  };

  const handleClarificationSubmit = async (clarification: string) => {
    if (!sessionId) return;
    setIsLoading(true);
    setNeedsClarification(false);
    setError(null);

    try {
      const response = await sendClarification(sessionId, clarification);
      if (response.plan) {
        setPlan(response.plan);
      }
      if (response.trace) {
        setTrace(response.trace);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to submit clarification.');
    } finally {
      setIsLoading(false);
    }
  };

  const resetPlan = () => {
    setPlan(null);
    setTrace([]);
    setError(null);
    setNeedsClarification(false);
    setClarificationQuestion(null);
    cleanupSSE();
  };

  return {
    plan,
    trace,
    isLoading,
    error,
    needsClarification,
    clarificationQuestion,
    handleCreatePlan,
    handleClarificationSubmit,
    resetPlan,
  };
};
