import { fetchCompanies } from '@/lib/api';
import Link from 'next/link';

export default async function CompaniesPage() {
  const companies = await fetchCompanies();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Companies</h1>
          <p className="text-lg text-gray-600">
            Explore top tech companies hiring now
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <Link
              key={company.id}
              href={`/companies/${company.id}`}
              className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6 border border-gray-200"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                {company.name}
              </h2>
              <p className="text-gray-600 mb-4 line-clamp-3">
                {company.description}
              </p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">
                  {company.job_count || 0} open positions
                </span>
                {company.website && (
                  <span className="text-blue-600 hover:text-blue-700">
                    Visit website →
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>

        {companies.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No companies found</p>
          </div>
        )}
      </div>
    </div>
  );
}
