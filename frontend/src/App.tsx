import React from 'react';
import { Navbar } from './components/Navbar';
import { PlannerForm } from './components/PlannerForm';
import { PlanResult } from './components/PlanResult';
import { AgentTraceView } from './components/AgentTraceView';
import { ClarificationModal } from './components/ClarificationModal';
import { ErrorBanner } from './components/ErrorBanner';
import { usePlanner } from './hooks/usePlanner';
import { ShieldCheck, Compass, Zap } from 'lucide-react';

export const App: React.FC = () => {
  const {
    plan,
    trace,
    isLoading,
    error,
    needsClarification,
    clarificationQuestion,
    handleCreatePlan,
    handleClarificationSubmit,
    resetPlan,
  } = usePlanner();

  return (
    <div className="min-h-screen bg-[#090a0f] text-zinc-100 flex flex-col font-sans selection:bg-emerald-500/20 selection:text-emerald-300">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-10 sm:py-14">
        {/* Error Banner */}
        {error && (
          <ErrorBanner
            type="error"
            title="Service Notice"
            message={error}
            onDismiss={() => {}}
          />
        )}

        {/* Clarification Modal */}
        {needsClarification && clarificationQuestion && (
          <ClarificationModal
            isOpen={needsClarification}
            question={clarificationQuestion}
            onSubmit={handleClarificationSubmit}
            isLoading={isLoading}
          />
        )}

        {!plan ? (
          <div className="space-y-10">
            {/* Hero Section */}
            <div className="text-center max-w-2xl mx-auto space-y-3.5">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-zinc-100 tracking-tight leading-tight">
                Plan Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300">Perfect Saturday</span>
              </h1>

              <p className="text-zinc-400 text-sm sm:text-base leading-relaxed max-w-xl mx-auto">
                Tell us what your Saturday looks like. We&apos;ll turn it into a realistic plan you&apos;ll actually enjoy.
              </p>

              {/* Minimal feature badges */}
              <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs text-zinc-400">
                <span className="flex items-center space-x-1.5 bg-zinc-900/60 px-3 py-1 rounded-full border border-zinc-800/80">
                  <ShieldCheck className="w-3 h-3 text-emerald-400" />
                  <span>Constraint Validation</span>
                </span>
                <span className="flex items-center space-x-1.5 bg-zinc-900/60 px-3 py-1 rounded-full border border-zinc-800/80">
                  <Compass className="w-3 h-3 text-zinc-400" />
                  <span>Travel Buffers</span>
                </span>
                <span className="flex items-center space-x-1.5 bg-zinc-900/60 px-3 py-1 rounded-full border border-zinc-800/80">
                  <Zap className="w-3 h-3 text-zinc-400" />
                  <span>Deterministic Fallbacks</span>
                </span>
              </div>
            </div>

            {/* Input Form */}
            <div className="max-w-2xl mx-auto">
              <PlannerForm onSubmit={handleCreatePlan} isLoading={isLoading} />
            </div>

            {/* In-Flight Agent Trace HUD */}
            {isLoading && trace.length > 0 && (
              <div className="max-w-2xl mx-auto mt-6">
                <AgentTraceView trace={trace} isLoading={isLoading} />
              </div>
            )}
          </div>
        ) : (
          <PlanResult
            plan={plan}
            trace={trace}
            onReset={resetPlan}
            isLoading={isLoading}
          />
        )}
      </main>

      {/* Minimal Footer */}
      <footer className="border-t border-zinc-800/60 bg-[#07080c] py-6 px-4 sm:px-6 mt-16 text-center text-xs text-zinc-500 space-y-2">
        <div className="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-2 text-zinc-400">
            <span>Perfect Saturday Planner</span>
            <span>•</span>
            <span>AI Engineer Assignment</span>
          </div>

          <div className="text-[11px] text-zinc-500">
            Bangalore Seed Dataset Active
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
