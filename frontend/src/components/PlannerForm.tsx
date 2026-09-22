import React, { useState } from 'react';
import {
  MapPin,
  Wallet,
  Clock,
  Sparkles,
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
  const [city, setCity] = useState('Bangalore');
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
      <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-2xl bg-zinc-900/60 border border-zinc-800/80 backdrop-blur-md">
        <div className="flex items-center space-x-2 text-xs text-zinc-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>Looking to test the default evaluation scenario?</span>
        </div>
        <button
          type="button"
          onClick={loadDemoScenario}
          className="px-3 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700/80 text-xs font-medium transition-all flex items-center space-x-1.5 cursor-pointer"
        >
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>Load Demo Scenario</span>
        </button>
      </div>

      {/* Main Form Card */}
      <div className="minimal-card rounded-2xl p-6 sm:p-8 space-y-7">
        {/* City & Budget */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* City */}
          <div className="space-y-2">
            <label className="text-xs font-medium text-zinc-300 flex items-center space-x-1.5">
              <MapPin className="w-3.5 h-3.5 text-zinc-400" />
              <span>City</span>
            </label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="e.g. Bangalore"
              required
              className="w-full bg-zinc-900/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 transition-all font-medium"
            />
          </div>

          {/* Budget */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs font-medium text-zinc-300 flex items-center space-x-1.5">
                <Wallet className="w-3.5 h-3.5 text-zinc-400" />
                <span>Budget (INR)</span>
              </label>
              <span className="text-xs font-mono text-zinc-400">
                ₹{budget.toLocaleString()}
              </span>
            </div>
            <div className="space-y-2">
              <div className="relative">
                <span className="absolute left-3.5 top-2.5 text-zinc-500 text-sm">₹</span>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  placeholder="2000"
                  min="100"
                  required
                  className="w-full bg-zinc-900/80 border border-zinc-800 rounded-xl pl-8 pr-4 py-2.5 text-sm text-zinc-100 font-mono placeholder-zinc-500 focus:outline-none focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 transition-all"
                />
              </div>

              {/* Quick Budget Chips */}
              <div className="flex flex-wrap gap-1.5">
                {BUDGET_PRESETS.map((val) => (
                  <button
                    key={val}
                    type="button"
                    onClick={() => setBudget(val)}
                    className={`interactive-chip text-xs px-2.5 py-1 rounded-lg font-mono transition-all cursor-pointer ${
                      budget === val
                        ? 'bg-zinc-200 text-zinc-950 font-semibold'
                        : 'bg-zinc-900 text-zinc-400 hover:text-zinc-200 border border-zinc-800'
                    }`}
                  >
                    ₹{val.toLocaleString()}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Available Time */}
        <div className="space-y-2.5">
          <label className="text-xs font-medium text-zinc-300 flex items-center space-x-1.5">
            <Clock className="w-3.5 h-3.5 text-zinc-400" />
            <span>Available Time</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {TIME_OPTIONS.map((timeOption) => {
              const isSelected = availableTime === timeOption;
              return (
                <button
                  key={timeOption}
                  type="button"
                  onClick={() => setAvailableTime(timeOption)}
                  className={`interactive-chip px-3.5 py-2 rounded-xl text-xs font-medium transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-zinc-100 text-zinc-950 font-semibold shadow-sm'
                      : 'bg-zinc-900/80 text-zinc-400 hover:text-zinc-200 border border-zinc-800'
                  }`}
                >
                  {timeOption}
                </button>
              );
            })}
          </div>
        </div>

        {/* Mood */}
        <div className="space-y-2.5">
          <label className="text-xs font-medium text-zinc-300">
            <span>Mood / Vibe</span>
          </label>
          <input
            type="text"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            placeholder="e.g. tired but wants to do something fun"
            className="w-full bg-zinc-900/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-zinc-500 focus:ring-1 focus:ring-zinc-500 transition-all font-medium mb-2"
          />

          <div className="flex flex-wrap gap-1.5">
            {MOOD_PRESETS.map((preset) => (
              <button
                key={preset}
                type="button"
                onClick={() => setMood(preset)}
                className={`interactive-chip text-xs px-3 py-1 rounded-lg transition-all cursor-pointer ${
                  mood === preset
                    ? 'bg-zinc-200 text-zinc-950 font-medium'
                    : 'bg-zinc-900 text-zinc-400 hover:text-zinc-200 border border-zinc-800'
                }`}
              >
                {preset}
              </button>
            ))}
          </div>
        </div>

        {/* Interests */}
        <div className="space-y-2.5">
          <label className="text-xs font-medium text-zinc-300">
            <span>Interests</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {INTERESTS_LIST.map((interest) => {
              const isSelected = interests.includes(interest.toLowerCase());
              return (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`interactive-chip flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer border ${
                    isSelected
                      ? 'bg-zinc-100 text-zinc-950 border-zinc-200 font-semibold'
                      : 'bg-zinc-900/80 text-zinc-400 border-zinc-800 hover:text-zinc-200 hover:border-zinc-700'
                  }`}
                >
                  {isSelected && <Check className="w-3 h-3 stroke-[3]" />}
                  <span>{interest}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Constraints */}
        <div className="space-y-2.5">
          <label className="text-xs font-medium text-zinc-300">
            <span>Constraints & Preferences</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {CONSTRAINTS_LIST.map((constraint) => {
              const isSelected = constraints.includes(constraint.toLowerCase());
              return (
                <button
                  key={constraint}
                  type="button"
                  onClick={() => toggleConstraint(constraint)}
                  className={`interactive-chip flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all cursor-pointer border ${
                    isSelected
                      ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30 font-semibold'
                      : 'bg-zinc-900/80 text-zinc-400 border-zinc-800 hover:text-zinc-200 hover:border-zinc-700'
                  }`}
                >
                  {isSelected && <Check className="w-3 h-3 text-emerald-400 stroke-[3]" />}
                  <span>{constraint}</span>
                </button>
              );
            })}
          </div>

          {/* Custom constraint input */}
          <div className="flex items-center space-x-2 pt-1">
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
              placeholder="Add custom constraint..."
              className="flex-1 bg-zinc-900/80 border border-zinc-800 rounded-xl px-3.5 py-2 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-500"
            />
            <button
              type="button"
              onClick={addCustomConstraint}
              className="px-3.5 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium transition-all flex items-center space-x-1 cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add</span>
            </button>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-3 border-t border-zinc-800/80">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 rounded-xl bg-zinc-100 hover:bg-white text-zinc-950 font-semibold text-sm transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center space-x-2 disabled:opacity-50 cursor-pointer"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-zinc-950 border-t-transparent rounded-full animate-spin"></div>
                <span>Building Itinerary...</span>
              </>
            ) : (
              <>
                <span>Plan My Saturday</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
};
