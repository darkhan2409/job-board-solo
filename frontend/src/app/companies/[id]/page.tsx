import { fetchCompanyById } from '@/lib/api';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { formatSalary } from '@/lib/salary-utils';

interface CompanyDetailPageProps {
  params: {
    id: string;
  };
}

export default async function CompanyDetailPage({ params }: CompanyDetailPageProps) {
  try {
    const company = await fetchCompanyById(parseInt(params.id));

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Breadcrumb */}
          <nav className="mb-8">
            <Link
              href="/companies"
              className="text-blue-600 hover:text-blue-700 flex items-center gap-2"
            >
              ← Back to companies
            </Link>
          </nav>

          {/* Company Header */}
          <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              {company.name}
            </h1>
            <p className="text-lg text-gray-600 mb-6">
              {company.description}
            </p>
            {company.website && (
              <a
                href={company.website}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700"
              >
                Visit website →
              </a>
            )}
          </div>

          {/* Open Positions */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Open Positions at {company.name}
            </h2>

            {company.jobs && company.jobs.length > 0 ? (
              <div className="grid gap-4">
                {company.jobs.map((job) => {
                  const formattedSalary = formatSalary(job.salary);
                  return (
                    <Link
                      key={job.id}
                      href={`/jobs/${job.id}`}
                      className="group bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6 border border-gray-200"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">
                          {job.title}
                        </h3>
                        <span className="text-sm font-medium text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                          {job.level}
                        </span>
                      </div>
                      <p className="text-gray-600 mb-4 line-clamp-2">
                        {job.description}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>📍 {job.location}</span>
                        {formattedSalary && (
                          <span>💰 {formattedSalary}</span>
                        )}
                      </div>
                    </Link>
                  );
                })}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-sm p-8 text-center">
                <p className="text-gray-500">
                  No open positions at the moment
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  } catch (error) {
    notFound();
  }
}
