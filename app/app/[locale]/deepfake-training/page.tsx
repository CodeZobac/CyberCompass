/**
 * Deepfake Detection Training Page
 * Interactive deepfake detection challenges
 */

import { DeepfakeDetectionChallenge } from '@/components/DeepfakeDetectionChallenge';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';

interface PageProps {
  params: Promise<{
    locale: string;
  }>;
}

export default async function DeepfakeTrainingPage({ params }: PageProps) {
  const session = await getServerSession(authOptions);
  const { locale } = await params;

  return (
    <div className="min-h-screen bg-white py-12 px-4">
      <div className="container mx-auto">
        {/* Page Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-black uppercase text-red-500 mb-4">
            {locale === 'pt' ? 'Treinamento de Detecção de Deepfake' : 'Deepfake Detection Training'}
          </h1>
          <p className="text-xl font-semibold text-gray-700 max-w-3xl mx-auto">
            {locale === 'pt'
              ? 'Aprenda a identificar deepfakes através de desafios interativos. Analise mídia e desenvolva suas habilidades de detecção.'
              : 'Learn to identify deepfakes through interactive challenges. Analyze media and develop your detection skills.'}
          </p>
        </div>

        {/* Challenge Component */}
        <DeepfakeDetectionChallenge
          locale={locale}
          userId={session?.user?.id}
          onComplete={(result) => {
            console.log('Training completed:', result);
            // Handle completion - could redirect to results page
          }}
        />
      </div>
    </div>
  );
}
