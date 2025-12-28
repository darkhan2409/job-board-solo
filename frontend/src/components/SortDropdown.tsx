'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { ArrowUpDown, Check } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'

export default function SortDropdown() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  
  const currentSort = searchParams.get('sort') || 'newest'
  
  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
    { value: 'salary-high', label: 'Salary: High to Low' },
    { value: 'salary-low', label: 'Salary: Low to High' },
  ]

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSort = (value: string) => {
    const params = new URLSearchParams(searchParams.toString())
    params.set('sort', value)
    router.push(`/jobs?${params.toString()}`)
    setIsOpen(false)
  }

  const currentLabel = sortOptions.find(opt => opt.value === currentSort)?.label || 'Sort by'

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center gap-2 px-4 py-2 bg-card border border-muted rounded-xl hover:border-primary transition-colors font-medium text-sm"
      >
        <ArrowUpDown className="w-4 h-4 text-primary" />
        {currentLabel}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-card rounded-xl shadow-xl border border-muted py-2 z-10">
          {sortOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => handleSort(option.value)}
              className={`w-full px-4 py-2 text-left text-sm hover:bg-muted transition-colors flex items-center justify-between ${
                currentSort === option.value ? 'text-primary font-semibold' : 'text-foreground'
              }`}
            >
              {option.label}
              {currentSort === option.value && (
                <Check className="w-4 h-4 text-primary" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
