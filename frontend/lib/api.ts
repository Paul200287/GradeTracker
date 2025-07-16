import axios from "axios"

const API_BASE_URL = "http://localhost:8000"

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwt_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired, redirect to login
      localStorage.removeItem("jwt_token")
      localStorage.removeItem("user_data")
      window.location.href = "/"
    }
    return Promise.reject(error)
  },
)

// Helper function to get current user ID
const getCurrentUserId = (): number | null => {
  const userData = localStorage.getItem("user_data")
  if (userData) {
    try {
      const user = JSON.parse(userData)
      return user.id || null
    } catch (e) {
      return null
    }
  }
  return null
}

// Subject API endpoints
export const subjectApi = {
  getAll: async () => {
    const response = await apiClient.get("/api/v1/subjects/")
    return response.data
  },

  create: async (data: {
    name: string
    description?: string
    semester?: string
    teacher_name?: string
  }) => {
    const userId = getCurrentUserId()
    if (!userId) {
      throw new Error("User not logged in")
    }

    const payload = {
      user_id: userId,
      name: data.name,
      description: data.description || null,
      semester: data.semester || null,
      teacher_name: data.teacher_name || null,
    }

    const response = await apiClient.post("/api/v1/subjects/create-subject", payload)
    return response.data
  },

  update: async (
    id: number,
    data: {
      name: string
      description?: string
      semester?: string
      teacher_name?: string
    },
  ) => {
    const payload = {
      name: data.name,
      description: data.description || null,
      semester: data.semester || null,
      teacher_name: data.teacher_name || null,
    }

    const response = await apiClient.put(`/api/v1/subjects/update-subject/${id}`, payload)
    return response.data
  },
}

// User API endpoints
export const userApi = {
  getProfile: async () => {
    // Use POST /login/me to get current user profile
    const response = await apiClient.post("/api/v1/login/me")
    return response.data
  },

  getAll: async () => {
    const response = await apiClient.get("/api/v1/users")
    return response.data
  },
}

export default apiClient
