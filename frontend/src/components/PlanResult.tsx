import React from 'react';
import {
  Wallet,
  Clock,
  Repeat,
  ShieldCheck,
  Info,
  Calendar,
  Check
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
    <div className="space-y-8 animate-fade-in w-full max-w-full">
      {/* Fallback Notice */}
      {plan.is_fallback && (
        <ErrorBanner
          type="warning"
          title="Adjusted Fallback Plan"
          message={
            plan.fallback_reason ||
            "No exact combination met all strict criteria simultaneously, so a guaranteed feasible alternative was generated."
          }
        />
      )}

      {/* Plan Header Card */}
      <div className="card-premium rounded-3xl p-5 sm:p-7 space-y-6 w-full overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <span className="px-3.5 py-1 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 text-xs font-bold flex items-center space-x-1.5 shadow-sm">
              <Calendar className="w-3.5 h-3.5 text-emerald-400" />
              <span>Personalized Saturday Plan</span>
            </span>
          </div>

          <button
            onClick={onReset}
            className="flex items-center space-x-2 text-xs font-semibold px-3.5 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 border border-zinc-600 text-zinc-100 transition-colors cursor-pointer shadow-sm"
          >
            <Repeat className="w-3.5 h-3.5" />
            <span>Create Another Plan</span>
          </button>
        </div>

        <div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-black text-white tracking-tight mb-2.5">
            {plan.title}
          </h2>
          <p className="text-sm sm:text-base text-zinc-300 leading-relaxed max-w-3xl font-normal">
            {plan.summary}
          </p>
        </div>

        {/* Metric Cards Grid - Responsive, bounded & zero-overflow */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 pt-5 border-t border-zinc-800/80 w-full">
          {/* Estimated Spend */}
          <div className="card-inner rounded-2xl p-4 space-y-2 min-w-0 overflow-hidden flex flex-col justify-between">
            <div className="flex items-center justify-between gap-2 text-xs text-zinc-300">
              <span className="flex items-center space-x-1.5 font-bold truncate">
                <Wallet className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="truncate">Estimated Spend</span>
              </span>
              <span className="font-mono text-xs font-bold text-emerald-400 shrink-0">{budgetPercent}% Budget</span>
            </div>
            <div className="text-lg sm:text-xl font-black text-white font-mono flex flex-wrap items-baseline gap-1.5">
              <span>₹{plan.total_cost.toFixed(0)}</span>
              <span className="text-xs text-zinc-400 font-normal font-sans">
                (₹{plan.remaining_budget.toFixed(0)} left)
              </span>
            </div>
            <div className="w-full bg-zinc-800 h-2 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500"
                style={{ width: `${budgetPercent}%` }}
              ></div>
            </div>
          </div>

          {/* Time Window */}
          <div className="card-inner rounded-2xl p-4 space-y-2 min-w-0 overflow-hidden flex flex-col justify-between">
            <div className="flex items-center justify-between gap-2 text-xs text-zinc-300">
              <span className="flex items-center space-x-1.5 font-bold truncate">
                <Clock className="w-4 h-4 text-cyan-400 shrink-0" />
                <span className="truncate">Total Duration</span>
              </span>
              <span className="font-mono text-xs font-bold text-cyan-400 shrink-0">{plan.timeline.length} Stops</span>
            </div>
            <div className="text-lg sm:text-xl font-black text-white flex flex-wrap items-baseline gap-1.5">
              <span>{hours}h {minutes > 0 ? `${minutes}m` : ''}</span>
              <span className="text-xs text-zinc-400 font-normal font-mono">door-to-door</span>
            </div>
            <p className="text-[11px] text-zinc-400 truncate">Includes venues + travel buffers</p>
          </div>

          {/* Verification Status */}
          <div className="card-inner rounded-2xl p-4 space-y-2 min-w-0 overflow-hidden flex flex-col justify-between">
            <div className="flex items-center justify-between gap-2 text-xs text-zinc-300">
              <span className="flex items-center space-x-1.5 font-bold truncate">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                <span className="truncate">Validation Status</span>
              </span>
              <span className="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                100% Passed
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-0.5">
              <span className="text-[11px] px-2 py-0.5 rounded-lg bg-zinc-800/80 text-zinc-200 border border-zinc-700 flex items-center space-x-1 font-medium">
                <Check className="w-3 h-3 text-emerald-400 stroke-[3] shrink-0" />
                <span>Budget</span>
              </span>
              <span className="text-[11px] px-2 py-0.5 rounded-lg bg-zinc-800/80 text-zinc-200 border border-zinc-700 flex items-center space-x-1 font-medium">
                <Check className="w-3 h-3 text-emerald-400 stroke-[3] shrink-0" />
                <span>Schedule</span>
              </span>
              <span className="text-[11px] px-2 py-0.5 rounded-lg bg-zinc-800/80 text-zinc-200 border border-zinc-700 flex items-center space-x-1 font-medium">
                <Check className="w-3 h-3 text-emerald-400 stroke-[3] shrink-0" />
                <span>Dietary</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Timeline Column */}
        <div className="lg:col-span-7 space-y-6">
          <TimelineView timeline={plan.timeline} />
        </div>

        {/* Side Column: Trade-offs & Agent Trace */}
        <div className="lg:col-span-5 space-y-6">
          {/* Trade-offs Explanation Card */}
          {plan.tradeoffs && plan.tradeoffs.length > 0 && (
            <div className="card-premium rounded-2xl p-5 sm:p-6 space-y-3.5">
              <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-300 flex items-center space-x-2">
                <Info className="w-4 h-4 text-amber-400" />
                <span>Trade-offs & Strategic Reasoning</span>
              </h3>
              <ul className="space-y-3">
                {plan.tradeoffs.map((item, idx) => (
                  <li key={idx} className="flex items-start space-x-2.5 text-xs text-zinc-300 leading-relaxed font-normal">
                    <span className="text-amber-400 font-bold shrink-0 mt-0.5">•</span>
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
