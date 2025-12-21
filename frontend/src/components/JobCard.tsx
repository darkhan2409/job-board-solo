import Link from 'next/link';
import { Job } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { formatSalary } from '@/lib/salary-utils';

interface JobCardProps {
  job: Job;
}

export default function JobCard({ job }: JobCardProps) {
  const formattedSalary = formatSalary(job.salary);

  return (
    <Link
      href={`/jobs/${job.id}`}
      className="block bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6 border border-gray-200"
      data-testid="job-card"
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-1">
            {job.title}
          </h3>
          <p className="text-gray-600 font-medium">
            {job.company?.name || 'Company'}
          </p>
        </div>
        <Badge variant="secondary" className="ml-4">
          {job.level}
        </Badge>
      </div>

      <p className="text-gray-600 mb-4 line-clamp-2">
        {job.description}
      </p>

      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
        <span className="flex items-center gap-1">
          📍 {job.location}
        </span>
        {formattedSalary && (
          <span className="flex items-center gap-1">
            💰 {formattedSalary}
          </span>
        )}
        <span className="text-gray-400">
          {new Date(job.created_at).toLocaleDateString()}
        </span>
      </div>
    </Link>
  );
}
