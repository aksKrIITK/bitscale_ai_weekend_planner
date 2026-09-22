import React, { useState } from 'react';
import {
  MapPin,
  Wallet,
  Clock,
  Play,
  Plus,
  Check,
  ArrowRight
} from 'lucide-react';
import { PlanRequest } from '../types/planner';

interface PlannerFormProps {
  onSubmit: (formData: PlanRequest) => void;
  isLoading: boolean;
}

const INTERESTS_LIST = [
  'Food',
  'Music',
  'Walks',
  'Movies',
  'Art',
  'Nature',
  'Shopping',
  'Coffee',
  'Books',
  'Sports',
  'Photography',
];

const MOOD_PRESETS = [
  'tired but wants to do something fun',
  'adventurous',
  'relaxed',
  'social',
  'creative',
  'romantic',
  'outdoorsy'
];

const CONSTRAINTS_LIST = [
  'Vegetarian',
  'Avoid crowded places',
  'Avoid alcohol',
  'Indoor only',
  'Outdoor only',
  'No long travel',
  'Wheelchair accessible',
  'Family friendly',
];

const TIME_OPTIONS = ['2 hours', '4 hours', '6 hours', '8 hours'];
const BUDGET_PRESETS = [1000, 2000, 3500, 5000];

export const PlannerForm: React.FC<PlannerFormProps> = ({ onSubmit, isLoading }) => {
  const [city, setCity] = useState('');
  const [budget, setBudget] = useState<number>(2000);
  const [availableTime, setAvailableTime] = useState('4 hours');
  const [mood, setMood] = useState('tired but wants to do something fun');
  const [interests, setInterests] = useState<string[]>(['food', 'music', 'walks']);
  const [constraints, setConstraints] = useState<string[]>(['vegetarian', 'avoid crowded places']);
  const [customConstraint, setCustomConstraint] = useState('');

  const toggleInterest = (interest: string) => {
    const norm = interest.toLowerCase();
    setInterests((prev) =>
      prev.includes(norm) ? prev.filter((i) => i !== norm) : [...prev, norm]
    );
  };

  const toggleConstraint = (constraint: string) => {
    const norm = constraint.toLowerCase();
    setConstraints((prev) =>
      prev.includes(norm) ? prev.filter((c) => c !== norm) : [...prev, norm]
    );
  };

  const addCustomConstraint = () => {
    if (customConstraint.trim()) {
      const norm = customConstraint.trim().toLowerCase();
      if (!constraints.includes(norm)) {
        setConstraints((prev) => [...prev, norm]);
      }
      setCustomConstraint('');
    }
  };

  const loadDemoScenario = () => {
    setCity('Bangalore');
    setBudget(2000);
    setAvailableTime('4 hours');
    setMood('tired but wants to do something fun');
    setInterests(['food', 'music', 'walks']);
    setConstraints(['vegetarian', 'avoid crowded places']);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      city,
      budget: Number(budget) || 2000,
      available_time: availableTime,
      mood,
      interests,
      constraints,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 animate-fade-in">
      {/* 1-Click Demo Shortcut Banner */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-2xl bg-zinc-900/90 border border-zinc-700/80 shadow-sm backdrop-blur-md">
        <div className="flex items-center space-x-2.5 text-xs text-zinc-300">
          <span className="w-2 h-2 rounded-full bg-emerald-400 shrink-0"></span>
          <span className="font-medium">Quick Test: Fill standard evaluation demo parameters</span>
        </div>
        <button
          type="button"
          onClick={loadDemoScenario}
          className="px-3.5 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-100 border border-zinc-600/80 text-xs font-semibold transition-all flex items-center space-x-1.5 cursor-pointer shadow-sm"
        >
          <Play className="w-3 h-3 text-emerald-400 fill-emerald-400" />
          <span>Load Demo Scenario</span>
        </button>
      </div>

      {/* Main Form Card with Enhanced Readability & Contrast */}
      <div className="bg-[#11131c] rounded-2xl p-6 sm:p-8 space-y-7 border border-zinc-700/70 shadow-xl">
        {/* City & Budget Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* City Input */}
          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center space-x-1.5">
              <MapPin className="w-3.5 h-3.5 text-emerald-400" />
              <span>City / Location</span>
            </label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="e.g. Bangalore, Mumbai, Delhi, Tokyo..."
              required
              className="w-full bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition-all font-semibold"
            />
            <p className="text-[11px] text-zinc-400">Works for any city worldwide.</p>
          </div>

          {/* Budget Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center space-x-1.5">
                <Wallet className="w-3.5 h-3.5 text-emerald-400" />
                <span>Budget Limit (INR)</span>
              </label>
              <span className="text-xs font-mono font-bold text-emerald-400">
                ₹{budget.toLocaleString()} Max
              </span>
            </div>
            <div className="space-y-2.5">
              <div className="relative">
                <span className="absolute left-4 top-3 text-zinc-400 font-bold text-sm">₹</span>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  placeholder="2000"
                  min="100"
                  required
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-xl pl-8 pr-4 py-3 text-sm text-zinc-100 font-mono font-bold placeholder-zinc-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition-all"
                />
              </div>

              {/* Quick Budget Chips */}
              <div className="flex flex-wrap gap-2">
                {BUDGET_PRESETS.map((val) => (
                  <button
                    key={val}
                    type="button"
                    onClick={() => setBudget(val)}
                    className={`text-xs px-3 py-1.5 rounded-lg font-mono transition-all cursor-pointer border ${
                      budget === val
                        ? 'bg-zinc-100 text-zinc-950 font-bold border-zinc-100 shadow-sm'
                        : 'bg-zinc-900 text-zinc-300 hover:text-white border-zinc-700/80 hover:border-zinc-600'
                    }`}
                  >
                    ₹{val.toLocaleString()}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Available Time Section */}
        <div className="space-y-2.5 pt-2 border-t border-zinc-800">
          <label className="text-xs font-semibold uppercase tracking-wider text-zinc-300 flex items-center space-x-1.5">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>Available Time Window</span>
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            {TIME_OPTIONS.map((timeOption) => {
              const isSelected = availableTime === timeOption;
              return (
                <button
                  key={timeOption}
                  type="button"
                  onClick={() => setAvailableTime(timeOption)}
                  className={`px-4 py-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer border text-center ${
                    isSelected
                      ? 'bg-zinc-100 text-zinc-950 border-zinc-100 shadow-md font-bold'
                      : 'bg-zinc-900 text-zinc-300 hover:text-white border-zinc-700/80 hover:border-zinc-600'
                  }`}
                >
                  {timeOption}
                </button>
              );
            })}
          </div>
        </div>

        {/* Mood & Vibe Section */}
        <div className="space-y-2.5 pt-2 border-t border-zinc-800">
          <label className="text-xs font-semibold uppercase tracking-wider text-zinc-300">
            <span>Mood / Vibe</span>
          </label>
          <input
            type="text"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            placeholder="e.g. tired but wants to do something fun"
            className="w-full bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 transition-all font-medium mb-2.5"
          />

          <div className="flex flex-wrap gap-2">
            {MOOD_PRESETS.map((preset) => {
              const isSelected = mood === preset;
              return (
                <button
                  key={preset}
                  type="button"
                  onClick={() => setMood(preset)}
                  className={`text-xs px-3 py-1.5 rounded-xl transition-all cursor-pointer border ${
                    isSelected
                      ? 'bg-zinc-200 text-zinc-950 font-bold border-zinc-200 shadow-sm'
                      : 'bg-zinc-900 text-zinc-300 hover:text-white border-zinc-700/80 hover:border-zinc-600'
                  }`}
                >
                  {preset}
                </button>
              );
            })}
          </div>
        </div>

        {/* Interests Section */}
        <div className="space-y-2.5 pt-2 border-t border-zinc-800">
          <label className="text-xs font-semibold uppercase tracking-wider text-zinc-300">
            <span>Interests (Multi-select)</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {INTERESTS_LIST.map((interest) => {
              const isSelected = interests.includes(interest.toLowerCase());
              return (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer border ${
                    isSelected
                      ? 'bg-emerald-500 text-zinc-950 border-emerald-400 shadow-md font-bold'
                      : 'bg-zinc-900 text-zinc-300 border-zinc-700/80 hover:text-white hover:border-zinc-600'
                  }`}
                >
                  {isSelected && <Check className="w-3.5 h-3.5 stroke-[3]" />}
                  <span>{interest}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Constraints & Rules Section */}
        <div className="space-y-2.5 pt-2 border-t border-zinc-800">
          <label className="text-xs font-semibold uppercase tracking-wider text-zinc-300">
            <span>Constraints & Dietary Rules</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {CONSTRAINTS_LIST.map((constraint) => {
              const isSelected = constraints.includes(constraint.toLowerCase());
              return (
                <button
                  key={constraint}
                  type="button"
                  onClick={() => toggleConstraint(constraint)}
                  className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer border ${
                    isSelected
                      ? 'bg-indigo-500/25 text-indigo-200 border-indigo-400 font-bold shadow-sm'
                      : 'bg-zinc-900 text-zinc-300 border-zinc-700/80 hover:text-white hover:border-zinc-600'
                  }`}
                >
                  {isSelected && <Check className="w-3.5 h-3.5 text-indigo-300 stroke-[3]" />}
                  <span>{constraint}</span>
                </button>
              );
            })}
          </div>

          {/* Custom constraint input */}
          <div className="flex items-center space-x-2 pt-1.5">
            <input
              type="text"
              value={customConstraint}
              onChange={(e) => setCustomConstraint(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addCustomConstraint();
                }
              }}
              placeholder="Add custom constraint (e.g. pet friendly, near metro)..."
              className="flex-1 bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-400 font-medium"
            />
            <button
              type="button"
              onClick={addCustomConstraint}
              className="px-4 py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-100 text-xs font-bold transition-all flex items-center space-x-1 cursor-pointer border border-zinc-700"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add</span>
            </button>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4 border-t border-zinc-800">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-4 rounded-xl bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 hover:from-emerald-300 hover:to-cyan-300 text-zinc-950 font-extrabold text-sm transition-all duration-200 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2 disabled:opacity-50 cursor-pointer"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-zinc-950 border-t-transparent rounded-full animate-spin"></div>
                <span>LangGraph Agent Building Itinerary...</span>
              </>
            ) : (
              <>
                <span>Plan My Saturday</span>
                <ArrowRight className="w-4 h-4 stroke-[2.5]" />
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
};
