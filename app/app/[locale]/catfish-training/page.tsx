/**
 * Catfish Detection Training Page
 * Interactive chat simulation for catfish detection
 * Requirements: 3
 */

import { CatfishChatSimulation } from '@/components/CatfishChatSimulation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

interface PageProps {
  params: Promise<{
    locale: string;
  }>;
}

export default async function CatfishTrainingPage({ params }: PageProps) {
  const session = await getServerSession(authOptions);
  const { locale } = await params;

  const content = {
    en: {
      title: 'CATFISH DETECTION TRAINING',
      subtitle: 'Learn to spot red flags in online conversations',
      features: [
        { icon: '🎭', text: 'Chat with suspicious characters' },
        { icon: '🚩', text: 'Identify red flags in real-time' },
        { icon: '📊', text: 'Get detailed performance analysis' },
      ],
      cta: 'START CHAT SIMULATION',
    },
    pt: {
      title: 'TREINAMENTO DE DETECÇÃO DE CATFISH',
      subtitle: 'Aprenda a identificar sinais de alerta em conversas online',
      features: [
        { icon: '🎭', text: 'Converse com personagens suspeitos' },
        { icon: '🚩', text: 'Identifique sinais de alerta em tempo real' },
        { icon: '📊', text: 'Obtenha análise detalhada de desempenho' },
      ],
      cta: 'INICIAR SIMULAÇÃO DE CHAT',
    },
  };

  const t = content[locale as keyof typeof content] || content.en;

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white">
      {/* Hero Section */}
      <div className="border-b-6 border-black bg-gradient-to-r from-purple-50 to-pink-50 py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-6xl">
          {/* Title with purple accent */}
          <h1 className="text-5xl sm:text-6xl md:text-8xl font-black uppercase text-purple-500 mb-6 text-center leading-tight drop-shadow-[4px_4px_0_rgba(0,0,0,0.25)]">
            💬 {t.title}
          </h1>

          {/* Subtitle */}
          <p className="text-xl sm:text-2xl font-semibold text-gray-700 text-center max-w-3xl mx-auto mb-12">
            {t.subtitle}
          </p>

          {/* Feature list with icons - messaging app inspired */}
          <div className="max-w-2xl mx-auto mb-12">
            <div className="bg-purple-100 border-4 border-purple-500 shadow-[8px_8px_0_0_#000] p-6 sm:p-8">
              <div className="space-y-4">
                {t.features.map((feature, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-4 bg-white border-2 border-black p-4 shadow-[4px_4px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0_0_#000] transition-all duration-150"
                  >
                    <span className="text-4xl">{feature.icon}</span>
                    <span className="text-lg font-bold text-gray-800">{feature.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* CTA Button */}
          <div className="text-center">
            <a
              href="#chat-simulation"
              className="inline-block bg-purple-500 text-white font-black text-lg sm:text-xl uppercase px-8 sm:px-12 py-4 sm:py-6 border-4 border-black shadow-[8px_8px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[6px_6px_0_0_#000] transition-all duration-150 active:translate-x-[4px] active:translate-y-[4px] active:shadow-[4px_4px_0_0_#000]"
            >
              {t.cta} →
            </a>
          </div>
        </div>
      </div>

      {/* Chat Simulation Section */}
      <div id="chat-simulation" className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-6xl">
          <div className="max-w-4xl mx-auto" style={{ height: '700px' }}>
            <CatfishChatSimulation
              locale={locale}
              userId={session?.user?.id}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
