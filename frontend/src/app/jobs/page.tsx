import { Suspense } from 'react'
import { fetchJobs } from '@/lib/api'
import { JobFilters, JobLevel } from '@/lib/types'
import JobCard from '@/components/JobCard'
import FilterBar from '@/components/FilterBar'
import { Briefcase } from 'lucide-react'

interface JobsPageProps {
  searchParams: {
    search?: string
    location?: string
    level?: string
  }
}

async function JobsList({ searchParams }: JobsPageProps) {
  const filters: JobFilters = {
    search: searchParams.search,
    location: searchParams.location,
    level: searchParams.level as JobLevel | undefined,
  }
  
  const jobs = await fetchJobs(filters)
  
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
      {jobs.map((job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </>
  )
}

function JobsLoading() {
  return (
    <>
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <div 
          key={i} 
          className="bg-white border rounded-xl p-6 animate-pulse shadow-sm"
        >
          <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="space-y-2">
            <div className="h-4 bg-gray-200 rounded w-1/3"></div>
            <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          </div>
        </div>
      ))}
    </>
  )
}

export default function JobsPage({ searchParams }: JobsPageProps) {
  const hasFilters = searchParams.search || searchParams.location || searchParams.level
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-gradient">Find Your Next Job</h1>
          <p className="text-lg text-muted-foreground">
            Browse through our latest job opportunities from top companies
          </p>
        </div>
        
        {/* Main Content */}
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar - Filters */}
          <aside className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border p-6 sticky top-24">
              <FilterBar />
            </div>
          </aside>
          
          {/* Jobs Grid */}
          <div className="lg:col-span-3">
            <div className="mb-6 flex items-center justify-between">
              <Suspense fallback={<p className="text-muted-foreground">Loading jobs...</p>}>
                <JobsCount searchParams={searchParams} />
              </Suspense>
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
      <p className="text-sm font-semibold text-gray-700">
        {jobs.length} {jobs.length === 1 ? 'job' : 'jobs'} found
      </p>
    </div>
  )
}
