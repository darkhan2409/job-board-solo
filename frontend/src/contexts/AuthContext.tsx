'use client'

import React, { createContext, useState, useEffect, useCallback } from 'react'
import { User, AuthState, LoginRequest, RegisterRequest } from '@/lib/types'
import {
  loginUser,
  registerUser,
  logoutUser as apiLogout,
} from '@/lib/api'
import {
  getStoredUser,
  saveUser,
  setTokens,
  clearTokens,
  getAccessToken,
  getRefreshToken,
} from '@/lib/auth'

interface AuthContextType extends AuthState {
  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<User>
  logout: () => Promise<void>
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  })

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = () => {
      const storedUser = getStoredUser()
      const token = getAccessToken()

      if (storedUser && token) {
        setState({
          user: storedUser,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        })
      } else {
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        })
      }
    }

    initAuth()
  }, [])

  const login = useCallback(async (data: LoginRequest) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await loginUser(data)
      setTokens(response.access_token, response.refresh_token)
      saveUser(response.user)

      setState({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      })
    } catch (error) {
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Login failed',
      })
      throw error
    }
  }, [])

  const register = useCallback(async (data: RegisterRequest): Promise<User> => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }))

    try {
      const user = await registerUser(data)
      setState((prev) => ({ ...prev, isLoading: false, error: null }))
      return user
    } catch (error) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Registration failed',
      }))
      throw error
    }
  }, [])

  const logout = useCallback(async () => {
    const refreshToken = getRefreshToken()

    try {
      if (refreshToken) {
        await apiLogout(refreshToken)
      }
    } catch (error) {
      console.error('Logout API call failed:', error)
    } finally {
      clearTokens()
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      })
    }
  }, [])

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
