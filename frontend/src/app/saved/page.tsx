'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Bookmark, Briefcase } from 'lucide-react';
import { getSavedJobs } from '@/lib/api';
import { SavedJob } from '@/lib/types';
import { useAuth } from '@/hooks/useAuth';
import JobCard from '@/components/JobCard';

export default function SavedJobsPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [savedJobs, setSavedJobs] = useState<SavedJob[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login?redirect=/saved');
      return;
    }

    if (isAuthenticated) {
      loadSavedJobs();
    }
  }, [isAuthenticated, authLoading, router]);

  const loadSavedJobs = async () => {
    try {
      setIsLoading(true);
      const jobs = await getSavedJobs();
      setSavedJobs(jobs);
    } catch (err) {
      setError('Failed to load saved jobs');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen">
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">Saved Roles</h1>
            <p className="text-lg text-muted-foreground">
              Your bookmarked opportunities
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div 
                key={i} 
                className="bg-card border border-muted rounded-2xl p-6 animate-pulse"
              >
                <div className="h-6 bg-muted rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-muted rounded w-1/2 mb-4"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-muted rounded w-1/3"></div>
                  <div className="h-4 bg-muted rounded w-1/4"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center py-12">
            <p className="text-red-500">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Bookmark className="w-8 h-8 text-primary" />
            <h1 className="text-4xl font-bold">Saved Roles</h1>
          </div>
          <p className="text-lg text-muted-foreground">
            {savedJobs.length} {savedJobs.length === 1 ? 'role' : 'roles'} bookmarked
          </p>
        </div>

        {/* Jobs Grid */}
        {savedJobs.length === 0 ? (
          <div className="text-center py-12">
            <Briefcase className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">No saved roles yet</h3>
            <p className="text-muted-foreground mb-6">
              Start bookmarking roles you're interested in
            </p>
            <a
              href="/jobs"
              className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-6 py-3 rounded-xl font-semibold hover:bg-primary/90 transition-all"
            >
              Browse Roles
            </a>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {savedJobs.map((savedJob) => (
              <JobCard key={savedJob.job_id} job={savedJob.job} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
