import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

// Handle beacon sync requests (called during page unload)
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { type, items, deviceId } = body;
    
    if (type !== 'batch_sync' || !Array.isArray(items)) {
      return NextResponse.json(
        { error: 'Invalid beacon sync request' },
        { status: 400 }
      );
    }

    let processed = 0;
    let failed = 0;

    // Process each sync item
    for (const item of items) {
      try {
        // Insert or update anonymous progress
        const { error } = await supabase
          .from('anonymous_progress')
          .upsert(
            {
              session_id: item.sessionId,
              challenge_id: item.challengeId,
              selected_option_id: item.selectedOptionId,
              is_completed: item.isCompleted,
              completed_at: new Date(item.timestamp).toISOString(),
              updated_at: new Date().toISOString(),
            },
            {
              onConflict: 'session_id,challenge_id',
            }
          );

        if (error) {
          console.error('Beacon sync error for item:', item.challengeId, error);
          failed++;
        } else {
          processed++;
        }
      } catch (error) {
        console.error('Error processing beacon sync item:', error);
        failed++;
      }
    }

    // Log the beacon sync attempt
    try {
      await supabase
        .from('progress_sync_log')
        .insert({
          user_id: null, // Anonymous beacon sync
          session_id: items[0]?.sessionId || 'unknown',
          sync_type: 'offline_sync',
          challenges_synced: processed,
          conflicts_resolved: 0,
        });
    } catch (logError) {
      console.error('Error logging beacon sync:', logError);
      // Don't fail the sync if logging fails
    }

    return NextResponse.json({
      success: true,
      processed,
      failed,
      total: items.length,
    });
  } catch (error) {
    console.error('Beacon sync error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
