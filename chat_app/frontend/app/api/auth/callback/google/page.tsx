'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { authService } from '@/lib/auth';

export default function GoogleCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState('Processing authentication...');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function handleCallback() {
      const code = searchParams?.get('code');
      const error = searchParams?.get('error');
      
      // Handle errors from Google's OAuth server
      if (error) {
        console.error('Google OAuth error:', error);
        setError(`Google authentication failed: ${error}`);
        setTimeout(() => router.push('/login?error=oauth_error'), 2000);
        return;
      }
      
      // Validate the authorization code
      if (!code) {
        console.error('No authorization code received');
        setError('No authorization code received');
        setTimeout(() => router.push('/login?error=no_code'), 2000);
        return;
      }
      
      try {
        setStatus('Authenticating with Google...');
        // Call the auth service to exchange the code for a token
        const result = await authService.handleGoogleCallback(code);
        
        // If result is null, it means a redirect was already triggered (e.g., expired code)
        if (result === null) {
          return;
        }
        
        setStatus('Authentication successful, redirecting...');
        
        // Redirect to the chat page after successful authentication
        setTimeout(() => router.push('/chat'), 500);
      } catch (err) {
        console.error('Error completing Google authentication:', err);
        setError(err instanceof Error ? err.message : 'Authentication failed');
        
        // Redirect back to login with error after a delay
        setTimeout(() => router.push('/login?error=auth_failed'), 2000);
      }
    }
    
    handleCallback();
  }, [router, searchParams]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center mb-4 dark:text-white">
          Google Authentication
        </h1>
        
        {!error ? (
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">{status}</p>
          </div>
        ) : (
          <div className="text-center">
            <div className="flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mx-auto mb-4">
              <svg className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="text-red-500 mb-4">{error}</p>
            <p className="text-gray-600 dark:text-gray-300">Redirecting back to login...</p>
          </div>
        )}
      </div>
    </div>
  );
}
