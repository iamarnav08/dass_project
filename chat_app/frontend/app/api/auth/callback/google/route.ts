import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get('code');
  const error = searchParams.get('error');

  // Handle error cases
  if (error) {
    console.error('Google auth error:', error);
    return NextResponse.redirect(new URL('/login?error=oauth_error', request.url));
  }

  // If no code was received, redirect to login
  if (!code) {
    return NextResponse.redirect(new URL('/login?error=no_code', request.url));
  }

  // Create the callback URL with the code
  // Important: Don't redirect back to /api/auth/callback/google as this would cause a loop
  const callbackUrl = new URL('/api/auth/callback/google/processing', request.url);
  callbackUrl.searchParams.set('code', code);
  
  return NextResponse.redirect(callbackUrl);
}
