import React, { useState } from 'react';
import { HelpCircle, ArrowRight } from 'lucide-react';

interface ClarificationModalProps {
  question: string;
  isOpen: boolean;
  onSubmit: (clarification: string) => void;
  isLoading: boolean;
}

export const ClarificationModal: React.FC<ClarificationModalProps> = ({
  question,
  isOpen,
  onSubmit,
  isLoading,
}) => {
  const [answer, setAnswer] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (answer.trim()) {
      onSubmit(answer.trim());
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-md minimal-card rounded-2xl p-6 border border-zinc-700/60 shadow-2xl space-y-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-zinc-800 text-zinc-300 flex items-center justify-center">
            <HelpCircle className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-100">Clarification Needed</h3>
            <p className="text-xs text-zinc-400">A few quick details to refine the plan</p>
          </div>
        </div>

        <div className="bg-zinc-900/80 rounded-xl p-3.5 border border-zinc-800 text-xs text-zinc-300 font-medium">
          {question}
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="e.g. In Bangalore with budget ₹2000, looking for live acoustic music..."
            rows={3}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl p-3 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-zinc-500 transition-colors"
            autoFocus
          />

          <div className="flex justify-end space-x-2">
            <button
              type="submit"
              disabled={isLoading || !answer.trim()}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-zinc-100 hover:bg-white text-zinc-950 font-medium text-xs transition-all disabled:opacity-50 cursor-pointer"
            >
              {isLoading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-zinc-950 border-t-transparent rounded-full animate-spin"></div>
                  <span>Updating...</span>
                </>
              ) : (
                <>
                  <span>Submit</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
