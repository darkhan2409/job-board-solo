import Link from 'next/link'
import { Briefcase, Building2, TrendingUp, Users, Award, ArrowRight, Code, Palette, Database, Smartphone, Globe, Cpu, Terminal, Zap, Shield } from 'lucide-react'
import { fetchJobs } from '@/lib/api'
import JobCard from '@/components/JobCard'
import HeroSearch from '@/components/HeroSearch'

export default async function HomePage() {
  // Fetch featured jobs (latest 6)
  const featuredJobs = await fetchJobs({ limit: 6 })
  
  const categories = [
    { name: 'Frontend', icon: Code, count: 45, color: 'text-primary' },
    { name: 'UI/UX Design', icon: Palette, count: 32, color: 'text-secondary' },
    { name: 'Backend', icon: Database, count: 38, color: 'text-primary' },
    { name: 'Mobile', icon: Smartphone, count: 28, color: 'text-accent' },
    { name: 'Full Stack', icon: Globe, count: 52, color: 'text-secondary' },
    { name: 'DevOps', icon: Cpu, count: 24, color: 'text-accent' },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section - Digital Career OS */}
      <section className="relative overflow-hidden py-24 px-4 noise-texture">
        <div className="absolute inset-0 grid-pattern opacity-30" />
        <div className="container mx-auto relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-card border border-muted rounded-full mb-6">
              <Terminal className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-muted-foreground">Digital Career OS</span>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Find your next
              <span className="block mt-2 text-gradient">IT role</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
              Not another job board. A developer-oriented platform for structured career opportunities.
            </p>
            
            {/* Command Bar Style Search */}
            <HeroSearch />

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/jobs"
                className="inline-flex items-center justify-center gap-2 bg-primary text-primary-foreground px-8 py-4 rounded-xl font-semibold hover:bg-primary/90 transition-all duration-200 shadow-lg shadow-primary/20 hover:shadow-primary/30"
              >
                <Briefcase className="w-5 h-5" />
                Browse Roles
              </Link>
              <Link 
                href="/companies"
                className="inline-flex items-center justify-center gap-2 bg-card border-2 border-muted text-foreground px-8 py-4 rounded-xl font-semibold hover:border-primary transition-all duration-200"
              >
                <Building2 className="w-5 h-5" />
                Companies
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 border-y border-muted">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary mb-2 mono">500+</div>
              <div className="text-muted-foreground text-sm uppercase tracking-wide">Active Roles</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-secondary mb-2 mono">200+</div>
              <div className="text-muted-foreground text-sm uppercase tracking-wide">Companies</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2 mono">10K+</div>
              <div className="text-muted-foreground text-sm uppercase tracking-wide">Developers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-accent mb-2 mono">95%</div>
              <div className="text-muted-foreground text-sm uppercase tracking-wide">Match Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Built for <span className="text-gradient">Developers</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              A product-driven approach to career opportunities
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-card border border-muted rounded-2xl p-8 card-hover">
              <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <Terminal className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Structured Data</h3>
              <p className="text-muted-foreground leading-relaxed">
                Roles presented as structured data. Filter by tech stack, salary range, and experience level with precision.
              </p>
            </div>
            
            <div className="bg-card border border-muted rounded-2xl p-8 card-hover">
              <div className="w-12 h-12 bg-secondary/10 rounded-xl flex items-center justify-center mb-6">
                <Zap className="w-6 h-6 text-secondary" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Live Filtering</h3>
              <p className="text-muted-foreground leading-relaxed">
                Real-time search and filtering. No page reloads, no waiting. Control panel-style interface for developers.
              </p>
            </div>
            
            <div className="bg-card border border-muted rounded-2xl p-8 card-hover">
              <div className="w-12 h-12 bg-accent/10 rounded-xl flex items-center justify-center mb-6">
                <Shield className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Verified Roles</h3>
              <p className="text-muted-foreground leading-relaxed">
                Every role is verified. Salary ranges are real. No spam, no fake listings. Quality over quantity.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Jobs Section */}
      <section className="py-20 px-4 bg-card/30">
        <div className="container mx-auto">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-4xl font-bold mb-2">Latest Roles</h2>
              <p className="text-lg text-muted-foreground">
                Recently posted opportunities
              </p>
            </div>
            <Link 
              href="/jobs"
              className="hidden md:inline-flex items-center gap-2 text-primary hover:text-primary/80 font-semibold transition-colors"
            >
              View all
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {featuredJobs.slice(0, 6).map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>

          <div className="text-center md:hidden">
            <Link 
              href="/jobs"
              className="inline-flex items-center gap-2 text-primary hover:text-primary/80 font-semibold transition-colors"
            >
              View all roles
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Popular Categories Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Browse by Category</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Explore roles organized by tech domain
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((category) => {
              const Icon = category.icon
              return (
                <Link
                  key={category.name}
                  href={`/jobs?search=${encodeURIComponent(category.name)}`}
                  className="group bg-card border border-muted rounded-2xl p-6 card-hover"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className={`w-12 h-12 bg-muted rounded-xl flex items-center justify-center ${category.color}`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <div className="px-3 py-1 bg-muted rounded-full">
                      <span className="text-sm font-semibold mono text-muted-foreground">
                        {category.count}
                      </span>
                    </div>
                  </div>
                  <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">
                    {category.name}
                  </h3>
                  <p className="text-muted-foreground text-sm">
                    Explore {category.name.toLowerCase()} opportunities
                  </p>
                </Link>
              )
            })}
          </div>
        </div>
      </section>
    </div>
  )
}
