import { NextRequest, NextResponse } from 'next/server';
import { generateOllamaResponse } from '@lib/ollama';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    // Added locale to destructuring
    const { selectedOption, correctOption, challengeTitle, challengeDescription, locale } = body; 
    
    if (!selectedOption || !correctOption || !locale) { // Added locale check
      return NextResponse.json(
        { error: 'Selected option and correct option are required' },
        { status: 400 }
      );
    }

    // Prepare prompt for Ollama
    const prompt = `
Challenge: ${challengeTitle || 'Cyber security challenge'}
${challengeDescription ? `Description: ${challengeDescription}` : ''}

Selected answer: ${selectedOption}
Correct answer: ${correctOption}

Provide educational feedback on why this answer is ${selectedOption === correctOption ? 'correct' : 'incorrect'}.
If incorrect, explain why the correct answer is better. Keep the explanation educational, supportive and focused on learning.
Limit your response to 3-4 sentences maximum.
`;

    // Connect to Ollama using the utility function, now passing locale
    const feedbackText = await generateOllamaResponse(prompt, locale); 
    
    return NextResponse.json({ 
      feedback: feedbackText || 'No feedback available at this time.' 
    });
  } catch (error) {
    console.error('Error generating AI feedback:', error);
    return NextResponse.json(
      { error: 'Failed to generate AI feedback', details: (error as Error).message },
      { status: 500 }
    );
  }
}
