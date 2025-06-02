"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import LoginForm from "@/components/login-form"

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem("jwt_token")
    if (token) {
      router.push("/subjects")
    }
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <LoginForm />
    </div>
  )
}
