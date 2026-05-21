/**
 * E-Shifa AI - Next.js Middleware
 * Role-based access control and verification status routing
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { jwtVerify } from 'jose'

// Define route access rules
const ROUTE_ACCESS_RULES = {
  // Public routes (no authentication required)
  public: [
    '/',
    '/auth',
    '/auth/login',
    '/auth/signup',
    '/about',
    '/contact',
  ],
  
  // Onboarding routes (authenticated but not verified)
  onboarding: [
    '/onboarding/role-selection',
    '/onboarding/profile-completion',
    '/onboarding/document-upload',
    '/onboarding/verification-pending',
  ],
  
  // Role-specific dashboard routes
  dashboards: {
    system_owner: ['/owner'],
    doctor: ['/doctor'],
    nurse: ['/nurse'],
    allied_professional: ['/professional'],
    patient: ['/patient'],
    hospital: ['/hospital'],
    clinic: ['/hospital'],
    diagnostic_center: ['/hospital'],
    pharmacy: ['/pharmacy'],
    medical_store: ['/pharmacy'],
  },
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  
  // Allow public routes
  if (isPublicRoute(pathname)) {
    return NextResponse.next()
  }
  
  // Check authentication
  const token = request.cookies.get('auth_token')?.value
  
  if (!token) {
    return redirectToLogin(request)
  }
  
  try {
    // Verify JWT token
    const secret = new TextEncoder().encode(process.env.JWT_SECRET_KEY)
    const { payload } = await jwtVerify(token, secret)
    
    const user = payload as {
      sub: string
      role: string
      profile_completed: boolean
      verification_status: string
      dashboard_access_enabled: boolean
    }
    
    // Handle onboarding flow
    if (!user.profile_completed || !user.dashboard_access_enabled) {
      return handleOnboardingFlow(request, user)
    }
    
    // Handle role-based access
    return handleRoleBasedAccess(request, user)
    
  } catch (error) {
    console.error('Middleware auth error:', error)
    return redirectToLogin(request)
  }
}

/**
 * Check if route is public
 */
function isPublicRoute(pathname: string): boolean {
  return ROUTE_ACCESS_RULES.public.some(route => 
    pathname === route || pathname.startsWith(route)
  )
}

/**
 * Handle onboarding flow based on user status
 */
function handleOnboardingFlow(
  request: NextRequest,
  user: any
): NextResponse {
  const { pathname } = request.nextUrl
  
  // If already on onboarding route, allow
  if (ROUTE_ACCESS_RULES.onboarding.some(route => pathname.startsWith(route))) {
    return NextResponse.next()
  }
  
  // Redirect based on completion status
  if (!user.profile_completed) {
    // Check if role is selected
    if (user.role === 'patient' && !user.profile_completed) {
      return NextResponse.redirect(
        new URL('/onboarding/role-selection', request.url)
      )
    }
    
    // Profile not completed
    return NextResponse.redirect(
      new URL('/onboarding/profile-completion', request.url)
    )
  }
  
  // Profile completed but not verified
  if (user.verification_status === 'pending' || 
      user.verification_status === 'profile_incomplete') {
    return NextResponse.redirect(
      new URL('/onboarding/document-upload', request.url)
    )
  }
  
  // Documents uploaded, waiting for verification
  if (user.verification_status === 'under_ai_review' ||
      user.verification_status === 'documents_uploaded') {
    return NextResponse.redirect(
      new URL('/onboarding/verification-pending', request.url)
    )
  }
  
  // Verification rejected or escalated
  if (user.verification_status === 'rejected' ||
      user.verification_status === 'escalated_to_owner') {
    return NextResponse.redirect(
      new URL('/onboarding/verification-status', request.url)
    )
  }
  
  // Default: redirect to role selection
  return NextResponse.redirect(
    new URL('/onboarding/role-selection', request.url)
  )
}

/**
 * Handle role-based dashboard access
 */
function handleRoleBasedAccess(
  request: NextRequest,
  user: any
): NextResponse {
  const { pathname } = request.nextUrl
  
  // Get allowed routes for user's role
  const allowedRoutes = ROUTE_ACCESS_RULES.dashboards[user.role as keyof typeof ROUTE_ACCESS_RULES.dashboards]
  
  if (!allowedRoutes) {
    return NextResponse.redirect(new URL('/unauthorized', request.url))
  }
  
  // Check if user is accessing their allowed dashboard
  const hasAccess = allowedRoutes.some(route => pathname.startsWith(route))
  
  if (!hasAccess) {
    // Redirect to user's appropriate dashboard
    return NextResponse.redirect(new URL(allowedRoutes[0], request.url))
  }
  
  // Add user info to request headers for server components
  const response = NextResponse.next()
  response.headers.set('x-user-id', user.sub)
  response.headers.set('x-user-role', user.role)
  response.headers.set('x-verification-status', user.verification_status)
  
  return response
}

/**
 * Redirect to login page
 */
function redirectToLogin(request: NextRequest): NextResponse {
  const loginUrl = new URL('/auth/login', request.url)
  loginUrl.searchParams.set('redirect', request.nextUrl.pathname)
  return NextResponse.redirect(loginUrl)
}

// Configure middleware matcher
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
}
