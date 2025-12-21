import Link from 'next/link'
import { Briefcase, Building2, Search } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <section className="text-center py-20">
        <h1 className="text-5xl font-bold mb-6">
          Find Your Dream Tech Job
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Browse thousands of tech jobs from top companies. 
          Get matched with opportunities that fit your skills and experience.
        </p>
        <div className="flex gap-4 justify-center">
          <Link 
            href="/jobs"
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity"
          >
            <Search className="w-5 h-5" />
            Browse Jobs
          </Link>
          <Link 
            href="/companies"
            className="inline-flex items-center gap-2 border border-input px-6 py-3 rounded-lg font-semibold hover:bg-accent transition-colors"
          >
            <Building2 className="w-5 h-5" />
            View Companies
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-8 py-12">
        <div className="text-center p-6">
          <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Briefcase className="w-6 h-6 text-primary" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Latest Opportunities</h3>
          <p className="text-muted-foreground">
            Access the newest job postings from leading tech companies
          </p>
        </div>
        
        <div className="text-center p-6">
          <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Search className="w-6 h-6 text-primary" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Smart Filtering</h3>
          <p className="text-muted-foreground">
            Filter by location, seniority level, and tech stack
          </p>
        </div>
        
        <div className="text-center p-6">
          <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Building2 className="w-6 h-6 text-primary" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Leading Companies</h3>
          <p className="text-muted-foreground">
            Explore opportunities at innovative tech companies
          </p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-accent rounded-lg p-12 text-center mt-12">
        <h2 className="text-3xl font-bold mb-4">
          Ready to Start Your Job Search?
        </h2>
        <p className="text-muted-foreground mb-6 max-w-xl mx-auto">
          Join thousands of developers finding their next opportunity
        </p>
        <Link 
          href="/jobs"
          className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity"
        >
          Get Started
        </Link>
      </section>
    </div>
  )
}
