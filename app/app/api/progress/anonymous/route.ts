import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

// Submit anonymous progress
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { sessionId, challengeId, optionId } = body;
    
    if (!sessionId || !challengeId || !optionId) {
      return NextResponse.json(
        { error: 'Session ID, challenge ID, and option ID are required' },
        { status: 400 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    // Check if the option is correct
    const { data: option, error: optionError } = await supabase
      .from('challenge_options')
      .select('is_correct')
      .eq('id', optionId)
      .single();

    if (optionError) {
      console.error('Error fetching option:', optionError);
      return NextResponse.json(
        { error: 'Invalid option ID' },
        { status: 400 }
      );
    }

    // Insert or update anonymous progress
    const { data, error } = await supabase
      .from('anonymous_progress')
      .upsert(
        {
          session_id: sessionId,
          challenge_id: challengeId,
          selected_option_id: optionId,
          is_completed: true,
          completed_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
        {
          onConflict: 'session_id,challenge_id',
        }
      )
      .select()
      .single();

    if (error) {
      console.error('Error saving anonymous progress:', error);
      return NextResponse.json(
        { error: 'Failed to save progress' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      isCorrect: option.is_correct,
      progress: data,
    });
  } catch (error) {
    console.error('Error in anonymous progress API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Get anonymous progress for a session
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const sessionId = searchParams.get('sessionId');
    
    if (!sessionId) {
      return NextResponse.json(
        { error: 'Session ID is required' },
        { status: 400 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    const { data, error } = await supabase
      .from('anonymous_progress')
      .select(`
        *,
        challenges (
          id,
          title,
          category_id
        )
      `)
      .eq('session_id', sessionId)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching anonymous progress:', error);
      return NextResponse.json(
        { error: 'Failed to fetch progress' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      progress: data || [],
    });
  } catch (error) {
    console.error('Error in anonymous progress GET API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
