/**
 * Deepfake Feedback API Route
 * Gets AI-powered feedback on deepfake detection decisions
 */

import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, mediaId, userDecision, correctAnswer, locale } = body;

    // TODO: Replace with actual AI backend call
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

    const response = await fetch(`${AI_BACKEND_URL}/api/deepfake/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_BACKEND_API_KEY}`,
      },
      body: JSON.stringify({
        user_id: userId,
        media_id: mediaId,
        user_decision: userDecision,
        correct_answer: correctAnswer,
        locale,
      }),
    });

    if (!response.ok) {
      throw new Error('AI backend request failed');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error getting deepfake feedback:', error);
    
    // Return mock feedback for development
    const isCorrect = body.userDecision === body.correctAnswer;
    return NextResponse.json({
      isCorrect,
      explanation: isCorrect
        ? 'Great job! You correctly identified this media. Your attention to detail is improving.'
        : `This was actually ${body.correctAnswer ? 'a deepfake' : 'authentic'}. Look for subtle inconsistencies in lighting, facial movements, and edge artifacts.`,
      cluesRevealed: [
        'Unnatural eye movements',
        'Inconsistent lighting on face',
        'Blurred edges around hairline',
      ],
      technicalDetails: [
        'AI backend integration pending - this is mock feedback',
        'Real feedback will include detailed technical analysis',
      ],
    });
  }
}

// Need to access body in catch block
let body: any = {};
