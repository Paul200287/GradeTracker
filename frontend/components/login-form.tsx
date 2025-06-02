"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2 } from "lucide-react"

export default function LoginForm() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      // Create form data for OAuth2PasswordRequestForm
      const formData = new FormData()
      formData.append("username", email) // FastAPI OAuth2 uses 'username' field for email
      formData.append("password", password)

      const response = await fetch("http://localhost:8000/api/v1/login", {
        method: "POST",
        body: formData, // Send as form data, not JSON
      })

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem("jwt_token", data.access_token)
        // Store basic user info (you might want to fetch full user details separately)
        localStorage.setItem("user_data", JSON.stringify({ email }))
        router.push("/subjects")
      } else {
        const errorData = await response.json()
        setError(errorData.detail || "Invalid credentials")
      }
    } catch (err) {
      setError("Login failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleMicrosoftSignIn = async () => {
    setLoading(true)
    setError("")

    try {
      // Simulate Microsoft OAuth flow
      // In a real app, this would redirect to Microsoft OAuth
      const response = await fetch("/api/auth/microsoft", {
        method: "POST",
      })

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem("jwt_token", data.token)
        localStorage.setItem("user_data", JSON.stringify(data.user))
        router.push("/subjects")
      } else {
        setError("Microsoft sign-in failed")
      }
    } catch (err) {
      setError("Microsoft sign-in failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="mx-auto max-w-sm">
      <CardHeader>
        <CardTitle className="text-2xl">Login</CardTitle>
        <CardDescription>Enter your email below to login to your account</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleLogin} className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="m@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Signing in...
              </>
            ) : (
              "Sign in"
            )}
          </Button>

          <Button type="button" variant="outline" className="w-full" onClick={handleMicrosoftSignIn} disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Signing in...
              </>
            ) : (
              "Sign in with Microsoft"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
