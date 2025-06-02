import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json()

    // Simulate authentication logic
    // In a real app, you would validate credentials against your database
    if (email === "admin@example.com" && password === "password") {
      // Generate a mock JWT token
      const token =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

      const user = {
        id: 1,
        username: "admin",
        email: "admin@example.com",
        role: "Superuser",
      }

      return NextResponse.json({
        token,
        user,
        message: "Login successful",
      })
    } else {
      return NextResponse.json({ error: "Invalid credentials" }, { status: 401 })
    }
  } catch (error) {
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
