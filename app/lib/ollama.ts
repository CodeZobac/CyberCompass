/**
 * Utility to communicate with Ollama API
 */
export async function generateOllamaResponse(
  prompt: string,
  locale: string, // Added locale parameter (e.g., 'en', 'pt')
  model: string = 'cyber-compass'
): Promise<string> {
  try {
    // Base system prompt content (similar to what's in Modelfile's SYSTEM block)
    const baseSystemPrompt = `
I am Cyber Compass, a cyber ethics educator and mentor. My role is to evaluate your response to ethical dilemmas related to digital issues, and provide constructive feedback.

I will be given:
1. Your answer to an ethical dilemma
2. The correct or best answer to that dilemma

My task is to:
- If your answer matches or closely aligns with the correct answer: Provide positive reinforcement and explain why your thinking is on the right track.
- If your answer differs from the correct answer: Explain why your response might not be the most effective or appropriate in a supportive, non-judgmental way. Focus on education rather than criticism.
- In all cases: Provide additional context about the ethical principles involved and how they apply in digital environments.
- Be supportive and encouraging regardless of your answer.
- CRITICAL INSTRUCTION: Your entire response MUST be in the exact same language as the 'USER'S ANSWER'. If 'USER'S ANSWER' is in Portuguese, respond entirely in Portuguese. If 'USER'S ANSWER' is in English, respond entirely in English. Do not mix languages or default to English if the input is Portuguese.
- Always identify myself as "Cyber Compass" at the beginning of my responses.

My feedback should help you develop critical thinking skills about cyber ethics, online safety, privacy, and digital citizenship.
    `.trim();

    let languageSpecificInstruction = '';
    if (locale === 'pt') {
      languageSpecificInstruction = "IMPORTANT: Your entire response MUST be in Portuguese.";
    } else if (locale === 'en') {
      languageSpecificInstruction = "IMPORTANT: Your entire response MUST be in English.";
    }

    // Combine base prompt with the specific language instruction
    const dynamicSystemPrompt = `${baseSystemPrompt}\n${languageSpecificInstruction}`.trim();

    console.log("User's Answer (prompt):", prompt);
    console.log("Dynamic System Prompt to Ollama:", dynamicSystemPrompt);

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
        system: dynamicSystemPrompt, // Pass the dynamically constructed system prompt
        stream: false
      }),
    });

    if (!response.ok) {
      const errorBody = await response.text();
      console.error('Ollama API error response body:', errorBody);
      throw new Error(`Ollama API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    return result.response || '';
  } catch (error) {
    console.error('Error generating Ollama response:', error);
    throw error;
  }
}
