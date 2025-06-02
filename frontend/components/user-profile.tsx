"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { User, Mail, Calendar, Shield } from "lucide-react"
import { userApi } from "@/lib/api"

interface UserProfile {
  username: string
  email: string
  id: number
  created_at: string
  updated_at: string
  role: string
}

export default function UserProfile() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    fetchUserProfile()
  }, [])

  const fetchUserProfile = async () => {
    try {
      const data = await userApi.getProfile()
      setProfile(data)
      localStorage.setItem("user_data", JSON.stringify(data))
      setError("")
    } catch (err: any) {
      console.error("Failed to fetch user profile:", err)
      setError("Failed to load user profile")

      // Fallback to stored user data if available
      const storedUserData = localStorage.getItem("user_data")
      if (storedUserData) {
        try {
          const userData = JSON.parse(storedUserData)
          setProfile(userData)
          setError("")
        } catch (parseError) {
          console.error("Failed to parse stored user data:", parseError)
        }
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            User Profile
          </CardTitle>
          <CardDescription>Loading your account information...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error && !profile) {
    // Show minimal info from localStorage if profile fetch failed
    const storedUserData = localStorage.getItem("user_data")
    if (storedUserData) {
      try {
        const userData = JSON.parse(storedUserData)
        if (userData.email) {
          return (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5" />
                  User Profile
                </CardTitle>
                <CardDescription>Your account information (cached)</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-gray-500" />
                  <span className="font-medium">Email:</span>
                  <span>{userData.email}</span>
                </div>
              </CardContent>
            </Card>
          )
        }
      } catch (e) {
        // Ignore parse errors
      }
    }
    return null
  }

  if (!profile) {
    return null
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const getRoleBadgeVariant = (role: string) => {
    switch (role.toLowerCase()) {
      case "superuser":
        return "destructive"
      case "admin":
        return "default"
      case "user":
        return "secondary"
      default:
        return "outline"
    }
  }

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <User className="h-5 w-5" />
          User Profile
        </CardTitle>
        <CardDescription>Your account information</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <User className="h-4 w-4 text-gray-500" />
            <span className="font-medium">Username:</span>
            <span>{profile.username}</span>
          </div>
          <div className="flex items-center gap-2">
            <Mail className="h-4 w-4 text-gray-500" />
            <span className="font-medium">Email:</span>
            <span>{profile.email}</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-gray-500" />
            <span className="font-medium">Role:</span>
            <Badge variant={getRoleBadgeVariant(profile.role)}>{profile.role}</Badge>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-gray-500" />
            <span className="font-medium">Member since:</span>
            <span>{formatDate(profile.created_at)}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
