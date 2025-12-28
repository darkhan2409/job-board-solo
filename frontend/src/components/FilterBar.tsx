'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { JobLevel } from '@/lib/types';
import { Search, MapPin, Briefcase, X } from 'lucide-react';

export default function FilterBar() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [location, setLocation] = useState(searchParams.get('location') || '');
  const [selectedLevels, setSelectedLevels] = useState<JobLevel[]>(() => {
    const levelParam = searchParams.get('level');
    return levelParam ? [levelParam as JobLevel] : [];
  });

  const levels: JobLevel[] = ['junior', 'middle', 'senior', 'lead'];

  const levelColors = {
    junior: 'bg-green-100 text-green-700 border-green-200 hover:bg-green-200',
    middle: 'bg-blue-100 text-blue-700 border-blue-200 hover:bg-blue-200',
    senior: 'bg-primary/10 text-primary border-primary/20 hover:bg-primary/20',
    lead: 'bg-accent/10 text-accent border-accent/20 hover:bg-accent/20',
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      applyFilters();
    }, 500);

    return () => clearTimeout(timer);
  }, [search, location, selectedLevels]);

  const applyFilters = () => {
    const params = new URLSearchParams();
    
    if (search) params.set('search', search);
    if (location) params.set('location', location);
    if (selectedLevels.length > 0) params.set('level', selectedLevels[0]);

    router.push(`/jobs?${params.toString()}`);
  };

  const toggleLevel = (level: JobLevel) => {
    setSelectedLevels(prev => 
      prev.includes(level) 
        ? prev.filter(l => l !== level)
        : [level]
    );
  };

  const clearFilters = () => {
    setSearch('');
    setLocation('');
    setSelectedLevels([]);
    router.push('/jobs');
  };

  const hasFilters = search || location || selectedLevels.length > 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
          <Briefcase className="w-5 h-5 text-primary" />
          Filters
        </h2>
        {hasFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-primary hover:text-primary/80 font-medium flex items-center gap-1"
          >
            <X className="w-4 h-4" />
            Clear
          </button>
        )}
      </div>

      {/* Search */}
      <div>
        <label htmlFor="search-input" className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <Search className="w-4 h-4 text-primary" />
          Search
        </label>
        <Input
          id="search-input"
          data-testid="search-input"
          type="text"
          placeholder="Job title or keyword..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full"
        />
      </div>
      
      {/* Location */}
      <div>
        <label htmlFor="location-input" className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <MapPin className="w-4 h-4 text-secondary" />
          Location
        </label>
        <Input
          id="location-input"
          data-testid="location-filter"
          type="text"
          placeholder="City or Remote..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full"
        />
      </div>

      {/* Level */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-3">
          Experience Level
        </label>
        <div className="flex flex-col gap-2">
          {levels.map((level) => (
            <button
              key={level}
              data-testid={`level-${level}`}
              onClick={() => toggleLevel(level)}
              className={`px-4 py-2.5 rounded-lg text-sm font-semibold transition-all border ${
                selectedLevels.includes(level)
                  ? levelColors[level]
                  : 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100'
              }`}
            >
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {hasFilters && (
        <Button
          data-testid="clear-filters"
          onClick={clearFilters}
          variant="outline"
          className="w-full font-semibold"
        >
          Clear all filters
        </Button>
      )}
    </div>
  );
}
