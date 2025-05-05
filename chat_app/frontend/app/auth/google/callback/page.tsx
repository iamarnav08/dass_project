'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { authService } from '@/lib/auth';

export default function GoogleCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [processingComplete, setProcessingComplete] = useState(false);

  useEffect(() => {
    // Use a ref to prevent duplicate requests
    let isProcessing = false;

    async function completeGoogleAuth() {
      // Guard against duplicate processing
      if (isProcessing || processingComplete) return;
      isProcessing = true;

      try {
        // Get the authorization code from URL search params
        const code = searchParams?.get('code');
        
        if (!code) {
          throw new Error('Authorization code not found in URL');
        }
        
        console.log(`Processing authentication with code: ${code.substring(0, 10)}...`);
        
        // Exchange code for token through our backend
        const result = await authService.handleGoogleCallback(code);
        console.log('Authentication successful!');
        setProcessingComplete(true);
        
        // Add a small delay before redirecting to ensure token is stored
        setTimeout(() => {
          router.push('/chat');
        }, 500);
      } catch (err) {
        console.error('Error completing Google authentication:', err);
        setError(err instanceof Error ? err.message : 'Authentication failed');
        
        // Redirect to login page after a delay on error
        setTimeout(() => {
          router.push('/login?error=auth_failed');
        }, 3000);
      } finally {
        setLoading(false);
        isProcessing = false;
      }
    }
    
    completeGoogleAuth();
  }, [router, searchParams, processingComplete]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {error ? (
        <div className="p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-900 dark:text-red-100">
          <h2 className="text-lg font-bold mb-2">Authentication Error</h2>
          <p>{error}</p>
          <p className="mt-2">Redirecting to login page...</p>
        </div>
      ) : (
        <>
          <h1 className="text-2xl font-bold mb-4">
            {processingComplete ? 'Authentication Successful!' : 'Completing Authentication'}
          </h1>
          {loading ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white"></div>
              <span className="ml-3">Completing Google sign-in...</span>
            </div>
          ) : (
            <div className="text-green-600 dark:text-green-400">
              <p>You've been successfully logged in!</p>
              <p className="mt-2">Redirecting to chat page...</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
