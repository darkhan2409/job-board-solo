import Link from 'next/link';
import { Job } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { formatSalary } from '@/lib/salary-utils';
import { MapPin, DollarSign, Calendar, Building2, ExternalLink } from 'lucide-react';
import SaveJobButton from './SaveJobButton';

interface JobCardProps {
  job: Job;
}

const getLevelColor = (level: string) => {
  switch (level.toLowerCase()) {
    case 'junior':
      return 'bg-secondary/10 text-secondary border-secondary/20';
    case 'middle':
      return 'bg-primary/10 text-primary border-primary/20';
    case 'senior':
      return 'bg-accent/10 text-accent border-accent/20';
    case 'lead':
      return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
    default:
      return 'bg-muted text-muted-foreground border-muted';
  }
};

export default function JobCard({ job }: JobCardProps) {
  const formattedSalary = formatSalary(job.salary);

  return (
    <Link
      href={`/jobs/${job.id}`}
      className="block bg-card border border-muted rounded-2xl p-6 card-hover group"
      data-testid="job-card"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">
            {job.title}
          </h3>
          <div className="flex items-center gap-2 text-muted-foreground text-sm">
            <Building2 className="w-4 h-4" />
            <span className="font-medium">{job.company?.name || 'Company'}</span>
          </div>
        </div>
        <div className="flex items-center gap-2 ml-4">
          <Badge className={`border font-semibold uppercase text-xs tracking-wide ${getLevelColor(job.level)}`}>
            {job.level}
          </Badge>
          <SaveJobButton jobId={job.id} variant="card" />
        </div>
      </div>

      {/* Description */}
      <p className="text-muted-foreground mb-4 line-clamp-2 leading-relaxed text-sm">
        {job.description}
      </p>

      {/* Footer - Salary is the main anchor */}
      <div className="flex items-center justify-between pt-4 border-t border-muted">
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <MapPin className="w-4 h-4" />
            {job.location}
          </span>
          <span className="flex items-center gap-1.5 text-muted-foreground/60">
            <Calendar className="w-4 h-4" />
            {new Date(job.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
          </span>
        </div>
        {formattedSalary && (
          <div className="flex items-center gap-1.5 font-bold text-primary mono">
            <DollarSign className="w-4 h-4" />
            {formattedSalary}
          </div>
        )}
      </div>

      {/* Hover indicator */}
      <div className="mt-4 flex items-center gap-2 text-primary opacity-0 group-hover:opacity-100 transition-opacity">
        <span className="text-sm font-semibold">View details</span>
        <ExternalLink className="w-4 h-4" />
      </div>
    </Link>
  );
}
