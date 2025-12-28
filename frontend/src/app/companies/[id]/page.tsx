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
      <div className="min-h-screen bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Breadcrumb */}
          <nav className="mb-8">
            <Link
              href="/companies"
              className="text-primary hover:text-primary/80 flex items-center gap-2 transition-colors"
            >
              ← Back to companies
            </Link>
          </nav>

          {/* Company Header */}
          <div className="card-dark p-8 mb-8 border border-border/50">
            <h1 className="text-4xl font-bold text-white mb-4 font-heading">
              {company.name}
            </h1>
            <p className="text-lg text-gray-300 mb-6 leading-relaxed">
              {company.description}
            </p>
            {company.website && (
              <a
                href={company.website}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-primary hover:text-primary/80 transition-colors font-medium"
              >
                Visit website →
              </a>
            )}
          </div>

          {/* Open Positions */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-white mb-6 font-heading">
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
                      className="group card-dark p-6 border border-border/50 hover:border-primary/30 transition-all duration-200"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-xl font-semibold text-white group-hover:text-primary transition-colors">
                          {job.title}
                        </h3>
                        <span className={`text-xs font-mono px-3 py-1 rounded-md ${
                          job.level === 'Junior' ? 'bg-secondary/10 text-secondary border border-secondary/20' :
                          job.level === 'Middle' ? 'bg-primary/10 text-primary border border-primary/20' :
                          job.level === 'Senior' ? 'bg-accent/10 text-accent border border-accent/20' :
                          'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                        }`}>
                          {job.level}
                        </span>
                      </div>
                      <p className="text-gray-400 mb-4 line-clamp-2 text-sm leading-relaxed">
                        {job.description}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-gray-500 font-mono">
                        <span className="flex items-center gap-1.5">
                          <span className="text-primary">📍</span>
                          {job.location}
                        </span>
                        {formattedSalary && (
                          <span className="flex items-center gap-1.5 text-secondary font-semibold">
                            <span>💰</span>
                            {formattedSalary}
                          </span>
                        )}
                      </div>
                    </Link>
                  );
                })}
              </div>
            ) : (
              <div className="card-dark p-8 text-center border border-border/50">
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
