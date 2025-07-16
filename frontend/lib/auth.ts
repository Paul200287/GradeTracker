// Authentication utilities
export const getAuthToken = (): string | null => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("jwt_token")
  }
  return null
}

export const isAuthenticated = (): boolean => {
  return !!getAuthToken()
}

export const logout = (): void => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("jwt_token")
    localStorage.removeItem("user_data")
  }
}

export const getStoredUser = (): any => {
  if (typeof window !== "undefined") {
    const userData = localStorage.getItem("user_data")
    return userData ? JSON.parse(userData) : null
  }
  return null
}
