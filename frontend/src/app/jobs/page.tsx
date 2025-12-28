import { Suspense } from 'react'
import { fetchJobs } from '@/lib/api'
import { JobFilters, JobLevel } from '@/lib/types'
import JobCard from '@/components/JobCard'
import JobCardSkeleton from '@/components/JobCardSkeleton'
import FilterBar from '@/components/FilterBar'
import SortDropdown from '@/components/SortDropdown'
import Pagination from '@/components/Pagination'
import { Briefcase, ArrowUpDown } from 'lucide-react'

const ITEMS_PER_PAGE = 12;

interface JobsPageProps {
  searchParams: {
    search?: string
    location?: string
    level?: string
    sort?: string
    minSalary?: string
    maxSalary?: string
    page?: string
  }
}

async function JobsList({ searchParams }: JobsPageProps) {
  const filters: JobFilters = {
    search: searchParams.search,
    location: searchParams.location,
    level: searchParams.level as JobLevel | undefined,
  }
  
  let jobs = await fetchJobs(filters)
  
  // Apply salary filter (client-side for now)
  if (searchParams.minSalary || searchParams.maxSalary) {
    const minSalary = searchParams.minSalary ? parseInt(searchParams.minSalary) : 0;
    const maxSalary = searchParams.maxSalary ? parseInt(searchParams.maxSalary) : Infinity;
    
    jobs = jobs.filter(job => {
      if (!job.salary) return false;
      
      // Extract numbers from salary string (e.g., "$150,000 - $180,000" or "€70,000 - €90,000")
      const salaryNumbers = job.salary.match(/\d+/g);
      if (!salaryNumbers || salaryNumbers.length === 0) return false;
      
      // Get the average or first salary value
      const salaryValue = parseInt(salaryNumbers[0].replace(/,/g, ''));
      
      return salaryValue >= minSalary && salaryValue <= maxSalary;
    });
  }
  
  // Apply sorting
  const sortBy = searchParams.sort || 'newest'
  if (sortBy === 'newest') {
    jobs = jobs.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
  } else if (sortBy === 'oldest') {
    jobs = jobs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  } else if (sortBy === 'salary-high') {
    jobs = jobs.sort((a, b) => (b.salary || 0) - (a.salary || 0))
  } else if (sortBy === 'salary-low') {
    jobs = jobs.sort((a, b) => (a.salary || 0) - (b.salary || 0))
  }

  // Pagination
  const currentPage = parseInt(searchParams.page || '1');
  const totalJobs = jobs.length;
  const totalPages = Math.ceil(totalJobs / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedJobs = jobs.slice(startIndex, endIndex);
  
  if (jobs.length === 0) {
    return (
      <div className="col-span-full text-center py-12">
        <Briefcase className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
        <h3 className="text-xl font-semibold mb-2">No jobs found</h3>
        <p className="text-muted-foreground">
          Try adjusting your filters or search terms
        </p>
      </div>
    )
  }
  
  return (
    <>
      <div className="col-span-full grid md:grid-cols-2 gap-6 animate-stagger">
        {paginatedJobs.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
      <div className="col-span-full">
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          itemsPerPage={ITEMS_PER_PAGE}
          totalItems={totalJobs}
        />
      </div>
    </>
  )
}

function JobsLoading() {
  return (
    <>
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <JobCardSkeleton key={i} />
      ))}
    </>
  )
}

export default function JobsPage({ searchParams }: JobsPageProps) {
  const hasFilters = searchParams.search || searchParams.location || searchParams.level
  
  return (
    <div className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Browse Roles</h1>
          <p className="text-lg text-muted-foreground">
            Structured opportunities from verified companies
          </p>
        </div>
        
        {/* Main Content */}
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar - Filters */}
          <aside className="lg:col-span-1">
            <div className="bg-card border border-muted rounded-2xl p-6 sticky top-24">
              <FilterBar />
            </div>
          </aside>
          
          {/* Jobs Grid */}
          <div className="lg:col-span-3">
            <div className="mb-6 flex items-center justify-between">
              <Suspense fallback={<p className="text-muted-foreground">Loading...</p>}>
                <JobsCount searchParams={searchParams} />
              </Suspense>
              <SortDropdown />
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <Suspense fallback={<JobsLoading />}>
                <JobsList searchParams={searchParams} />
              </Suspense>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

async function JobsCount({ searchParams }: JobsPageProps) {
  const filters: JobFilters = {
    search: searchParams.search,
    location: searchParams.location,
    level: searchParams.level as JobLevel | undefined,
  }
  
  const jobs = await fetchJobs(filters)
  
  return (
    <div className="flex items-center gap-2">
      <div className="w-2 h-2 bg-primary rounded-full"></div>
      <p className="text-sm font-semibold text-muted-foreground mono">
        {jobs.length} {jobs.length === 1 ? 'role' : 'roles'}
      </p>
    </div>
  )
}
