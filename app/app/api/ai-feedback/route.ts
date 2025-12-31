import { NextRequest, NextResponse } from 'next/server';
import { aiBackendClient, FallbackService } from '@lib/services/ai-backend-client';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { 
      selectedOption, 
      correctOption, 
      challengeTitle, 
      challengeDescription, 
      locale,
      userId,
      challengeId,
      userHistory 
    } = body; 
    
    // Validate required fields
    if (!selectedOption || !correctOption || !locale) {
      return NextResponse.json(
        { error: 'Selected option, correct option, and locale are required' },
        { status: 400 }
      );
    }

    // Determine if answer is correct
    const isCorrect = selectedOption === correctOption;

    try {
      // Call the new Python AI backend
      const feedbackResponse = await aiBackendClient.generateFeedback({
        user_id: userId || 'anonymous',
        challenge_id: challengeId || 'unknown',
        selected_option: selectedOption,
        correct_option: correctOption,
        locale: locale,
        user_history: userHistory || [],
        context: {
          challenge_title: challengeTitle,
          challenge_description: challengeDescription,
          is_correct: isCorrect,
        },
      });

      // Return the enhanced feedback from CrewAI backend
      return NextResponse.json({
        feedback: feedbackResponse.feedback,
        reasoning: feedbackResponse.reasoning,
        learning_objectives: feedbackResponse.learning_objectives,
        follow_up_questions: feedbackResponse.follow_up_questions,
        confidence_score: feedbackResponse.confidence_score,
      });

    } catch (backendError) {
      // Log the backend error
      console.warn('AI backend unavailable, using fallback:', backendError);

      // Use fallback service for graceful degradation
      const fallbackResponse = FallbackService.generateFallbackFeedback(
        selectedOption,
        correctOption,
        isCorrect,
        locale
      );

      return NextResponse.json({
        feedback: fallbackResponse.feedback,
        confidence_score: fallbackResponse.confidence_score,
        fallback: true,
        error_message: 'AI backend unavailable - using fallback response',
      });
    }

  } catch (error) {
    console.error('Error in AI feedback route:', error);
    return NextResponse.json(
      { 
        error: 'Failed to generate AI feedback', 
        details: (error as Error).message 
      },
      { status: 500 }
    );
  }
}
