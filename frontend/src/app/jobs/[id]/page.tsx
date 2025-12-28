import { fetchJobById } from '@/lib/api';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { MapPin, DollarSign, Calendar, Building2, ArrowLeft, ExternalLink } from 'lucide-react';
import { formatSalary } from '@/lib/salary-utils';
import SaveJobButton from '@/components/SaveJobButton';

interface JobDetailPageProps {
  params: {
    id: string;
  };
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

export default async function JobDetailPage({ params }: JobDetailPageProps) {
  try {
    const job = await fetchJobById(parseInt(params.id));
    const formattedSalary = formatSalary(job.salary);

    return (
      <div className="min-h-screen">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Breadcrumb */}
          <nav className="mb-8" data-testid="breadcrumb">
            <Link
              href="/jobs"
              className="text-primary hover:text-primary/80 flex items-center gap-2 font-medium transition-colors text-sm"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to roles
            </Link>
          </nav>

          {/* Job Header */}
          <div className="bg-card border border-muted rounded-2xl p-8 mb-6">
            <div className="flex justify-between items-start mb-6">
              <div className="flex-1">
                <h1 className="text-4xl font-bold mb-3" data-testid="job-title">
                  {job.title}
                </h1>
                {job.company && (
                  <Link
                    href={`/companies/${job.company.id}`}
                    className="text-xl text-muted-foreground hover:text-primary flex items-center gap-2 font-medium transition-colors"
                    data-testid="company-name"
                  >
                    <Building2 className="w-5 h-5" />
                    {job.company.name}
                  </Link>
                )}
              </div>
              <Badge 
                className={`text-sm font-semibold border uppercase tracking-wide ${getLevelColor(job.level)}`}
                data-testid="job-level"
              >
                {job.level}
              </Badge>
            </div>

            <div className="flex flex-wrap gap-6 text-muted-foreground mb-8 pb-6 border-b border-muted">
              <div className="flex items-center gap-2">
                <MapPin className="w-5 h-5" />
                <span className="font-medium">{job.location}</span>
              </div>
              {formattedSalary && (
                <div className="flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-primary" />
                  <span className="font-bold text-primary mono">{formattedSalary}</span>
                </div>
              )}
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                <span>{new Date(job.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
              </div>
            </div>

            <div className="flex flex-wrap gap-4">
            <Button 
              className="w-full sm:w-auto btn-primary px-8 py-4 text-base font-semibold" 
              size="lg"
              data-testid="apply-button"
            >
              Apply for this role
            </Button>
            <SaveJobButton jobId={job.id} variant="detail" />
            </div>
          </div>

          {/* Job Description */}
          <div className="bg-card border border-muted rounded-2xl p-8 mb-6">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <div className="w-1 h-8 bg-primary rounded"></div>
              Description
            </h2>
            <div 
              className="max-w-none text-muted-foreground leading-relaxed space-y-4"
              data-testid="job-description"
            >
              {job.description.split('\n\n').map((section, sectionIndex) => {
                const lines = section.split('\n');
                const isListSection = lines.some(line => line.trim().startsWith('-'));
                
                if (isListSection) {
                  const heading = lines[0];
                  const items = lines.slice(1).filter(line => line.trim().startsWith('-'));
                  
                  return (
                    <div key={sectionIndex} className="space-y-3">
                      {heading && !heading.trim().startsWith('-') && (
                        <h3 className="text-lg font-semibold text-white font-heading">{heading}</h3>
                      )}
                      <ul className="space-y-2 ml-4">
                        {items.map((item, itemIndex) => (
                          <li key={itemIndex} className="flex items-start gap-3">
                            <span className="text-primary mt-1.5 text-xs">▸</span>
                            <span className="flex-1">{item.replace(/^-\s*/, '')}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  );
                }
                
                return (
                  <p key={sectionIndex} className="leading-relaxed">
                    {section}
                  </p>
                );
              })}
            </div>
          </div>

          {/* About the Company */}
          {job.company && (
            <div className="bg-card border border-muted rounded-2xl p-8">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <div className="w-1 h-8 bg-secondary rounded"></div>
                About {job.company.name}
              </h2>
              {job.company.description && (
                <p className="text-muted-foreground mb-6 leading-relaxed">
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
                  <span>Visit website</span>
                  <ExternalLink className="w-4 h-4" />
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
