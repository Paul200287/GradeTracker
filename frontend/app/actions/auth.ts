"use server"

import { redirect } from "next/navigation"
import { createSession, deleteSession } from "@/lib/session"

export async function loginAction(formData: FormData) {
  const email = formData.get("email") as string
  const password = formData.get("password") as string

  // Validate input
  if (!email || !password) {
    return { error: "Email and password are required" }
  }

  try {
    // In a real app, you would verify credentials against your database
    // This is a simplified example
    const user = await verifyUserCredentials(email, password)

    if (!user) {
      return { error: "Invalid email or password" }
    }

    // Create session
    await createSession(user.id)

    // Redirect to dashboard
    redirect("/dashboard")
  } catch (error) {
    console.error("Login error:", error)
    return { error: "An error occurred during login" }
  }
}

export async function microsoftSignIn() {
  // In a real app, you would integrate with Microsoft Graph API
  // This is a placeholder for the Microsoft OAuth flow
  const microsoftAuthUrl =
    `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?` +
    `client_id=${process.env.MICROSOFT_CLIENT_ID}&` +
    `response_type=code&` +
    `redirect_uri=${encodeURIComponent(process.env.MICROSOFT_REDIRECT_URI || "")}&` +
    `scope=openid profile email&` +
    `response_mode=query`

  redirect(microsoftAuthUrl)
}

export async function logout() {
  await deleteSession()
  redirect("/login")
}

// Mock function - replace with your actual user verification logic
async function verifyUserCredentials(email: string, password: string) {
  // This would typically query your database
  // For demo purposes, we'll use a mock user
  if (email === "demo@example.com" && password === "password") {
    return { id: "1", email: "demo@example.com", name: "Demo User" }
  }
  return null
}