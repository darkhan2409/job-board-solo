// Client-side validation functions matching backend requirements

export interface ValidationError {
  field: string
  message: string
}

export function validateEmail(email: string): string | null {
  if (!email) {
    return "Email is required"
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return "Invalid email format"
  }

  return null
}

export function validatePassword(password: string): string | null {
  if (!password) {
    return "Password is required"
  }

  if (password.length < 8) {
    return "Password must be at least 8 characters"
  }

  if (password.length > 100) {
    return "Password must be less than 100 characters"
  }

  if (!/[A-Z]/.test(password)) {
    return "Password must contain an uppercase letter"
  }

  if (!/[a-z]/.test(password)) {
    return "Password must contain a lowercase letter"
  }

  if (!/[0-9]/.test(password)) {
    return "Password must contain a digit"
  }

  return null
}

export function validateFullName(name: string): string | null {
  if (!name) {
    return "Full name is required"
  }

  const trimmedName = name.trim()

  if (trimmedName.length < 1 || trimmedName.length > 100) {
    return "Full name must be between 1 and 100 characters"
  }

  return null
}
