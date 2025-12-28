import { fetchCompanies } from '@/lib/api';
import Link from 'next/link';
import { Building2, ExternalLink } from 'lucide-react';

export default async function CompaniesPage() {
  const companies = await fetchCompanies();

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-10">
          <h1 className="text-4xl font-bold mb-3">Companies</h1>
          <p className="text-lg text-muted-foreground">
            Verified tech companies hiring developers
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <Link
              key={company.id}
              href={`/companies/${company.id}`}
              className="group bg-card border border-muted rounded-2xl p-6 card-hover"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center text-primary font-bold text-xl">
                  {company.name.charAt(0)}
                </div>
                <div className="px-3 py-1 bg-muted rounded-full">
                  <span className="text-sm font-semibold mono text-muted-foreground">
                    {company.job_count || 0}
                  </span>
                </div>
              </div>
              
              <h2 className="text-xl font-bold mb-3 group-hover:text-primary transition-colors">
                {company.name}
              </h2>
              
              <p className="text-muted-foreground mb-4 line-clamp-3 leading-relaxed text-sm">
                {company.description}
              </p>
              
              {company.website && (
                <div className="pt-4 border-t border-muted flex items-center gap-2 text-primary text-sm font-medium">
                  <span>Visit website</span>
                  <ExternalLink className="w-4 h-4" />
                </div>
              )}
            </Link>
          ))}
        </div>

        {companies.length === 0 && (
          <div className="text-center py-16 bg-card rounded-2xl border border-muted">
            <Building2 className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground text-lg font-medium">No companies found</p>
          </div>
        )}
      </div>
    </div>
  );
}
