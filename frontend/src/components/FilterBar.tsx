'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { JobLevel } from '@/lib/types';

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
    <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
      <h2 className="text-lg font-semibold mb-4">Filters</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="search-input" className="block text-sm font-medium text-gray-700 mb-2">
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
        
        <div>
          <label htmlFor="location-input" className="block text-sm font-medium text-gray-700 mb-2">
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
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Level
        </label>
        <div className="flex flex-wrap gap-2">
          {levels.map((level) => (
            <button
              key={level}
              data-testid={`level-${level}`}
              onClick={() => toggleLevel(level)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                selectedLevels.includes(level)
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
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
          className="w-full md:w-auto"
        >
          Clear all filters
        </Button>
      )}
    </div>
  );
}
