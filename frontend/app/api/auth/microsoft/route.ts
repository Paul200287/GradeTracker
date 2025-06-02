import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    // Simulate Microsoft OAuth authentication
    // In a real app, you would handle the OAuth flow with Microsoft

    // Mock successful Microsoft authentication
    const token =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik1pY3Jvc29mdCBVc2VyIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    const user = {
      id: 2,
      username: "microsoft_user",
      email: "user@microsoft.com",
      role: "User",
    }

    return NextResponse.json({
      token,
      user,
      message: "Microsoft sign-in successful",
    })
  } catch (error) {
    return NextResponse.json({ error: "Microsoft sign-in failed" }, { status: 500 })
  }
}
