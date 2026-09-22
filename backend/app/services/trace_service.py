import asyncio
import time
from typing import Dict, List, Any, Optional, AsyncGenerator
from app.schemas.planner import TraceEvent


class TraceService:
    """
    Manages session-level trace events and real-time SSE subscriptions.
    """

    def __init__(self):
        self._traces: Dict[str, List[Dict[str, Any]]] = {}
        self._queues: Dict[str, List[asyncio.Queue]] = {}

    def init_session(self, session_id: str):
        if session_id not in self._traces:
            self._traces[session_id] = []
        if session_id not in self._queues:
            self._queues[session_id] = []

    def add_event(
        self,
        session_id: str,
        node: str,
        status: str,
        message: str,
        duration_ms: int = 0,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        self.init_session(session_id)
        
        event = {
            "node": node,
            "status": status,
            "message": message,
            "duration_ms": duration_ms,
            "data": data or {},
            "timestamp": time.time()
        }
        
        self._traces[session_id].append(event)
        
        # Broadcast to all active SSE listener queues for this session
        for q in self._queues.get(session_id, []):
            try:
                q.put_nowait(event)
            except Exception:
                pass
                
        return event

    def get_traces(self, session_id: str) -> List[Dict[str, Any]]:
        return self._traces.get(session_id, [])

    async def subscribe(self, session_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        self.init_session(session_id)
        queue: asyncio.Queue = asyncio.Queue()
        self._queues[session_id].append(queue)
        
        # First send any existing events that have already occurred
        for past_event in self._traces.get(session_id, []):
            yield past_event

        try:
            while True:
                event = await queue.get()
                yield event
                if event.get("node") in ["generate_final_plan", "ask_clarification"] and event.get("status") in ["completed", "failed"]:
                    break
        finally:
            if session_id in self._queues and queue in self._queues[session_id]:
                self._queues[session_id].remove(queue)


trace_service = TraceService()
