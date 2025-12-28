import { fetchCompanies } from '@/lib/api';
import Link from 'next/link';
import { Building2 } from 'lucide-react';

export default async function CompaniesPage() {
  const companies = await fetchCompanies();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-10">
          <h1 className="text-4xl font-bold mb-3 text-gradient">Top Companies</h1>
          <p className="text-lg text-muted-foreground">
            Explore leading tech companies hiring talented professionals
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <Link
              key={company.id}
              href={`/companies/${company.id}`}
              className="group bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 p-6 border border-gray-200 card-hover"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center text-white font-bold text-xl">
                  {company.name.charAt(0)}
                </div>
                <div className="px-3 py-1 bg-primary/10 rounded-full">
                  <span className="text-sm font-semibold text-primary">
                    {company.job_count || 0} jobs
                  </span>
                </div>
              </div>
              
              <h2 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-primary transition-colors">
                {company.name}
              </h2>
              
              <p className="text-gray-600 mb-4 line-clamp-3 leading-relaxed">
                {company.description}
              </p>
              
              {company.website && (
                <div className="pt-4 border-t">
                  <span className="text-secondary hover:text-secondary/80 font-medium inline-flex items-center gap-1">
                    Visit website →
                  </span>
                </div>
              )}
            </Link>
          ))}
        </div>

        {companies.length === 0 && (
          <div className="text-center py-16 bg-white rounded-xl shadow-sm border">
            <Building2 className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
            <p className="text-gray-500 text-lg font-medium">No companies found</p>
          </div>
        )}
      </div>
    </div>
  );
}
