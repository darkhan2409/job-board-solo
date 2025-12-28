import { fetchJobById } from '@/lib/api';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { MapPin, DollarSign, Calendar, Building2 } from 'lucide-react';
import { formatSalary } from '@/lib/salary-utils';

interface JobDetailPageProps {
  params: {
    id: string;
  };
}

export default async function JobDetailPage({ params }: JobDetailPageProps) {
  try {
    const job = await fetchJobById(parseInt(params.id));
    const formattedSalary = formatSalary(job.salary);

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Breadcrumb */}
          <nav className="mb-8" data-testid="breadcrumb">
            <Link
              href="/jobs"
              className="text-primary hover:text-primary/80 flex items-center gap-2 font-medium transition-colors"
            >
              ← Back to jobs
            </Link>
          </nav>

          {/* Job Header */}
          <div className="bg-white rounded-xl shadow-lg p-8 mb-6 border">
            <div className="flex justify-between items-start mb-6">
              <div className="flex-1">
                <h1 className="text-4xl font-bold text-gray-900 mb-3" data-testid="job-title">
                  {job.title}
                </h1>
                {job.company && (
                  <Link
                    href={`/companies/${job.company.id}`}
                    className="text-xl text-gray-600 hover:text-primary flex items-center gap-2 font-medium transition-colors"
                    data-testid="company-name"
                  >
                    <Building2 className="w-5 h-5 text-primary" />
                    {job.company.name}
                  </Link>
                )}
              </div>
              <Badge 
                className={`text-sm font-semibold border ${
                  job.level.toLowerCase() === 'junior' ? 'bg-green-100 text-green-700 border-green-200' :
                  job.level.toLowerCase() === 'middle' ? 'bg-blue-100 text-blue-700 border-blue-200' :
                  job.level.toLowerCase() === 'senior' ? 'bg-primary/10 text-primary border-primary/20' :
                  'bg-accent/10 text-accent border-accent/20'
                }`}
                data-testid="job-level"
              >
                {job.level}
              </Badge>
            </div>

            <div className="flex flex-wrap gap-6 text-gray-600 mb-8 pb-6 border-b">
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5 text-secondary" />
                <span className="font-medium">{job.location}</span>
              </div>
              {formattedSalary && (
                <div className="flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-accent" />
                  <span className="font-semibold text-accent">{formattedSalary}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-gray-400" />
                <span>Posted {new Date(job.created_at).toLocaleDateString()}</span>
              </div>
            </div>

            <Button 
              className="w-full sm:w-auto btn-primary px-8 py-6 text-lg" 
              size="lg"
              data-testid="apply-button"
            >
              Apply for this position
            </Button>
          </div>

          {/* Job Description */}
          <div className="bg-white rounded-xl shadow-lg p-8 mb-6 border">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <div className="w-1 h-8 bg-primary rounded"></div>
              Job Description
            </h2>
            <div 
              className="prose max-w-none text-gray-600 leading-relaxed"
              data-testid="job-description"
            >
              {job.description.split('\n').map((paragraph, index) => (
                <p key={index} className="mb-4">
                  {paragraph}
                </p>
              ))}
            </div>
          </div>

          {/* About the Company */}
          {job.company && (
            <div className="bg-white rounded-xl shadow-lg p-8 border">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <div className="w-1 h-8 bg-secondary rounded"></div>
                About the Company
              </h2>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                {job.company.name}
              </h3>
              {job.company.description && (
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {job.company.description}
                </p>
              )}
              {job.company.website && (
                <a
                  href={job.company.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-primary hover:text-primary/80 font-semibold transition-colors"
                >
                  Visit company website →
                </a>
              )}
            </div>
          )}
        </div>
      </div>
    );
  } catch (error) {
    notFound();
  }
}
