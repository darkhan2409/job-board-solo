import Link from 'next/link';
import { Job } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { formatSalary } from '@/lib/salary-utils';
import { MapPin, DollarSign, Calendar, Building2 } from 'lucide-react';

interface JobCardProps {
  job: Job;
}

const getLevelColor = (level: string) => {
  switch (level.toLowerCase()) {
    case 'junior':
      return 'bg-green-100 text-green-700 border-green-200';
    case 'middle':
      return 'bg-blue-100 text-blue-700 border-blue-200';
    case 'senior':
      return 'bg-primary/10 text-primary border-primary/20';
    case 'lead':
      return 'bg-accent/10 text-accent border-accent/20';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
};

export default function JobCard({ job }: JobCardProps) {
  const formattedSalary = formatSalary(job.salary);

  return (
    <Link
      href={`/jobs/${job.id}`}
      className="block bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 p-6 border border-gray-200 card-hover group"
      data-testid="job-card"
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary transition-colors">
            {job.title}
          </h3>
          <div className="flex items-center gap-2 text-gray-600 font-medium">
            <Building2 className="w-4 h-4 text-primary" />
            {job.company?.name || 'Company'}
          </div>
        </div>
        <Badge className={`ml-4 border font-semibold ${getLevelColor(job.level)}`}>
          {job.level}
        </Badge>
      </div>

      <p className="text-gray-600 mb-4 line-clamp-2 leading-relaxed">
        {job.description}
      </p>

      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 pt-4 border-t">
        <span className="flex items-center gap-1.5">
          <MapPin className="w-4 h-4 text-secondary" />
          {job.location}
        </span>
        {formattedSalary && (
          <span className="flex items-center gap-1.5 font-semibold text-accent">
            <DollarSign className="w-4 h-4" />
            {formattedSalary}
          </span>
        )}
        <span className="flex items-center gap-1.5 text-gray-400 ml-auto">
          <Calendar className="w-4 h-4" />
          {new Date(job.created_at).toLocaleDateString()}
        </span>
      </div>
    </Link>
  );
}
