import { type NextRequest, NextResponse } from "next/server"
import { decrypt } from "@/lib/session"

const protectedRoutes = ["/dashboard", "/profile"]
const authRoutes = ["/login", "/signup"]

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname
  const isProtectedRoute = protectedRoutes.includes(path)
  const isAuthRoute = authRoutes.includes(path)

  const cookie = request.cookies.get("session")?.value
  const session = await decrypt(cookie)

  // Redirect to dashboard if user is logged in and trying to access auth pages
  if (isAuthRoute && session?.userId) {
    return NextResponse.redirect(new URL("/dashboard", request.nextUrl))
  }

  // Redirect to login if user is not logged in and trying to access protected routes
  if (isProtectedRoute && !session?.userId) {
    return NextResponse.redirect(new URL("/login", request.nextUrl))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|.*\\.png$).*)"],
}
