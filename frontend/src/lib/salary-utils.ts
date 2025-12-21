/**
 * Utility functions for parsing and formatting salary strings
 */

export interface SalaryRange {
  min: number;
  max: number;
}

/**
 * Parse salary string like "$150,000 - $180,000" into min/max numbers
 */
export function parseSalary(salary?: string): SalaryRange | null {
  if (!salary) return null;

  // Remove $ and commas, split by dash or hyphen
  const cleaned = salary.replace(/\$/g, '').replace(/,/g, '');
  const parts = cleaned.split(/\s*-\s*/);

  if (parts.length !== 2) return null;

  const min = parseInt(parts[0].trim());
  const max = parseInt(parts[1].trim());

  if (isNaN(min) || isNaN(max)) return null;

  return { min, max };
}

/**
 * Format salary range for display
 */
export function formatSalary(salary?: string): string | null {
  const range = parseSalary(salary);
  if (!range) return null;

  return `$${range.min.toLocaleString()} - $${range.max.toLocaleString()}`;
}
