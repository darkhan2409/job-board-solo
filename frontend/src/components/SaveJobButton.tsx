'use client';

import { useState, useEffect } from 'react';
import { Bookmark } from 'lucide-react';
import { saveJob, unsaveJob, checkJobSaved } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth';
import { toast } from 'sonner';

interface SaveJobButtonProps {
  jobId: number;
  variant?: 'card' | 'detail';
}

export default function SaveJobButton({ jobId, variant = 'card' }: SaveJobButtonProps) {
  const { user, isAuthenticated } = useAuth();
  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      checkJobSaved(jobId).then(setIsSaved).catch(() => setIsSaved(false));
    }
  }, [jobId, isAuthenticated]);

  const handleToggleSave = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!isAuthenticated) {
      toast.error('Please login to save jobs');
      setTimeout(() => {
        window.location.href = '/login?redirect=/jobs';
      }, 1000);
      return;
    }

    setIsLoading(true);
    try {
      if (isSaved) {
        await unsaveJob(jobId);
        setIsSaved(false);
        toast.success('Removed from saved jobs');
      } else {
        await saveJob(jobId);
        setIsSaved(true);
        toast.success('Job saved successfully');
      }
    } catch (error) {
      console.error('Failed to toggle save:', error);
      
      // More detailed error handling
      if (error instanceof Error) {
        if (error.message.includes('401') || error.message.includes('Unauthorized')) {
          toast.error('Please login to save jobs');
          setTimeout(() => {
            window.location.href = '/login?redirect=/jobs';
          }, 1000);
        } else if (error.message.includes('already saved')) {
          toast.info('Job is already saved');
          setIsSaved(true);
        } else {
          toast.error(error.message || 'Failed to save job. Please try again.');
        }
      } else {
        toast.error('Failed to save job. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (variant === 'detail') {
    return (
      <button
        onClick={handleToggleSave}
        disabled={isLoading}
        className={`inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all border ${
          isSaved
            ? 'bg-primary/10 text-primary border-primary/20 hover:bg-primary/20'
            : 'bg-card text-muted-foreground border-muted hover:border-primary/50'
        } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <Bookmark className={`w-5 h-5 ${isSaved ? 'fill-current' : ''}`} />
        {isSaved ? 'Saved' : 'Save for later'}
      </button>
    );
  }

  return (
    <button
      onClick={handleToggleSave}
      disabled={isLoading}
      className={`p-2 rounded-lg transition-all ${
        isSaved
          ? 'bg-primary/10 text-primary hover:bg-primary/20'
          : 'bg-card hover:bg-muted text-muted-foreground hover:text-primary'
      } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
      title={isSaved ? 'Remove from saved' : 'Save for later'}
    >
      <Bookmark className={`w-5 h-5 ${isSaved ? 'fill-current' : ''}`} />
    </button>
  );
}
