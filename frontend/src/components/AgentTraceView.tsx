import React, { useState } from 'react';
import {
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Terminal
} from 'lucide-react';
import { TraceEvent } from '../types/planner';

interface AgentTraceViewProps {
  trace: TraceEvent[];
  isLoading?: boolean;
}

export const AgentTraceView: React.FC<AgentTraceViewProps> = ({ trace, isLoading }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const formatNodeTitle = (node: string) => {
    return node
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="bg-[#11131c] rounded-2xl overflow-hidden border border-zinc-750 shadow-md transition-all duration-200">
      {/* Accordion Header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-5 py-4 flex items-center justify-between bg-zinc-900/60 hover:bg-zinc-900/90 transition-colors text-left cursor-pointer"
      >
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-zinc-800 text-zinc-200 flex items-center justify-center border border-zinc-700">
            <Terminal className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-xs text-white">Agent Execution Trace</span>
              <span className="px-2.5 py-0.5 rounded-full bg-zinc-800 text-[10px] text-emerald-400 font-mono font-bold border border-zinc-700">
                {trace.length} Steps
              </span>
            </div>
            <p className="text-[11px] text-zinc-400">Live LangGraph decision telemetry</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {isLoading && (
            <span className="flex items-center space-x-1.5 text-xs text-emerald-400 font-bold font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Thinking...</span>
            </span>
          )}
          {isOpen ? (
            <ChevronUp className="w-4 h-4 text-zinc-400" />
          ) : (
            <ChevronDown className="w-4 h-4 text-zinc-400" />
          )}
        </div>
      </button>

      {/* Trace Items */}
      {isOpen && (
        <div className="p-5 border-t border-zinc-800 bg-[#0c0e17]">
          {trace.length === 0 ? (
            <div className="text-center py-4 text-zinc-500 text-xs font-mono">
              Agent execution steps will stream here in real-time.
            </div>
          ) : (
            <div className="relative pl-5 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-px before:bg-zinc-700">
              {trace.map((evt, idx) => {
                const isRunning = evt.status === 'running';
                const isFailed = evt.status === 'failed';
                const isExpanded = expandedIndex === idx;

                return (
                  <div key={idx} className="relative group animate-fade-in">
                    {/* Stepper Marker */}
                    <div
                      className={`absolute -left-5 top-1 w-4 h-4 rounded-full flex items-center justify-center border ${
                        isRunning
                          ? 'bg-emerald-500/20 border-emerald-400 animate-pulse'
                          : isFailed
                          ? 'bg-red-500/20 border-red-400'
                          : 'bg-zinc-900 border-zinc-600'
                      }`}
                    >
                      {isRunning ? (
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                      ) : (
                        <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                      )}
                    </div>

                    {/* Step Card */}
                    <div className="bg-[#141622] rounded-xl p-3.5 border border-zinc-750 space-y-1.5">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-xs text-white">
                          {formatNodeTitle(evt.node)}
                        </span>

                        <div className="flex items-center space-x-2">
                          {evt.duration_ms > 0 && (
                            <span className="text-[10px] font-mono text-zinc-300 font-bold bg-zinc-800 px-2 py-0.5 rounded">
                              {evt.duration_ms}ms
                            </span>
                          )}
                          <span
                            className={`text-[9px] uppercase font-mono font-bold px-2 py-0.5 rounded ${
                              isRunning
                                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                                : isFailed
                                ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                                : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                            }`}
                          >
                            {evt.status}
                          </span>
                        </div>
                      </div>

                      <p className="text-xs text-zinc-300 font-normal leading-relaxed">{evt.message}</p>

                      {evt.data && Object.keys(evt.data).length > 0 && (
                        <div className="mt-2 pt-2 border-t border-zinc-800">
                          <button
                            onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                            className="text-[10px] text-emerald-400 hover:text-emerald-300 font-mono font-semibold transition-colors cursor-pointer"
                          >
                            {isExpanded ? '[-] Hide tool payload' : '[+] Inspect tool payload'}
                          </button>

                          {isExpanded && (
                            <pre className="mt-2 p-2.5 bg-black/80 rounded-lg text-[10px] font-mono text-emerald-300 overflow-x-auto border border-zinc-800">
                              {JSON.stringify(evt.data, null, 2)}
                            </pre>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
