import Link from 'next/link'
import { Briefcase, Mail, MapPin, Phone, Github, Linkedin, Twitter } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gray-900 text-gray-300 border-t border-gray-800">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Briefcase className="w-6 h-6 text-accent" />
              <span className="text-xl font-bold text-white">JobBoard</span>
            </div>
            <p className="text-sm text-gray-400 mb-4 leading-relaxed">
              Your trusted platform for finding the perfect career opportunity. 
              Connect with top companies and advance your professional journey.
            </p>
            <div className="flex gap-3">
              <a 
                href="https://github.com/darkhan2409/job-board-solo" 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-9 h-9 bg-gray-800 hover:bg-primary rounded-lg flex items-center justify-center transition-colors"
              >
                <Github className="w-4 h-4" />
              </a>
              <a 
                href="#" 
                className="w-9 h-9 bg-gray-800 hover:bg-primary rounded-lg flex items-center justify-center transition-colors"
              >
                <Linkedin className="w-4 h-4" />
              </a>
              <a 
                href="#" 
                className="w-9 h-9 bg-gray-800 hover:bg-primary rounded-lg flex items-center justify-center transition-colors"
              >
                <Twitter className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/jobs" className="text-sm hover:text-accent transition-colors">
                  Browse Jobs
                </Link>
              </li>
              <li>
                <Link href="/companies" className="text-sm hover:text-accent transition-colors">
                  Companies
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-sm hover:text-accent transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-sm hover:text-accent transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* For Employers */}
          <div>
            <h3 className="text-white font-semibold mb-4">For Employers</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/post-job" className="text-sm hover:text-accent transition-colors">
                  Post a Job
                </Link>
              </li>
              <li>
                <Link href="/pricing" className="text-sm hover:text-accent transition-colors">
                  Pricing
                </Link>
              </li>
              <li>
                <Link href="/employer-resources" className="text-sm hover:text-accent transition-colors">
                  Resources
                </Link>
              </li>
              <li>
                <Link href="/faq" className="text-sm hover:text-accent transition-colors">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-2 text-sm">
                <MapPin className="w-4 h-4 text-accent mt-0.5 flex-shrink-0" />
                <span>123 Business St, Tech City, TC 12345</span>
              </li>
              <li className="flex items-center gap-2 text-sm">
                <Mail className="w-4 h-4 text-accent flex-shrink-0" />
                <a href="mailto:contact@jobboard.com" className="hover:text-accent transition-colors">
                  contact@jobboard.com
                </a>
              </li>
              <li className="flex items-center gap-2 text-sm">
                <Phone className="w-4 h-4 text-accent flex-shrink-0" />
                <a href="tel:+1234567890" className="hover:text-accent transition-colors">
                  +1 (234) 567-890
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-400">
              © {currentYear} JobBoard. All rights reserved.
            </p>
            <div className="flex gap-6 text-sm">
              <Link href="/privacy" className="hover:text-accent transition-colors">
                Privacy Policy
              </Link>
              <Link href="/terms" className="hover:text-accent transition-colors">
                Terms of Service
              </Link>
              <Link href="/cookies" className="hover:text-accent transition-colors">
                Cookie Policy
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
