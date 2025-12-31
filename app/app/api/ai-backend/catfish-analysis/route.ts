/**
 * Catfish Analysis API Route
 * Analyzes catfish detection chat performance
 */

import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  let redFlagsSpotted: string[] = [];
  let messageCount = 0;
  
  try {
    const body = await request.json();
    const { sessionId, userId, locale } = body;
    redFlagsSpotted = body.redFlagsSpotted || [];
    messageCount = body.messageCount || 0;

    // TODO: Replace with actual AI backend call
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

    const response = await fetch(`${AI_BACKEND_URL}/api/catfish/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_BACKEND_API_KEY}`,
      },
      body: JSON.stringify({
        session_id: sessionId,
        user_id: userId,
        red_flags_spotted: redFlagsSpotted,
        message_count: messageCount,
        locale,
      }),
    });

    if (!response.ok) {
      throw new Error('AI backend request failed');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error getting catfish analysis:', error);
    
    // Return mock analysis for development
    const detectionRate = Math.min((redFlagsSpotted.length / 5) * 100, 100);
    
    return NextResponse.json({
      redFlagsDetected: [
        {
          type: 'Age Inconsistency',
          description: 'Character claimed different ages during conversation',
          severity: 'high',
          detectedAt: new Date().toISOString(),
        },
        {
          type: 'Evasive Behavior',
          description: 'Avoided answering direct questions about personal details',
          severity: 'medium',
          detectedAt: new Date().toISOString(),
        },
        {
          type: 'Outdated References',
          description: 'Used slang and cultural references inconsistent with claimed age',
          severity: 'medium',
          detectedAt: new Date().toISOString(),
        },
        {
          type: 'Location Inconsistency',
          description: 'Mentioned details that contradict stated location',
          severity: 'high',
          detectedAt: new Date().toISOString(),
        },
        {
          type: 'Photo Reluctance',
          description: 'Made excuses to avoid video calls or recent photos',
          severity: 'high',
          detectedAt: new Date().toISOString(),
        },
      ],
      userDetectionRate: detectionRate,
      characterInconsistencies: [
        'Claimed to be 16 but used outdated slang from the 1990s',
        'Said they live in California but mentioned local UK references',
        'Profile photo appears to be from a stock image website',
        'Story about school changed between conversations',
      ],
      recommendations: [
        'Always verify profile information through multiple sources',
        'Be cautious of people who avoid video calls',
        'Look for inconsistencies in stories and details',
        'Trust your instincts if something feels off',
        'Never share personal information with unverified contacts',
      ],
      overallScore: Math.round(detectionRate * 0.8 + (messageCount > 10 ? 20 : messageCount * 2)),
    });
  }
}
