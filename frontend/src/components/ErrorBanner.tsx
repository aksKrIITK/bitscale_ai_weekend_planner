import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle, Info } from 'lucide-react';

interface ErrorBannerProps {
  type?: 'error' | 'warning' | 'info' | 'fallback';
  title?: string;
  message: string;
  onDismiss?: () => void;
}

export const ErrorBanner: React.FC<ErrorBannerProps> = ({
  type = 'error',
  title,
  message,
  onDismiss,
}) => {
  const styles = {
    error: 'bg-red-500/10 border-red-500/20 text-red-300',
    warning: 'bg-amber-500/10 border-amber-500/20 text-amber-300',
    info: 'bg-blue-500/10 border-blue-500/20 text-blue-300',
    fallback: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300',
  };

  const icons = {
    error: <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />,
    warning: <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />,
    info: <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />,
    fallback: <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />,
  };

  return (
    <div className={`p-4 rounded-xl border flex items-start space-x-3 mb-6 animate-fade-in ${styles[type]}`}>
      {icons[type]}
      <div className="flex-1 min-w-0">
        {title && <h4 className="font-medium text-xs mb-0.5">{title}</h4>}
        <p className="text-xs opacity-90 leading-relaxed">{message}</p>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-xs opacity-60 hover:opacity-100 transition-opacity ml-2 cursor-pointer"
        >
          ✕
        </button>
      )}
    </div>
  );
};
