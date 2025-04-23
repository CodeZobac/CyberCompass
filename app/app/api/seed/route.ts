import { NextRequest, NextResponse } from 'next/server';
import { seedChallenges } from '@lib/seed-challenges';

// This endpoint is for development use only
// It should be secured or removed in production
export async function POST(request: NextRequest) {
  // Check for secret token to prevent unauthorized seeding
  const authHeader = request.headers.get('authorization');
  if (!authHeader || authHeader !== `Bearer ${process.env.SEED_SECRET_TOKEN}`) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  try {
    const result = await seedChallenges();
    
    if (result.error) {
      return NextResponse.json(
        { error: 'Failed to seed database', details: result.error },
        { status: 500 }
      );
    }
    
    return NextResponse.json({ success: true, message: 'Database seeded successfully' });
  } catch (error) {
    console.error('Error seeding database:', error);
    return NextResponse.json(
      { error: 'Failed to seed database' },
      { status: 500 }
    );
  }
}