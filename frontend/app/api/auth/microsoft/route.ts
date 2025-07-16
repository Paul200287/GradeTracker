import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    // Simulate Microsoft OAuth authentication
    // In a real app, you would handle the OAuth flow with Microsoft

    // Mock successful Microsoft authentication
    const token =
      "TOKEN-PLACEHOLDER"

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
