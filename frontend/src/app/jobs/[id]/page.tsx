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
              className="text-blue-600 hover:text-blue-700 flex items-center gap-2"
            >
              ← Back to jobs
            </Link>
          </nav>

          {/* Job Header */}
          <div className="bg-white rounded-lg shadow-sm p-8 mb-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h1 className="text-4xl font-bold text-gray-900 mb-2" data-testid="job-title">
                  {job.title}
                </h1>
                {job.company && (
                  <Link
                    href={`/companies/${job.company.id}`}
                    className="text-xl text-gray-600 hover:text-blue-600 flex items-center gap-2"
                    data-testid="company-name"
                  >
                    <Building2 className="w-5 h-5" />
                    {job.company.name}
                  </Link>
                )}
              </div>
              <Badge className="text-sm" data-testid="job-level">
                {job.level}
              </Badge>
            </div>

            <div className="flex flex-wrap gap-4 text-gray-600 mb-6">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                <span>{job.location}</span>
              </div>
              {formattedSalary && (
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4" />
                  <span>{formattedSalary}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>Posted {new Date(job.created_at).toLocaleDateString()}</span>
              </div>
            </div>

            <Button 
              className="w-full sm:w-auto" 
              size="lg"
              data-testid="apply-button"
            >
              Apply Now
            </Button>
          </div>

          {/* Job Description */}
          <div className="bg-white rounded-lg shadow-sm p-8 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Job Description</h2>
            <div 
              className="prose max-w-none text-gray-600"
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
            <div className="bg-white rounded-lg shadow-sm p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">About the Company</h2>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {job.company.name}
              </h3>
              {job.company.description && (
                <p className="text-gray-600 mb-4">
                  {job.company.description}
                </p>
              )}
              {job.company.website && (
                <a
                  href={job.company.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700"
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
