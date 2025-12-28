import Link from 'next/link'
import { Briefcase, Building2, Search, TrendingUp, Users, Award } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section - Corporate Professional */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-primary/95 to-secondary py-24 px-4">
        <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:20px_20px]" />
        <div className="container mx-auto relative z-10">
          <div className="max-w-4xl mx-auto text-center text-white">
            <div className="inline-block mb-4 px-4 py-2 bg-accent/20 backdrop-blur-sm rounded-full border border-accent/30">
              <span className="text-accent font-semibold">🚀 #1 Professional Job Board</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Elevate Your Career to
              <span className="block mt-2 text-accent">New Heights</span>
            </h1>
            <p className="text-xl text-blue-100 mb-10 max-w-2xl mx-auto leading-relaxed">
              Connect with leading companies and discover opportunities that match your expertise. 
              Join thousands of professionals advancing their careers.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/jobs"
                className="inline-flex items-center justify-center gap-2 bg-accent text-white px-8 py-4 rounded-lg font-semibold hover:bg-accent/90 transition-all duration-200 shadow-xl hover:shadow-2xl hover:scale-105"
              >
                <Search className="w-5 h-5" />
                Explore Opportunities
              </Link>
              <Link 
                href="/companies"
                className="inline-flex items-center justify-center gap-2 bg-white text-primary px-8 py-4 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200 shadow-lg"
              >
                <Building2 className="w-5 h-5" />
                View Companies
              </Link>
            </div>
          </div>
        </div>
        
        {/* Decorative Elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-accent/10 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary/10 rounded-full blur-3xl" />
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-muted/30 border-y">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary mb-2">500+</div>
              <div className="text-muted-foreground font-medium">Active Jobs</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">200+</div>
              <div className="text-muted-foreground font-medium">Companies</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">10K+</div>
              <div className="text-muted-foreground font-medium">Professionals</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">95%</div>
              <div className="text-muted-foreground font-medium">Success Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Why Choose <span className="text-gradient">JobBoard</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              The professional platform trusted by industry leaders
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card border rounded-xl p-8 card-hover">
              <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <TrendingUp className="w-7 h-7 text-primary" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Career Growth</h3>
              <p className="text-muted-foreground leading-relaxed">
                Access exclusive opportunities from Fortune 500 companies and innovative startups. 
                Advance your career with positions that match your ambitions.
              </p>
            </div>
            
            <div className="bg-card border rounded-xl p-8 card-hover">
              <div className="w-14 h-14 bg-secondary/10 rounded-xl flex items-center justify-center mb-6">
                <Users className="w-7 h-7 text-secondary" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Expert Network</h3>
              <p className="text-muted-foreground leading-relaxed">
                Join a community of top-tier professionals. Connect with industry leaders 
                and expand your professional network.
              </p>
            </div>
            
            <div className="bg-card border rounded-xl p-8 card-hover">
              <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-6">
                <Award className="w-7 h-7 text-accent" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Premium Support</h3>
              <p className="text-muted-foreground leading-relaxed">
                Get personalized career guidance and AI-powered job matching. 
                Our platform ensures you find the perfect fit.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-primary to-secondary">
        <div className="container mx-auto">
          <div className="max-w-3xl mx-auto text-center text-white">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Take the Next Step?
            </h2>
            <p className="text-xl text-blue-100 mb-10 leading-relaxed">
              Join thousands of professionals who have found their dream careers through our platform. 
              Your next opportunity awaits.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/register"
                className="inline-flex items-center justify-center gap-2 bg-accent text-white px-8 py-4 rounded-lg font-semibold hover:bg-accent/90 transition-all duration-200 shadow-xl hover:shadow-2xl hover:scale-105"
              >
                Get Started Free
              </Link>
              <Link 
                href="/jobs"
                className="inline-flex items-center justify-center gap-2 bg-white text-primary px-8 py-4 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200 shadow-lg"
              >
                <Briefcase className="w-5 h-5" />
                Browse Jobs
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
