/**
 * AI Backend Client - Service for communicating with the Python CrewAI backend
 */

// Types for API requests and responses
export interface FeedbackRequest {
  user_id: string;
  challenge_id: string;
  selected_option: string;
  correct_option: string;
  locale: string;
  user_history?: Array<Record<string, any>>;
  context?: Record<string, any>;
}

export interface FeedbackResponse {
  feedback: string;
  reasoning?: string;
  learning_objectives?: string[];
  follow_up_questions?: string[];
  confidence_score?: number;
}

export interface DeepfakeChallengeRequest {
  user_id: string;
  difficulty_level?: number;
  locale: string;
}

export interface DeepfakeChallengeResponse {
  challenge_id: string;
  media_url: string;
  media_type: 'audio' | 'video' | 'image';
  is_deepfake: boolean;
  difficulty_level: number;
  detection_clues: string[];
}

export interface SocialMediaSimulationRequest {
  user_id: string;
  locale: string;
  preferences?: Record<string, any>;
}

export interface SocialMediaSimulationResponse {
  session_id: string;
  feed_content: Array<{
    post_id: string;
    content: string;
    author_profile: Record<string, any>;
    is_disinformation: boolean;
    category: string;
    engagement_metrics: Record<string, any>;
  }>;
}

export interface AnalyticsRequest {
  user_id: string;
  locale: string;
}

export interface AnalyticsResponse {
  competency_scores: Record<string, number>;
  learning_path: string[];
  achievements: Array<Record<string, any>>;
  trend_data: Array<Record<string, any>>;
  insights: Array<{
    insight_type: string;
    title: string;
    description: string;
    actionable_recommendations: string[];
    confidence_score: number;
  }>;
}

export interface APIError {
  error: string;
  details?: string;
  suggested_actions?: string[];
  fallback_available?: boolean;
}

class AIBackendClient {
  private baseUrl: string;
  private timeout: number;

  constructor() {
    // Use environment variable or default to localhost for development
    this.baseUrl = process.env.NEXT_PUBLIC_AI_BACKEND_URL || 'http://localhost:8000';
    this.timeout = 30000; // 30 seconds timeout
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers: defaultHeaders,
        signal: AbortSignal.timeout(this.timeout),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        // Handle specific error types
        if (error.name === 'AbortError' || error.message.includes('timeout')) {
          throw new Error('Request timeout - AI backend may be unavailable');
        }
        if (error.message.includes('Failed to fetch')) {
          throw new Error('Cannot connect to AI backend - service may be down');
        }
      }
      throw error;
    }
  }

  /**
   * Generate AI feedback for challenge responses
   */
  async generateFeedback(request: FeedbackRequest): Promise<FeedbackResponse> {
    return this.makeRequest<FeedbackResponse>('/api/v1/feedback', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Start a deepfake detection challenge
   */
  async startDeepfakeChallenge(request: DeepfakeChallengeRequest): Promise<DeepfakeChallengeResponse> {
    return this.makeRequest<DeepfakeChallengeResponse>('/api/v1/challenges/deepfake', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Submit deepfake detection result
   */
  async submitDeepfakeResult(challengeId: string, userDecision: boolean, userId: string): Promise<FeedbackResponse> {
    return this.makeRequest<FeedbackResponse>(`/api/v1/challenges/deepfake/${challengeId}/submit`, {
      method: 'POST',
      body: JSON.stringify({
        user_decision: userDecision,
        user_id: userId,
      }),
    });
  }

  /**
   * Start social media simulation
   */
  async startSocialMediaSimulation(request: SocialMediaSimulationRequest): Promise<SocialMediaSimulationResponse> {
    return this.makeRequest<SocialMediaSimulationResponse>('/api/v1/simulations/social-media', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get user analytics and progress insights
   */
  async getUserAnalytics(request: AnalyticsRequest): Promise<AnalyticsResponse> {
    return this.makeRequest<AnalyticsResponse>(`/api/v1/analytics/user/${request.user_id}`, {
      method: 'GET',
      headers: {
        'Accept-Language': request.locale,
      },
    });
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string; version: string }> {
    return this.makeRequest<{ status: string; version: string }>('/health');
  }

  /**
   * Check if AI backend is available
   */
  async isAvailable(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch {
      return false;
    }
  }
}

// Export singleton instance
export const aiBackendClient = new AIBackendClient();

// Export fallback functions for graceful degradation
export class FallbackService {
  static generateFallbackFeedback(
    selectedOption: string,
    correctOption: string,
    isCorrect: boolean,
    locale: string = 'en'
  ): FeedbackResponse {
    const messages = {
      en: {
        correct: `Great job! You correctly selected "${selectedOption}". This demonstrates your understanding of this cybersecurity concept.`,
        incorrect: `The correct answer is "${correctOption}". Understanding the difference between your selected answer and the correct one will help deepen your cybersecurity knowledge.`,
      },
      pt: {
        correct: `Excelente! Você selecionou corretamente "${selectedOption}". Isso demonstra sua compreensão deste conceito de cibersegurança.`,
        incorrect: `A resposta correta é "${correctOption}". Compreender a diferença entre sua resposta selecionada e a correta ajudará a aprofundar seu conhecimento em cibersegurança.`,
      },
    };

    const localeMessages = messages[locale as keyof typeof messages] || messages.en;
    const feedback = isCorrect ? localeMessages.correct : localeMessages.incorrect;

    return {
      feedback,
      confidence_score: 0.5, // Lower confidence for fallback
    };
  }

  static generateFallbackAnalytics(userId: string, locale: string = 'en'): AnalyticsResponse {
    const messages = {
      en: {
        insight_title: 'Analytics Unavailable',
        insight_description: 'AI analytics are currently unavailable. Your progress is still being tracked.',
        recommendation: 'Continue practicing to improve your cybersecurity skills.',
      },
      pt: {
        insight_title: 'Análises Indisponíveis',
        insight_description: 'As análises de IA estão atualmente indisponíveis. Seu progresso ainda está sendo acompanhado.',
        recommendation: 'Continue praticando para melhorar suas habilidades de cibersegurança.',
      },
    };

    const localeMessages = messages[locale as keyof typeof messages] || messages.en;

    return {
      competency_scores: {},
      learning_path: [],
      achievements: [],
      trend_data: [],
      insights: [
        {
          insight_type: 'fallback',
          title: localeMessages.insight_title,
          description: localeMessages.insight_description,
          actionable_recommendations: [localeMessages.recommendation],
          confidence_score: 0.0,
        },
      ],
    };
  }
}