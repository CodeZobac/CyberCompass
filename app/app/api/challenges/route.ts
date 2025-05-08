import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { 
  getChallengesByCategorySlug, 
  recordChallengeProgress,  
} from '@lib/challenges';

// Get challenges for a specific category
export async function GET(request: NextRequest) {
  try {
    // Check for authentication
    const session = await getServerSession(authOptions);
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    // Get category from URL
    const searchParams = request.nextUrl.searchParams;
    const category = searchParams.get('category');
    
    if (!category) {
      return NextResponse.json(
        { error: 'Category parameter is required' },
        { status: 400 }
      );
    }

    // Fetch challenges for the category
    const challenges = await getChallengesByCategorySlug(category);
    
    return NextResponse.json({ challenges });
  } catch (error) {
    console.error('Error fetching challenges:', error);
    return NextResponse.json(
      { error: 'Failed to fetch challenges' },
      { status: 500 }
    );
  }
}

// Submit an answer to a challenge
export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json();
    const { challengeId, optionId, userId = 'anonymous' } = body;
    
    if (!challengeId || !optionId) {
      return NextResponse.json(
        { error: 'Challenge ID and option ID are required' },
        { status: 400 }
      );
    }

    // Get session if available, otherwise use the provided userId
    const session = await getServerSession(authOptions);
    const userIdToUse = session?.user?.id || userId;
    
    // Record the challenge progress
    const result = await recordChallengeProgress(
      userIdToUse,
      challengeId,
      optionId
    );
    
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error submitting challenge answer:', error);
    return NextResponse.json(
      { error: 'Failed to submit answer' },
      { status: 500 }
    );
  }
}