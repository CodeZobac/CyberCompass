// Simple script to seed the database using next API route
// We'll use fetch to call our own API endpoint

async function runSeed() {
  try {
    console.log('Starting to seed challenges...');
    
    // Start the Next.js server in the background if not already running
    console.log('Make sure your Next.js server is running!');
    
    // Wait for user confirmation
    console.log('Press any key to continue and seed the database...');
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.on('data', async () => {
      process.stdin.setRawMode(false);
      process.stdin.pause();
      
      try {
        // Use the seed secret token from environment or a default for development
        const seedToken = process.env.SEED_SECRET_TOKEN || 'dev-seed-token';
        
        const response = await fetch('http://localhost:3000/api/seed', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${seedToken}`
          }
        });
        
        const result = await response.json();
        
        if (response.ok) {
          console.log('Database seeded successfully!', result);
        } else {
          console.error('Error seeding database:', result);
          console.log('\nMake sure:');
          console.log('1. Your Next.js server is running on port 3000');
          console.log('2. The SEED_SECRET_TOKEN environment variable is set correctly');
          console.log('3. You\'re using the same SEED_SECRET_TOKEN in this script and in your .env file');
        }
      } catch (error) {
        console.error('Network error or server not running:', error.message);
      }
      
      process.exit();
    });
    
  } catch (error) {
    console.error('Unexpected error during seeding:', error);
    process.exit(1);
  }
}

runSeed();