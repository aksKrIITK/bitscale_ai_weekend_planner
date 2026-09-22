import React from 'react';
import {
  MapPin,
  Utensils,
  Music,
  Footprints,
  Palette,
  BookOpen,
  Film,
  Compass,
  Users,
  Car
} from 'lucide-react';
import { TimelineItem } from '../types/planner';

interface TimelineViewProps {
  timeline: TimelineItem[];
}

export const TimelineView: React.FC<TimelineViewProps> = ({ timeline }) => {
  const getCategoryIcon = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes('food') || t.includes('dining') || t.includes('cafe')) {
      return <Utensils className="w-4 h-4 text-emerald-400" />;
    }
    if (t.includes('music')) {
      return <Music className="w-4 h-4 text-pink-400" />;
    }
    if (t.includes('walk') || t.includes('nature') || t.includes('park')) {
      return <Footprints className="w-4 h-4 text-teal-400" />;
    }
    if (t.includes('art') || t.includes('workshop')) {
      return <Palette className="w-4 h-4 text-amber-400" />;
    }
    if (t.includes('book')) {
      return <BookOpen className="w-4 h-4 text-blue-400" />;
    }
    if (t.includes('movie') || t.includes('cinema')) {
      return <Film className="w-4 h-4 text-purple-400" />;
    }
    return <Compass className="w-4 h-4 text-cyan-400" />;
  };

  return (
    <div className="space-y-6">
      {/* Schedule Header */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight">Your Saturday Schedule</h3>
          <p className="text-xs text-zinc-400">Sequential itinerary with 20m transit buffers</p>
        </div>
        <span className="text-xs font-mono font-bold px-3 py-1 rounded-full bg-zinc-900 border border-zinc-700 text-zinc-200">
          {timeline.length} Stops Planned
        </span>
      </div>

      {/* Timeline Thread */}
      <div className="space-y-6 relative before:absolute before:left-5 before:top-4 before:bottom-4 before:w-0.5 before:bg-gradient-to-b before:from-emerald-500 before:via-teal-400 before:to-zinc-800">
        {timeline.map((item, index) => (
          <div key={index} className="relative pl-12 group animate-fade-in">
            {/* Centered Timeline Dot Icon */}
            <div className="absolute left-5 top-5 -translate-x-1/2 w-8 h-8 rounded-xl bg-[#0c101a] border-2 border-zinc-600 flex items-center justify-center shadow-lg group-hover:border-emerald-400 transition-colors z-10">
              {getCategoryIcon(item.type)}
            </div>

            {/* High Readability Event Card */}
            <div className="card-premium rounded-2xl p-5 sm:p-6 space-y-3.5 card-premium-hover">
              {/* Header: Time & Price Badges */}
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-lg bg-zinc-800 border border-zinc-600 text-zinc-100">
                    {item.start} – {item.end}
                  </span>
                  <span className="text-[10px] uppercase font-bold text-zinc-300 bg-zinc-800/90 px-2 py-0.5 rounded border border-zinc-700">
                    {item.type}
                  </span>
                </div>

                <div>
                  {item.cost === 0 ? (
                    <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                      Free Entry
                    </span>
                  ) : (
                    <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-lg bg-zinc-800 text-emerald-400 border border-zinc-600">
                      ₹{item.cost.toFixed(0)}
                    </span>
                  )}
                </div>
              </div>

              {/* Venue Name */}
              <h4 className="text-base sm:text-lg font-bold text-white tracking-tight">
                {item.name}
              </h4>

              {/* Area & Crowd Tags */}
              {item.area && (
                <div className="flex flex-wrap items-center gap-2.5 text-xs text-zinc-300">
                  <span className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-[#0b0e17] border border-zinc-750 font-medium">
                    <MapPin className="w-3.5 h-3.5 text-cyan-400" />
                    <span>{item.area}</span>
                  </span>
                  {item.crowd_level && (
                    <span className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-[#0b0e17] border border-zinc-750 font-medium">
                      <Users className="w-3.5 h-3.5 text-zinc-400" />
                      <span className="capitalize">{item.crowd_level} crowd</span>
                    </span>
                  )}
                </div>
              )}

              {/* Clear "Why Chosen" Callout Box */}
              <div className="bg-[#0b0e17] rounded-xl p-3.5 border-l-3 border-emerald-400 border-y border-r border-zinc-800/80">
                <p className="text-xs text-zinc-200 leading-relaxed font-normal">
                  <span className="font-bold text-emerald-400">Why this was chosen: </span>
                  {item.why}
                </p>
              </div>
            </div>

            {/* Travel Buffer Indicator */}
            {index < timeline.length - 1 && (
              <div className="py-2.5 flex items-center space-x-2 text-xs text-zinc-400 pl-2">
                <Car className="w-3.5 h-3.5 text-zinc-400" />
                <span className="font-mono text-[11px] text-zinc-400 font-medium">
                  ~20 min transit buffer between stops
                </span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
