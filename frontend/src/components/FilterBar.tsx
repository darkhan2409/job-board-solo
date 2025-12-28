'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { JobLevel } from '@/lib/types';
import { Search, MapPin, Sliders, X } from 'lucide-react';

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
    junior: 'bg-secondary/10 text-secondary border-secondary/20 hover:bg-secondary/20',
    middle: 'bg-primary/10 text-primary border-primary/20 hover:bg-primary/20',
    senior: 'bg-accent/10 text-accent border-accent/20 hover:bg-accent/20',
    lead: 'bg-purple-500/10 text-purple-400 border-purple-500/20 hover:bg-purple-500/20',
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
        <h2 className="text-sm font-bold uppercase tracking-wide text-muted-foreground flex items-center gap-2">
          <Sliders className="w-4 h-4" />
          Filters
        </h2>
        {hasFilters && (
          <button
            onClick={clearFilters}
            className="text-xs text-primary hover:text-primary/80 font-medium flex items-center gap-1 uppercase tracking-wide"
          >
            <X className="w-3 h-3" />
            Clear
          </button>
        )}
      </div>

      {/* Search */}
      <div>
        <label htmlFor="search-input" className="block text-xs font-semibold text-muted-foreground mb-2 uppercase tracking-wide flex items-center gap-2">
          <Search className="w-3 h-3" />
          Search
        </label>
        <Input
          id="search-input"
          data-testid="search-input"
          type="text"
          placeholder="Role, tech stack..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-card border-muted"
        />
      </div>
      
      {/* Location */}
      <div>
        <label htmlFor="location-input" className="block text-xs font-semibold text-muted-foreground mb-2 uppercase tracking-wide flex items-center gap-2">
          <MapPin className="w-3 h-3" />
          Location
        </label>
        <Input
          id="location-input"
          data-testid="location-filter"
          type="text"
          placeholder="City or Remote..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full bg-card border-muted"
        />
      </div>

      {/* Level - Toggle style */}
      <div>
        <label className="block text-xs font-semibold text-muted-foreground mb-3 uppercase tracking-wide">
          Experience Level
        </label>
        <div className="flex flex-col gap-2">
          {levels.map((level) => (
            <button
              key={level}
              data-testid={`level-${level}`}
              onClick={() => toggleLevel(level)}
              className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all border uppercase tracking-wide ${
                selectedLevels.includes(level)
                  ? levelColors[level]
                  : 'bg-card text-muted-foreground border-muted hover:border-primary/50'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      {hasFilters && (
        <Button
          data-testid="clear-filters"
          onClick={clearFilters}
          variant="outline"
          className="w-full font-semibold border-muted hover:border-primary"
        >
          Clear all filters
        </Button>
      )}
    </div>
  );
}
