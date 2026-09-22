import React from 'react';
import {
  Wallet,
  Clock,
  Repeat,
  ShieldCheck,
  Info
} from 'lucide-react';
import { FinalPlan, TraceEvent } from '../types/planner';
import { TimelineView } from './TimelineView';
import { AgentTraceView } from './AgentTraceView';
import { ErrorBanner } from './ErrorBanner';

interface PlanResultProps {
  plan: FinalPlan;
  trace: TraceEvent[];
  onReset: () => void;
  isLoading?: boolean;
}

export const PlanResult: React.FC<PlanResultProps> = ({
  plan,
  trace,
  onReset,
  isLoading
}) => {
  const budgetPercent = Math.min(
    100,
    Math.round((plan.total_cost / (plan.total_cost + plan.remaining_budget || 1)) * 100)
  );

  const hours = Math.floor(plan.total_duration_minutes / 60);
  const minutes = plan.total_duration_minutes % 60;

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Fallback Banner */}
      {plan.is_fallback && (
        <ErrorBanner
          type="warning"
          title="Adjusted Fallback Plan"
          message={
            plan.fallback_reason ||
            "No exact candidate combination met all strict criteria simultaneously, so a guaranteed feasible alternative was generated."
          }
        />
      )}

      {/* Plan Header Card */}
      <div className="minimal-card rounded-2xl p-6 sm:p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-medium">
              Personalized Plan
            </span>
          </div>

          <button
            onClick={onReset}
            className="interactive-chip flex items-center space-x-2 text-xs font-medium px-3.5 py-1.5 rounded-xl bg-zinc-900 border border-zinc-800 hover:border-zinc-700 text-zinc-300 transition-colors cursor-pointer"
          >
            <Repeat className="w-3.5 h-3.5" />
            <span>Create New Plan</span>
          </button>
        </div>

        <div>
          <h2 className="text-2xl sm:text-3xl font-bold text-zinc-100 tracking-tight mb-2">
            {plan.title}
          </h2>
          <p className="text-sm sm:text-base text-zinc-400 leading-relaxed max-w-3xl">
            {plan.summary}
          </p>
        </div>

        {/* Metric Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-zinc-800/80">
          {/* Estimated Spend */}
          <div className="bg-zinc-900/60 rounded-xl p-4 border border-zinc-850">
            <div className="flex items-center justify-between text-xs text-zinc-400 mb-1">
              <span className="flex items-center space-x-1.5">
                <Wallet className="w-3.5 h-3.5 text-zinc-400" />
                <span>Estimated Spend</span>
              </span>
              <span className="font-mono text-xs text-zinc-400">{budgetPercent}%</span>
            </div>
            <div className="text-xl font-bold text-zinc-100 font-mono">
              ₹{plan.total_cost.toFixed(0)}
              <span className="text-xs text-zinc-400 font-normal font-sans ml-1.5">
                (₹{plan.remaining_budget.toFixed(0)} remaining)
              </span>
            </div>
            <div className="w-full bg-zinc-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div
                className="bg-emerald-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${budgetPercent}%` }}
              ></div>
            </div>
          </div>

          {/* Time Window */}
          <div className="bg-zinc-900/60 rounded-xl p-4 border border-zinc-850">
            <div className="flex items-center justify-between text-xs text-zinc-400 mb-1">
              <span className="flex items-center space-x-1.5">
                <Clock className="w-3.5 h-3.5 text-zinc-400" />
                <span>Total Duration</span>
              </span>
              <span className="font-mono text-xs text-zinc-400">{plan.timeline.length} Stops</span>
            </div>
            <div className="text-xl font-bold text-zinc-100">
              {hours}h {minutes > 0 ? `${minutes}m` : ''}
              <span className="text-xs text-zinc-400 font-normal ml-1.5">door-to-door</span>
            </div>
            <p className="text-[11px] text-zinc-500 mt-2">Includes activity + 20m buffers</p>
          </div>

          {/* Verification Status */}
          <div className="bg-zinc-900/60 rounded-xl p-4 border border-zinc-850">
            <div className="flex items-center justify-between text-xs text-zinc-400 mb-1">
              <span className="flex items-center space-x-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Constraint Checks</span>
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-medium">
                Verified
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5 mt-2">
              <span className="text-[11px] px-2 py-0.5 rounded-md bg-zinc-900 text-zinc-300 border border-zinc-800 flex items-center space-x-1">
                <span className="text-emerald-400">✓</span>
                <span>Budget</span>
              </span>
              <span className="text-[11px] px-2 py-0.5 rounded-md bg-zinc-900 text-zinc-300 border border-zinc-800 flex items-center space-x-1">
                <span className="text-emerald-400">✓</span>
                <span>Schedule</span>
              </span>
              <span className="text-[11px] px-2 py-0.5 rounded-md bg-zinc-900 text-zinc-300 border border-zinc-800 flex items-center space-x-1">
                <span className="text-emerald-400">✓</span>
                <span>Dietary</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content: Timeline + Trade-offs & Agent Trace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Timeline Column */}
        <div className="lg:col-span-7 space-y-6">
          <TimelineView timeline={plan.timeline} />
        </div>

        {/* Side Column: Trade-offs & Trace */}
        <div className="lg:col-span-5 space-y-6">
          {/* Trade-offs Explanation Card */}
          {plan.tradeoffs && plan.tradeoffs.length > 0 && (
            <div className="minimal-card rounded-2xl p-5 space-y-3">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 flex items-center space-x-1.5">
                <Info className="w-3.5 h-3.5 text-zinc-400" />
                <span>Trade-offs & Reasoning</span>
              </h3>
              <ul className="space-y-2.5">
                {plan.tradeoffs.map((item, idx) => (
                  <li key={idx} className="flex items-start space-x-2 text-xs text-zinc-300 leading-relaxed">
                    <span className="text-zinc-500 font-bold shrink-0 mt-0.5">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Trace Accordion */}
          <AgentTraceView trace={trace} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};
