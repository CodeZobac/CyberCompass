const fs = require('fs');
const path = require('path');

// Function to recursively find all TypeScript/JavaScript files
function findFiles(dir, extension = '.tsx') {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      // Skip node_modules and .next directories
      if (file !== 'node_modules' && file !== '.next') {
        results = results.concat(findFiles(filePath, extension));
      }
    } else if (file.endsWith(extension) || file.endsWith('.ts') || file.endsWith('.jsx') || file.endsWith('.js')) {
      results.push(filePath);
    }
  });
  
  return results;
}

// Function to remove dark: classes from a file
function removeDarkClasses(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Pattern to match dark: classes
  const darkClassPattern = /\s+dark:[a-zA-Z0-9\-\[\]\/\(\)_:]+/g;
  
  // Check if file contains dark: classes
  if (darkClassPattern.test(content)) {
    console.log(`Found dark: classes in ${filePath}`);
    
    // Remove dark: classes
    const cleanedContent = content.replace(darkClassPattern, '');
    
    // Write back to file
    fs.writeFileSync(filePath, cleanedContent, 'utf8');
    console.log(`✅ Cleaned ${filePath}`);
  }
}

// Main execution
console.log('🔍 Searching for files with dark: classes...');

const files = findFiles('./app/components');
let processedCount = 0;

files.forEach(file => {
  try {
    removeDarkClasses(file);
    processedCount++;
  } catch (error) {
    console.error(`❌ Error processing ${file}:`, error.message);
  }
});

console.log(`\n✨ Processed ${processedCount} files`);
console.log('🎉 All dark: classes have been removed!');
