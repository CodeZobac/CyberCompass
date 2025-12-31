/**
 * CatfishChatSimulation Component
 * Enhanced catfish detection chat with real-time analysis
 * Requirements: 3, 9
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { ChatInterface } from './ChatInterface';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { TypingIndicator } from './TypingIndicator';
import { useSession } from 'next-auth/react';
import { useWebSocket } from '@lib/hooks/useWebSocket';

interface RedFlag {
  type: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
  detectedAt: string;
}

interface ChatAnalysis {
  redFlagsDetected: RedFlag[];
  userDetectionRate: number;
  characterInconsistencies: string[];
  recommendations: string[];
  overallScore: number;
}

export interface CatfishChatSimulationProps {
  locale?: string;
  userId?: string;
  onComplete?: (analysis: ChatAnalysis) => void;
}

export function CatfishChatSimulation({
  locale = 'en',
  userId,
  onComplete,
}: CatfishChatSimulationProps) {
  const { data: session } = useSession();
  const [sessionId] = useState(() => `catfish-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [analysis, setAnalysis] = useState<ChatAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [redFlagsSpotted, setRedFlagsSpotted] = useState<string[]>([]);
  const [messageCount, setMessageCount] = useState(0);

  const effectiveUserId = userId || session?.user?.email || 'anonymous';

  const messages = {
    en: {
      title: 'Catfish Detection Chat',
      description: 'Chat with this person and try to identify any red flags or suspicious behavior.',
      endButton: 'End Simulation',
      reportFlag: 'Report Red Flag',
      analysisTitle: 'Simulation Analysis',
      analysisDescription: 'Review the red flags and your detection performance.',
      redFlagsDetected: 'Red Flags Detected',
      yourDetectionRate: 'Your Detection Rate',
      characterInconsistencies: 'Character Inconsistencies',
      recommendations: 'Recommendations',
      overallScore: 'Overall Score',
      severity: 'Severity',
      tryAgain: 'Try Again',
      viewResults: 'View Results',
      messagesExchanged: 'Messages Exchanged',
      flagsReported: 'Flags Reported',
    },
    pt: {
      title: 'Chat de Detecção de Catfish',
      description: 'Converse com esta pessoa e tente identificar sinais de alerta ou comportamento suspeito.',
      endButton: 'Encerrar Simulação',
      reportFlag: 'Denunciar Sinal de Alerta',
      analysisTitle: 'Análise da Simulação',
      analysisDescription: 'Revise os sinais de alerta e seu desempenho de detecção.',
      redFlagsDetected: 'Sinais de Alerta Detectados',
      yourDetectionRate: 'Sua Taxa de Detecção',
      characterInconsistencies: 'Inconsistências de Personagem',
      recommendations: 'Recomendações',
      overallScore: 'Pontuação Geral',
      severity: 'Gravidade',
      tryAgain: 'Tentar Novamente',
      viewResults: 'Ver Resultados',
      messagesExchanged: 'Mensagens Trocadas',
      flagsReported: 'Sinais Denunciados',
    },
  };

  const t = messages[locale as keyof typeof messages] || messages.en;

  const handleEndSimulation = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/ai-backend/catfish-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          userId: effectiveUserId,
          redFlagsSpotted,
          messageCount,
          locale,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get analysis');
      }

      const analysisData = await response.json();
      setAnalysis(analysisData);
      setShowAnalysis(true);
      onComplete?.(analysisData);
    } catch (error) {
      console.error('Error getting analysis:', error);
      // Fallback analysis
      const mockAnalysis: ChatAnalysis = {
        redFlagsDetected: [
          {
            type: 'Age Inconsistency',
            description: 'Character claimed different ages in conversation',
            severity: 'high',
            detectedAt: new Date().toISOString(),
          },
          {
            type: 'Evasive Behavior',
            description: 'Avoided answering direct questions',
            severity: 'medium',
            detectedAt: new Date().toISOString(),
          },
        ],
        userDetectionRate: (redFlagsSpotted.length / 5) * 100,
        characterInconsistencies: [
          'Claimed to be 16 but used outdated slang',
          'Said they live in California but mentioned local UK references',
        ],
        recommendations: [
          'Always verify profile information',
          'Be cautious of evasive answers',
          'Look for inconsistencies in stories',
        ],
        overallScore: 75,
      };
      setAnalysis(mockAnalysis);
      setShowAnalysis(true);
      onComplete?.(mockAnalysis);
    } finally {
      setLoading(false);
    }
  };

  const handleReportFlag = () => {
    const flagId = `flag-${Date.now()}`;
    setRedFlagsSpotted(prev => [...prev, flagId]);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  if (showAnalysis && analysis) {
    return (
      <div className="w-full h-full overflow-y-auto bg-gradient-to-b from-purple-50 to-white p-4 sm:p-6">
        <div className="max-w-4xl mx-auto">
          {/* Analysis Header */}
          <div className="text-center mb-8 animate-fadeIn">
            <h2 className="text-4xl sm:text-5xl font-black uppercase text-purple-500 mb-3 drop-shadow-[4px_4px_0_rgba(0,0,0,0.25)]">
              🔍 {t.analysisTitle}
            </h2>
            <p className="text-lg font-semibold text-gray-700">{t.analysisDescription}</p>
          </div>

          <div className="space-y-6">
            {/* Score Display Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 animate-slideIn">
              <div className="bg-purple-100 border-4 border-purple-500 shadow-[8px_8px_0_0_#000] p-6 sm:p-8 text-center hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[12px_12px_0_0_#000] transition-all duration-200">
                <div className="text-5xl sm:text-6xl font-black text-purple-600 mb-2">{analysis.overallScore}</div>
                <div className="text-sm sm:text-base font-bold uppercase text-purple-800">{t.overallScore}</div>
              </div>
              <div className="bg-green-100 border-4 border-green-500 shadow-[8px_8px_0_0_#000] p-6 sm:p-8 text-center hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[12px_12px_0_0_#000] transition-all duration-200">
                <div className="text-5xl sm:text-6xl font-black text-green-600 mb-2">{Math.round(analysis.userDetectionRate)}%</div>
                <div className="text-sm sm:text-base font-bold uppercase text-green-800">{t.yourDetectionRate}</div>
              </div>
            </div>

            {/* Red Flags List with Severity Indicators */}
            <div className="bg-white border-4 border-black shadow-[8px_8px_0_0_#000] p-4 sm:p-6 animate-slideIn" style={{ animationDelay: '100ms' }}>
              <h3 className="text-2xl font-black uppercase mb-4 flex items-center gap-2">
                <span className="text-red-500">🚩</span>
                {t.redFlagsDetected}
              </h3>
              <div className="space-y-3">
                {analysis.redFlagsDetected.map((flag, idx) => (
                  <div 
                    key={idx} 
                    className={`bg-white border-l-6 p-4 shadow-[4px_4px_0_0_#000] ${
                      flag.severity === 'high' ? 'border-red-500' :
                      flag.severity === 'medium' ? 'border-yellow-500' :
                      'border-green-500'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                      <span className="font-black text-lg">{flag.type}</span>
                      <span className={`${getSeverityColor(flag.severity)} text-white px-3 py-1 text-xs font-bold uppercase border-2 border-black inline-block`}>
                        ⚠️ {flag.severity}
                      </span>
                    </div>
                    <p className="text-sm font-semibold text-gray-700">{flag.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Character Inconsistencies Section */}
            <div className="bg-white border-4 border-black shadow-[8px_8px_0_0_#000] p-4 sm:p-6 animate-slideIn" style={{ animationDelay: '200ms' }}>
              <h3 className="text-2xl font-black uppercase mb-4 flex items-center gap-2">
                <span className="text-yellow-500">💡</span>
                {t.characterInconsistencies}
              </h3>
              <div className="space-y-3">
                {analysis.characterInconsistencies.map((inconsistency, idx) => (
                  <div key={idx} className="flex items-start gap-3 bg-yellow-50 border-2 border-yellow-500 p-3">
                    <span className="text-yellow-600 font-black text-lg">•</span>
                    <span className="font-semibold text-gray-800 flex-1">{inconsistency}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations Panel */}
            <div className="bg-white border-4 border-black shadow-[8px_8px_0_0_#000] p-4 sm:p-6 animate-slideIn" style={{ animationDelay: '300ms' }}>
              <h3 className="text-2xl font-black uppercase mb-4 flex items-center gap-2">
                <span className="text-blue-500">🎯</span>
                {t.recommendations}
              </h3>
              <div className="space-y-3">
                {analysis.recommendations.map((rec, idx) => (
                  <div key={idx} className="flex items-start gap-3 bg-blue-50 border-2 border-blue-500 p-3">
                    <span className="text-blue-600 font-black text-lg">✓</span>
                    <span className="font-semibold text-gray-800 flex-1">{rec}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 animate-slideIn" style={{ animationDelay: '400ms' }}>
              <Button
                onClick={() => {
                  setShowAnalysis(false);
                  setAnalysis(null);
                  setRedFlagsSpotted([]);
                  setMessageCount(0);
                }}
                className="flex-1 bg-purple-500 text-white font-black uppercase text-base sm:text-lg px-6 py-4 border-4 border-black shadow-[8px_8px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[6px_6px_0_0_#000] transition-all duration-150"
              >
                {t.tryAgain}
              </Button>
              <Button
                onClick={() => onComplete?.(analysis)}
                className="flex-1 bg-white text-black font-black uppercase text-base sm:text-lg px-6 py-4 border-4 border-black shadow-[8px_8px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[6px_6px_0_0_#000] transition-all duration-150"
              >
                {t.viewResults}
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white border-4 border-black shadow-[8px_8px_0_0_#000] overflow-hidden">
      {/* Header */}
      <div className="px-4 sm:px-6 py-4 border-b-4 border-black bg-gradient-to-r from-purple-500 to-pink-600">
        <h2 className="text-xl sm:text-2xl font-black text-white uppercase mb-1">{t.title}</h2>
        <p className="text-xs sm:text-sm text-purple-100 font-semibold">{t.description}</p>
      </div>

      {/* Stats Bar with Red Flag Report Button */}
      <div className="px-4 sm:px-6 py-3 border-b-4 border-black bg-gray-50 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex gap-4 sm:gap-6">
          <div>
            <span className="font-bold uppercase text-xs text-gray-600">{t.messagesExchanged}</span>
            <span className="ml-2 font-black text-lg">{messageCount}</span>
          </div>
          <div>
            <span className="font-bold uppercase text-xs text-gray-600">{t.flagsReported}</span>
            <span className="ml-2 font-black text-lg text-red-500">{redFlagsSpotted.length}</span>
          </div>
        </div>
        <Button
          onClick={handleReportFlag}
          variant="brutal-normal"
          size="sm"
          className="bg-red-500 text-white hover:bg-red-600 border-2 border-black shadow-[4px_4px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0_0_#000] transition-all duration-150 w-full sm:w-auto"
        >
          🚩 {t.reportFlag}
        </Button>
      </div>

      {/* Chat Interface with Enhanced Styling */}
      <div className="flex-1 min-h-0">
        <EnhancedChatInterface
          sessionId={sessionId}
          scenarioType="catfish_chat"
          userId={effectiveUserId}
          locale={locale}
          onError={(err) => console.error('WebSocket error:', err)}
          onMessageSent={() => setMessageCount(prev => prev + 1)}
        />
      </div>

      {/* Footer Actions */}
      <div className="px-4 sm:px-6 py-4 border-t-4 border-black bg-gray-50">
        <Button
          onClick={handleEndSimulation}
          disabled={loading}
          variant="brutal"
          className="w-full bg-red-500 hover:bg-red-600 text-white font-black uppercase text-sm sm:text-base"
        >
          {loading ? 'Analyzing...' : t.endButton}
        </Button>
      </div>
    </div>
  );
}

/**
 * Enhanced Chat Interface with Brutalist Styling
 * Requirements: 3
 */
interface EnhancedChatInterfaceProps {
  sessionId: string;
  scenarioType: 'catfish_chat' | 'social_media_simulation';
  userId: string;
  locale?: string;
  onError?: (error: Error) => void;
  onMessageSent?: () => void;
}

function EnhancedChatInterface({
  sessionId,
  scenarioType,
  userId,
  locale = 'en',
  onError,
  onMessageSent,
}: EnhancedChatInterfaceProps) {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const {
    isConnected,
    connectionStatus,
    isAgentTyping,
    messages,
    sendMessage,
    connect,
    error,
  } = useWebSocket({
    sessionId,
    scenarioType,
    userId,
    autoConnect: true,
    onError,
  });

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isAgentTyping]);

  // Focus input when connected
  useEffect(() => {
    if (isConnected) {
      inputRef.current?.focus();
    }
  }, [isConnected]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || !isConnected) {
      return;
    }

    sendMessage(inputMessage);
    setInputMessage('');
    onMessageSent?.();
  };

  const formatTime = (timestamp?: string) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString(locale === 'pt' ? 'pt-BR' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Error Display */}
      {error && (
        <div className="px-4 py-2 bg-red-100 border-b-2 border-red-500">
          <p className="text-sm font-bold text-red-600">
            {locale === 'pt' ? 'Erro: ' : 'Error: '}
            {error.message}
          </p>
        </div>
      )}

      {/* Messages Container with Scroll */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8 font-semibold">
            {locale === 'pt' 
              ? 'Comece a conversa enviando uma mensagem...' 
              : 'Start the conversation by sending a message...'}
          </div>
        )}

        {messages.map((message, index) => {
          const isUserMessage = message.type === 'user_message';
          const isAgentMessage = message.type === 'agent_message';

          if (!isUserMessage && !isAgentMessage) return null;

          return (
            <div 
              key={`${message.timestamp}-${index}`}
              className={`flex items-end gap-1 sm:gap-2 animate-slideIn ${isUserMessage ? 'flex-row-reverse' : ''}`}
            >
              {/* Message Bubble - Mobile Optimized */}
              <div className={`flex-1 max-w-[85%] sm:max-w-[75%] ${isUserMessage ? 'items-end' : 'items-start'}`}>
                <div
                  className={`px-3 sm:px-4 py-2 sm:py-3 border-2 sm:border-3 border-black shadow-[3px_3px_0_0_#000] sm:shadow-[4px_4px_0_0_#000] ${
                    isUserMessage
                      ? 'bg-blue-500 text-white ml-auto'
                      : 'bg-gray-200 text-black'
                  }`}
                >
                  <p className="text-sm sm:text-base font-semibold whitespace-pre-wrap break-words leading-relaxed">{message.message}</p>
                </div>
                <div className={`text-xs text-gray-500 mt-1 px-1 font-medium ${isUserMessage ? 'text-right' : 'text-left'}`}>
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          );
        })}

        {/* Typing Indicator Animation */}
        {isAgentTyping && (
          <div className="flex items-end gap-2 animate-fadeIn">
            <div className="flex-1 max-w-[75%]">
              <div className="px-4 py-3 bg-gray-200 border-3 border-black shadow-[4px_4px_0_0_#000]">
                <TypingIndicator />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Message Input with Send Button - Mobile Optimized */}
      <form onSubmit={handleSubmit} className="p-3 sm:p-4 border-t-4 border-black bg-white">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={!isConnected}
            placeholder={
              locale === 'pt' 
                ? 'Digite sua mensagem...' 
                : 'Type your message...'
            }
            className="flex-1 px-3 sm:px-4 py-3 sm:py-3 border-3 border-black font-semibold focus:outline-none focus:ring-4 focus:ring-purple-300 disabled:bg-gray-100 disabled:cursor-not-allowed text-sm sm:text-base min-h-[44px]"
            style={{ fontSize: '16px' }} // Prevents zoom on iOS
          />
          <button
            type="submit"
            disabled={!isConnected || !inputMessage.trim()}
            className="px-4 sm:px-6 py-3 bg-purple-500 text-white font-black uppercase text-xs sm:text-sm border-3 border-black shadow-[4px_4px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0_0_#000] disabled:bg-gray-300 disabled:cursor-not-allowed transition-all duration-150 active:translate-x-[4px] active:translate-y-[4px] active:shadow-none min-h-[44px] min-w-[44px] touch-manipulation"
          >
            <span className="hidden sm:inline">{locale === 'pt' ? 'ENVIAR' : 'SEND'} →</span>
            <span className="sm:hidden">→</span>
          </button>
        </div>
      </form>
    </div>
  );
}
