/**
 * Social Media Simulation Page
 * Interactive disinformation detection training
 */

import { SocialMediaSimulation } from '@/components/SocialMediaSimulation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

interface PageProps {
  params: Promise<{
    locale: string;
  }>;
}

export default async function SocialMediaSimPage({ params }: PageProps) {
  const session = await getServerSession(authOptions);
  const { locale } = await params;

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section - Responsive layout adjustments */}
      <div className="border-b-4 sm:border-b-6 border-black bg-gradient-to-r from-blue-50 to-white py-12 sm:py-16 lg:py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-5xl">
          {/* Title with blue accent - Adjusted for small screens */}
          <h1 className="text-4xl xs:text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-black uppercase text-blue-500 mb-4 sm:mb-6 text-center drop-shadow-[2px_2px_0_rgba(0,0,0,1)] sm:drop-shadow-[4px_4px_0_rgba(0,0,0,1)] leading-tight">
            <span className="text-3xl xs:text-4xl sm:text-5xl lg:text-6xl">📱</span>
            <br className="sm:hidden" />
            {locale === 'pt' ? 'Simulação de Mídia Social' : 'Social Media Simulation'}
          </h1>

          {/* Simulation description - Adjusted font sizes */}
          <p className="text-lg xs:text-xl sm:text-2xl font-semibold text-gray-700 text-center mb-6 sm:mb-8 max-w-3xl mx-auto px-2">
            {locale === 'pt'
              ? 'Navegue pelo feed. Identifique as mentiras.'
              : 'Navigate the feed. Spot the lies.'}
          </p>

          {/* Info box with key features - Adjusted for mobile */}
          <div className="bg-blue-100 border-3 sm:border-4 border-blue-500 p-4 sm:p-6 shadow-[4px_4px_0_0_#000] sm:shadow-[8px_8px_0_0_#000] max-w-2xl mx-auto mb-6 sm:mb-8">
            <p className="font-semibold text-sm sm:text-base text-gray-800 mb-3 sm:mb-4 text-center leading-relaxed">
              {locale === 'pt'
                ? 'Teste seu pensamento crítico em um ambiente simulado de mídia social repleto de conteúdo autêntico e desinformação.'
                : 'Test your critical thinking in a simulated social media environment filled with both authentic content and disinformation.'}
            </p>
            <div className="grid grid-cols-1 xs:grid-cols-3 gap-2 sm:gap-3 text-xs sm:text-sm font-bold">
              <div className="flex items-center justify-center xs:justify-start gap-2 bg-white bg-opacity-50 p-2 rounded">
                <span className="text-xl sm:text-2xl">🎭</span>
                <span>{locale === 'pt' ? 'Conteúdo Realista' : 'Realistic Content'}</span>
              </div>
              <div className="flex items-center justify-center xs:justify-start gap-2 bg-white bg-opacity-50 p-2 rounded">
                <span className="text-xl sm:text-2xl">🧠</span>
                <span>{locale === 'pt' ? 'Pensamento Crítico' : 'Critical Thinking'}</span>
              </div>
              <div className="flex items-center justify-center xs:justify-start gap-2 bg-white bg-opacity-50 p-2 rounded">
                <span className="text-xl sm:text-2xl">📊</span>
                <span>{locale === 'pt' ? 'Análise Detalhada' : 'Detailed Analysis'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Adjusted padding for mobile */}
      <div className="container mx-auto py-6 sm:py-8 lg:py-12 px-3 sm:px-4">
        <SocialMediaSimulation
          locale={locale}
          userId={session?.user?.id}
        />
      </div>
    </div>
  );
}
