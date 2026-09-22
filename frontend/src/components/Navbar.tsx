import React from 'react';
import { Calendar, Compass } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-zinc-800/60 bg-[#090a0f]/80 backdrop-blur-xl">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-100 shadow-sm">
            <Calendar className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-sm text-zinc-100 tracking-tight font-sans">
                Saturday Planner
              </span>
              <span className="text-[10px] tracking-wide px-2 py-0.5 rounded-full bg-zinc-900 text-zinc-400 border border-zinc-800 font-medium">
                AI Powered
              </span>
            </div>
          </div>
        </div>

        {/* Status Pills */}
        <div className="flex items-center space-x-2 text-xs">
          <div className="hidden sm:flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-zinc-900/90 border border-zinc-800 text-zinc-400 text-[11px]">
            <Compass className="w-3 h-3 text-zinc-400" />
            <span>Bangalore</span>
          </div>

          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>LangGraph Agent</span>
          </div>
        </div>
      </div>
    </header>
  );
};
