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
      return <Utensils className="w-3.5 h-3.5 text-emerald-400" />;
    }
    if (t.includes('music')) {
      return <Music className="w-3.5 h-3.5 text-pink-400" />;
    }
    if (t.includes('walk') || t.includes('nature') || t.includes('park')) {
      return <Footprints className="w-3.5 h-3.5 text-teal-400" />;
    }
    if (t.includes('art') || t.includes('workshop')) {
      return <Palette className="w-3.5 h-3.5 text-amber-400" />;
    }
    if (t.includes('book')) {
      return <BookOpen className="w-3.5 h-3.5 text-blue-400" />;
    }
    if (t.includes('movie') || t.includes('cinema')) {
      return <Film className="w-3.5 h-3.5 text-purple-400" />;
    }
    return <Compass className="w-3.5 h-3.5 text-zinc-400" />;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80">
        <div>
          <h3 className="text-sm font-semibold text-zinc-100">Schedule & Timeline</h3>
          <p className="text-xs text-zinc-400">Sequential Saturday itinerary</p>
        </div>
        <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-400">
          {timeline.length} Stops
        </span>
      </div>

      {/* Timeline List */}
      <div className="space-y-6 relative before:absolute before:left-3.5 before:top-4 before:bottom-4 before:w-px before:bg-zinc-800">
        {timeline.map((item, index) => (
          <div key={index} className="relative pl-9 group animate-fade-in">
            {/* Timeline Dot Icon */}
            <div className="absolute left-1.5 top-3.5 -translate-x-1/2 w-6 h-6 rounded-full bg-zinc-900 border border-zinc-700 flex items-center justify-center group-hover:border-zinc-500 transition-colors">
              {getCategoryIcon(item.type)}
            </div>

            {/* Event Card */}
            <div className="minimal-card minimal-card-hover rounded-2xl p-5 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-mono font-medium px-2 py-0.5 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-300">
                    {item.start} – {item.end}
                  </span>
                  <span className="text-[10px] uppercase font-semibold text-zinc-400 bg-zinc-900/60 px-2 py-0.5 rounded">
                    {item.type}
                  </span>
                </div>

                <div>
                  {item.cost === 0 ? (
                    <span className="text-xs font-medium px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      Free
                    </span>
                  ) : (
                    <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded-md bg-zinc-900 text-zinc-200 border border-zinc-800">
                      ₹{item.cost.toFixed(0)}
                    </span>
                  )}
                </div>
              </div>

              {/* Venue Name */}
              <h4 className="text-base font-semibold text-zinc-100">
                {item.name}
              </h4>

              {/* Area & Crowd Tags */}
              {item.area && (
                <div className="flex flex-wrap items-center gap-3 text-xs text-zinc-400">
                  <span className="flex items-center space-x-1">
                    <MapPin className="w-3 h-3 text-zinc-500" />
                    <span>{item.area}</span>
                  </span>
                  {item.crowd_level && (
                    <span className="flex items-center space-x-1">
                      <Users className="w-3 h-3 text-zinc-500" />
                      <span className="capitalize">{item.crowd_level} crowd</span>
                    </span>
                  )}
                </div>
              )}

              {/* Why callout */}
              <div className="bg-zinc-900/60 rounded-xl p-3 border border-zinc-850">
                <p className="text-xs text-zinc-300 leading-relaxed">
                  <span className="font-medium text-zinc-200">Why this fits: </span>
                  {item.why}
                </p>
              </div>
            </div>

            {/* Transit Buffer */}
            {index < timeline.length - 1 && (
              <div className="py-2.5 flex items-center space-x-2 text-xs text-zinc-500 pl-2">
                <Car className="w-3.5 h-3.5 text-zinc-500" />
                <span className="font-mono text-[11px]">~20 min travel buffer</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
