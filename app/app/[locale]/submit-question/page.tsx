import { getTranslations } from 'next-intl/server';
import SubmitQuestionForm from '../../components/SubmitQuestionForm';

export default async function SubmitQuestionPage() {
  const t = await getTranslations('submitQuestion');

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            {t('title')}
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Help us improve CyberCompass by submitting your own cybersecurity questions. 
            Our team will review and potentially include them in our challenge database.
          </p>
        </div>
        
        <SubmitQuestionForm />
      </div>
    </div>
  );
}
