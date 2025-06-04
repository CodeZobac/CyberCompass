/**
 * Utility to communicate with Google Gemini API
 */
import { GoogleGenerativeAI } from '@google/generative-ai';

export async function generateGeminiResponse(
  prompt: string,
  locale: string, // Added locale parameter (e.g., 'en', 'pt')
  model: string = 'gemini-2.0-flash'
): Promise<string> {
  try {
    // Check for API key
    const apiKey = process.env.GOOGLE_GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error('GOOGLE_GEMINI_API_KEY environment variable is required');
    }

    // Initialize the Gemini API
    const genAI = new GoogleGenerativeAI(apiKey);

    // Base system prompt content (from Modelfile's SYSTEM block)
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
    console.log("Dynamic System Prompt to Gemini:", dynamicSystemPrompt);

    // Get the generative model with system instruction
    const modelInstance = genAI.getGenerativeModel({
      model: model,
      systemInstruction: dynamicSystemPrompt,
      generationConfig: {
        temperature: 0.7,
        topP: 0.9,
        maxOutputTokens: 1024,
      },
    });

    // Generate content
    const result = await modelInstance.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    return text || '';
  } catch (error: unknown) {
    console.error('Error generating Gemini response:', error);
    
    // Type guard for errors with status property
    const hasStatus = (err: unknown): err is { status: number } => {
      return typeof err === 'object' && err !== null && 'status' in err;
    };
    
    // Handle quota/rate limit errors more gracefully
    if (hasStatus(error) && error.status === 429) {
      console.log('Rate limit hit, suggesting fallback or retry');
      throw new Error('Rate limit exceeded. Please try again in a few minutes or upgrade your Gemini API plan.');
    }
    
    // Handle other common errors
    if (hasStatus(error) && error.status === 403) {
      throw new Error('API key invalid or insufficient permissions. Please check your Gemini API key.');
    }
    
    if (hasStatus(error) && error.status === 400) {
      throw new Error('Invalid request to Gemini API. Please check the input format.');
    }
    
    throw error;
  }
}

// Keep the old function name for backward compatibility
export const generateOllamaResponse = generateGeminiResponse;
