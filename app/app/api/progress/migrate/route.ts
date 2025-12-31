import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { createClient } from '@supabase/supabase-js';

// Migrate anonymous progress to authenticated user
export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    const body = await request.json();
    const { sessionId, anonymousProgress } = body;
    
    if (!sessionId || !Array.isArray(anonymousProgress)) {
      return NextResponse.json(
        { error: 'Session ID and anonymous progress array are required' },
        { status: 400 }
      );
    }

    const userId = session.user.id;
    let migrated = 0;
    let conflicts = 0;
    let failed = 0;
    const details: Array<{
      challengeId: string;
      status: 'migrated' | 'conflict' | 'failed';
      reason?: string;
    }> = [];

    // Get existing user progress to check for conflicts
    const { data: existingProgress, error: existingError } = await supabase
      .from('user_challenge_progress')
      .select('challenge_id')
      .eq('user_id', userId);

    if (existingError) {
      console.error('Error fetching existing progress:', existingError);
      return NextResponse.json(
        { error: 'Failed to check existing progress' },
        { status: 500 }
      );
    }

    const existingChallengeIds = new Set(
      existingProgress?.map(p => p.challenge_id) || []
    );

    // Process each anonymous progress item
    for (const progress of anonymousProgress) {
      try {
        if (existingChallengeIds.has(progress.challengeId)) {
          // Conflict: user already has progress for this challenge
          conflicts++;
          details.push({
            challengeId: progress.challengeId,
            status: 'conflict',
            reason: 'User already has progress for this challenge',
          });
          continue;
        }

        // Migrate the progress
        const { error: insertError } = await supabase
          .from('user_challenge_progress')
          .insert({
            user_id: userId,
            challenge_id: progress.challengeId,
            selected_option_id: progress.selectedOptionId,
            is_completed: progress.isCompleted,
            completed_at: progress.completedAt,
            created_at: progress.createdAt,
            updated_at: progress.updatedAt,
            sync_status: 'synced',
            device_id: null, // Will be set by client
            offline_created_at: progress.createdAt,
            last_synced_at: new Date().toISOString(),
          });

        if (insertError) {
          console.error('Error inserting progress:', insertError);
          failed++;
          details.push({
            challengeId: progress.challengeId,
            status: 'failed',
            reason: insertError.message,
          });
        } else {
          migrated++;
          details.push({
            challengeId: progress.challengeId,
            status: 'migrated',
          });
        }
      } catch (error) {
        console.error('Error processing progress item:', error);
        failed++;
        details.push({
          challengeId: progress.challengeId,
          status: 'failed',
          reason: 'Processing error',
        });
      }
    }

    // Log the migration
    const { error: logError } = await supabase
      .from('progress_sync_log')
      .insert({
        user_id: userId,
        session_id: sessionId,
        sync_type: 'anonymous_to_auth',
        challenges_synced: migrated,
        conflicts_resolved: conflicts,
      });

    if (logError) {
      console.error('Error logging migration:', logError);
      // Don't fail the migration if logging fails
    }

    const result = {
      migrated,
      conflicts,
      failed,
      details,
    };

    return NextResponse.json(result);
  } catch (error) {
    console.error('Error in migration API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
