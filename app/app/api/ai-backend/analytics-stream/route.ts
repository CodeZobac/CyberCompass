/**
 * Analytics Stream API Route
 * Server-Sent Events for real-time analytics updates
 */

import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const userId = request.nextUrl.searchParams.get('userId');

  if (!userId) {
    return new Response('Missing userId parameter', { status: 400 });
  }

  // Create a readable stream for Server-Sent Events
  const encoder = new TextEncoder();
  
  const stream = new ReadableStream({
    async start(controller) {
      // Send initial connection message
      controller.enqueue(
        encoder.encode(`data: ${JSON.stringify({ type: 'connected' })}\n\n`)
      );

      // TODO: Connect to AI backend WebSocket or SSE endpoint
      // For now, simulate periodic updates
      const interval = setInterval(() => {
        try {
          // Mock analytics update
          const update = {
            type: 'analytics_update',
            timestamp: new Date().toISOString(),
            data: {
              experiencePoints: Math.floor(Math.random() * 100) + 2300,
              currentStreak: 7,
            },
          };
          
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify(update)}\n\n`)
          );
        } catch (error) {
          console.error('Error sending analytics update:', error);
        }
      }, 30000); // Update every 30 seconds

      // Cleanup on connection close
      request.signal.addEventListener('abort', () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
