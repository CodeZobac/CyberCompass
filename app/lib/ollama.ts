/**
 * Utility to communicate with Ollama API
 */
export async function generateOllamaResponse(
  prompt: string,
  model: string = 'cyber-compass'
): Promise<string> {
  try {
    // Use the service name from docker-compose.yml instead of localhost
    const ollamaUrl = process.env.OLLAMA_HOST || 'http://ai-service:11434';
    const response = await fetch(`${ollamaUrl}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: model,
        prompt: prompt,
        stream: false
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`);
    }

    const result = await response.json();
    return result.response || '';
  } catch (error) {
    console.error('Error generating Ollama response:', error);
    throw error;
  }
}