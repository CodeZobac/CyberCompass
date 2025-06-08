'use client';

import React, { useEffect, useState } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import { createQueryClient } from '@lib/react-query';

interface QueryProviderProps {
  children: React.ReactNode;
}

// Create a stable query client instance
let globalQueryClient: ReturnType<typeof createQueryClient> | undefined = undefined;

const getQueryClient = () => {
  if (!globalQueryClient) {
    globalQueryClient = createQueryClient();
  }
  return globalQueryClient;
};

export function QueryProvider({ children }: QueryProviderProps) {
  const [queryClient] = useState(() => createQueryClient());
  const [isRestored, setIsRestored] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Create storage persister
      const persister = createSyncStoragePersister({
        storage: {
          getItem: (key: string) => {
            try {
              return localStorage.getItem(key);
            } catch {
              return null;
            }
          },
          setItem: (key: string, value: string) => {
            try {
              localStorage.setItem(key, value);
            } catch {
              // Silently fail
            }
          },
          removeItem: (key: string) => {
            try {
              localStorage.removeItem(key);
            } catch {
              // Silently fail
            }
          },
        },
        key: 'cybercompass-query-cache',
      });

      // Restore cache from storage
      const restoreCache = async () => {
        try {
          const storedData = localStorage.getItem('cybercompass-query-cache');
          if (storedData) {
            const parsedData = JSON.parse(storedData);
            queryClient.setQueryData(['progress'], parsedData.queries?.find((q: any) => 
              q.queryKey?.[0] === 'progress'
            )?.state?.data || []);
          }
        } catch (error) {
          console.warn('Failed to restore query cache:', error);
        } finally {
          setIsRestored(true);
        }
      };

      restoreCache();

      // Persist cache on changes
      const unsubscribe = queryClient.getQueryCache().subscribe(() => {
        try {
          const queries = queryClient.getQueryCache().getAll();
          const cacheData = {
            queries: queries.map(query => ({
              queryKey: query.queryKey,
              state: query.state,
            })),
            timestamp: Date.now(),
          };
          localStorage.setItem('cybercompass-query-cache', JSON.stringify(cacheData));
        } catch (error) {
          console.warn('Failed to persist query cache:', error);
        }
      });

      return () => {
        unsubscribe();
      };
    } else {
      setIsRestored(true);
    }
  }, [queryClient]);

  // Don't render until cache is restored on client
  if (typeof window !== 'undefined' && !isRestored) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="p-4 bg-white border-4 border-black shadow-[8px_8px_0_0_#000]">
          <span className="font-bold uppercase tracking-wider">Loading Progress...</span>
        </div>
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools 
          initialIsOpen={false}
          buttonPosition="bottom-left"
        />
      )}
    </QueryClientProvider>
  );
}
