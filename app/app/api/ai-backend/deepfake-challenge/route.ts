/**
 * Deepfake Challenge API Route
 * Fetches deepfake detection challenges from AI backend
 */

import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, locale, difficulty } = body;

    // TODO: Replace with actual AI backend call
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

    const response = await fetch(`${AI_BACKEND_URL}/api/deepfake/challenge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_BACKEND_API_KEY}`,
      },
      body: JSON.stringify({
        user_id: userId,
        locale,
        difficulty,
      }),
    });

    if (!response.ok) {
      throw new Error('AI backend request failed');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching deepfake challenge:', error);
    
    // Return mock data for development
    return NextResponse.json({
      media: {
        id: `mock-${Date.now()}`,
        url: '/placeholder-media.jpg',
        type: 'image',
        isDeepfake: Math.random() > 0.5,
        difficulty: 1,
        detectionClues: [
          'Check facial symmetry',
          'Look for unnatural lighting',
          'Examine edge artifacts',
        ],
      },
    });
  }
}
