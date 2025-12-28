export default function JobCardSkeleton() {
  return (
    <div className="bg-card border border-muted rounded-2xl p-6 animate-pulse">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="h-6 bg-muted rounded w-3/4 mb-3"></div>
          <div className="h-4 bg-muted rounded w-1/2"></div>
        </div>
        <div className="flex items-center gap-2 ml-4">
          <div className="h-6 w-16 bg-muted rounded-full"></div>
          <div className="h-10 w-10 bg-muted rounded-lg"></div>
        </div>
      </div>

      {/* Description */}
      <div className="space-y-2 mb-4">
        <div className="h-4 bg-muted rounded w-full"></div>
        <div className="h-4 bg-muted rounded w-5/6"></div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-muted">
        <div className="flex items-center gap-4">
          <div className="h-4 w-24 bg-muted rounded"></div>
          <div className="h-4 w-20 bg-muted rounded"></div>
        </div>
        <div className="h-4 w-28 bg-muted rounded"></div>
      </div>

      {/* Hover indicator */}
      <div className="mt-4">
        <div className="h-4 w-32 bg-muted rounded"></div>
      </div>
    </div>
  );
}
