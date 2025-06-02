'use client';

import { useEffect, useState } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { useParams } from 'next/navigation';
import Header from '../../../components/Header';

interface PendingChallenge {
  id: string;
  title: string;
  description: string;
  options: Array<{ content: string; is_correct: boolean }>;
  status: 'pending' | 'approved' | 'rejected';
  submitted_at: string;
  submitted_language: 'en' | 'pt';
  assigned_category_id: string;
  submitted_by_user: {
    name: string;
    email: string;
  };
  assigned_category: {
    name: string;
    slug: string;
  };
}

interface ReviewModalData {
  question: PendingChallenge;
  translatedTitleEn: string;
  translatedTitlePt: string;
  translatedDescriptionEn: string;
  translatedDescriptionPt: string;
  translatedOptions: {
    en: string[];
    pt: string[];
  };
  difficulty: number;
}

export default function AdminQuestions() {
  const params = useParams();
  const locale = params.locale as string || 'en';
  const [questions, setQuestions] = useState<PendingChallenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<'pending' | 'approved' | 'rejected'>('pending');
  const [reviewModal, setReviewModal] = useState<ReviewModalData | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Translations (using fallback text since we can't use getTranslations in client component)
  const t = {
    title: locale === 'pt' ? 'Rever Perguntas' : 'Review Questions',
    submittedBy: locale === 'pt' ? 'Submetido por' : 'Submitted by',
    submittedAt: locale === 'pt' ? 'Submetido em' : 'Submitted at',
    originalLanguage: locale === 'pt' ? 'Idioma Original' : 'Original Language',
    correctAnswer: locale === 'pt' ? 'Resposta Correta' : 'Correct Answer',
    difficulty: locale === 'pt' ? 'Dificuldade' : 'Difficulty',
    approve: locale === 'pt' ? 'Aprovar e Criar Desafio' : 'Approve & Create Challenge',
    reject: locale === 'pt' ? 'Rejeitar' : 'Reject',
    translate: locale === 'pt' ? 'Traduzir' : 'Translate',
    pending: locale === 'pt' ? 'Pendentes' : 'Pending',
    approved: locale === 'pt' ? 'Aprovadas' : 'Approved',
    rejected: locale === 'pt' ? 'Rejeitadas' : 'Rejected',
    translationForm: {
      english: locale === 'pt' ? 'Tradução em Inglês' : 'English Translation',
      portuguese: locale === 'pt' ? 'Tradução em Português' : 'Portuguese Translation'
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, [selectedStatus]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/admin/questions?status=${selectedStatus}`);
      if (!response.ok) {
        throw new Error('Failed to fetch questions');
      }
      const data = await response.json();
      setQuestions(data.questions || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const openReviewModal = (question: PendingChallenge) => {
    setReviewModal({
      question,
      translatedTitleEn: question.submitted_language === 'en' ? question.title : '',
      translatedTitlePt: question.submitted_language === 'pt' ? question.title : '',
      translatedDescriptionEn: question.submitted_language === 'en' ? question.description : '',
      translatedDescriptionPt: question.submitted_language === 'pt' ? question.description : '',
      translatedOptions: {
        en: question.submitted_language === 'en' ? question.options.map(opt => opt.content) : ['', '', '', ''],
        pt: question.submitted_language === 'pt' ? question.options.map(opt => opt.content) : ['', '', '', '']
      },
      difficulty: 1
    });
  };

  const handleApprove = async () => {
    if (!reviewModal || isProcessing) return;

    try {
      setIsProcessing(true);
      const response = await fetch(`/api/admin/questions/${reviewModal.question.id}/approve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          translatedTitleEn: reviewModal.translatedTitleEn,
          translatedTitlePt: reviewModal.translatedTitlePt,
          translatedDescriptionEn: reviewModal.translatedDescriptionEn,
          translatedDescriptionPt: reviewModal.translatedDescriptionPt,
          translatedOptions: reviewModal.translatedOptions,
          difficulty: reviewModal.difficulty,
          categoryId: reviewModal.question.assigned_category_id
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to approve question');
      }

      setReviewModal(null);
      fetchQuestions();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to approve question');
    } finally {
      setIsProcessing(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString(locale === 'pt' ? 'pt-PT' : 'en-US');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto px-6 py-12">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-500 rounded-xl border-4 border-black shadow-[4px_4px_0_0_#000] flex items-center justify-center mx-auto mb-4 animate-bounce">
              <span className="text-white text-2xl font-bold">⏳</span>
            </div>
            <p className="text-xl font-bold text-gray-900">
              {locale === 'pt' ? 'A carregar...' : 'Loading...'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      {/* Header Section */}
      <div className="bg-white border-b-4 border-black shadow-[0_4px_0_0_#000]">
        <div className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight flex items-center">
                📝 {t.title}
              </h1>
              <p className="text-lg text-gray-600">
                {locale === 'pt' 
                  ? 'Gerencie e revise todas as perguntas submetidas pelos utilizadores'
                  : 'Manage and review all questions submitted by users'
                }
              </p>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <div className="bg-blue-100 border-2 border-blue-600 rounded-lg px-4 py-2">
                <span className="text-blue-800 font-semibold text-sm uppercase tracking-wider">
                  📊 {questions.length} {locale === 'pt' ? 'Total' : 'Total'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-12">
        {/* Enhanced Status Tabs */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            🏷️ {locale === 'pt' ? 'Filtrar por Estado' : 'Filter by Status'}
          </h2>
          <div className="flex flex-wrap gap-4">
            {(['pending', 'approved', 'rejected'] as const).map((status) => (
              <button
                key={status}
                onClick={() => setSelectedStatus(status)}
                className={`px-6 py-3 rounded-lg font-bold text-lg uppercase tracking-wide border-4 transition-all duration-200 ${
                  selectedStatus === status
                    ? status === 'pending' 
                      ? 'bg-orange-500 text-white border-orange-600 shadow-[4px_4px_0_0_#ea580c]'
                      : status === 'approved'
                      ? 'bg-green-500 text-white border-green-600 shadow-[4px_4px_0_0_#16a34a]'
                      : 'bg-red-500 text-white border-red-600 shadow-[4px_4px_0_0_#dc2626]'
                    : 'bg-white text-gray-700 border-gray-300 shadow-[4px_4px_0_0_#9ca3af] hover:translate-x-1 hover:translate-y-1 hover:shadow-[2px_2px_0_0_#9ca3af]'
                }`}
              >
                {status === 'pending' ? '⏳' : status === 'approved' ? '✅' : '❌'} {t[status]}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="mb-8 p-6 bg-red-50 border-4 border-red-500 rounded-lg shadow-[8px_8px_0_0_#dc2626]">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-red-500 rounded-lg border-2 border-black flex items-center justify-center mr-4">
                <span className="text-white text-xl font-bold">⚠️</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-red-900 mb-1">
                  {locale === 'pt' ? 'Erro' : 'Error'}
                </h3>
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Enhanced Questions List */}
        <div className="space-y-8">
          {questions.length === 0 ? (
            <Card className="p-12 text-center bg-gradient-to-br from-gray-50 to-slate-50 border-4 border-gray-400 shadow-[8px_8px_0_0_#6b7280]">
              <div className="w-24 h-24 bg-gray-400 rounded-xl border-4 border-black shadow-[4px_4px_0_0_#000] flex items-center justify-center mx-auto mb-6">
                <span className="text-white text-3xl font-bold">📭</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3 uppercase tracking-wide">
                {locale === 'pt' ? 'Nenhuma Pergunta Encontrada' : 'No Questions Found'}
              </h3>
              <p className="text-gray-600 text-lg">
                {locale === 'pt' 
                  ? `Nenhuma pergunta ${selectedStatus === 'pending' ? 'pendente' : selectedStatus === 'approved' ? 'aprovada' : 'rejeitada'} encontrada.`
                  : `No ${selectedStatus} questions found.`
                }
              </p>
            </Card>
          ) : (
            questions.map((question) => (
              <Card key={question.id} className={`p-8 bg-gradient-to-br border-4 shadow-[8px_8px_0_0_#000] hover:shadow-[4px_4px_0_0_#000] hover:translate-x-1 hover:translate-y-1 transition-all duration-200 ${
                question.status === 'pending' 
                  ? 'from-orange-50 to-yellow-50 border-orange-400'
                  : question.status === 'approved'
                  ? 'from-green-50 to-emerald-50 border-green-400'
                  : 'from-red-50 to-pink-50 border-red-400'
              }`}>
                <div className="flex justify-between items-start mb-6">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4 mb-4">
                      <div className={`w-12 h-12 rounded-lg border-2 border-black flex items-center justify-center ${
                        question.status === 'pending' ? 'bg-orange-500' :
                        question.status === 'approved' ? 'bg-green-500' : 'bg-red-500'
                      }`}>
                        <span className="text-white text-xl font-bold">
                          {question.status === 'pending' ? '⏳' : question.status === 'approved' ? '✅' : '❌'}
                        </span>
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-gray-900 uppercase tracking-wide">
                          {question.title}
                        </h3>
                        <p className="text-sm text-gray-600 font-medium">
                          ID: {question.id.substring(0, 8)}...
                        </p>
                      </div>
                    </div>
                    <p className="text-gray-700 mb-6 text-lg leading-relaxed bg-white p-4 rounded-lg border-2 border-gray-300">
                      {question.description}
                    </p>
                  </div>
                  <div className="ml-6">
                    <span className={`inline-block px-4 py-2 rounded-lg text-sm font-bold uppercase tracking-wider border-2 ${
                      question.status === 'pending' 
                        ? 'bg-orange-200 text-orange-800 border-orange-600'
                        : question.status === 'approved' 
                        ? 'bg-green-200 text-green-800 border-green-600'
                        : 'bg-red-200 text-red-800 border-red-600'
                    }`}>
                      {question.status}
                    </span>
                  </div>
                </div>

                {/* Enhanced Info Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div className="bg-white p-4 rounded-lg border-2 border-gray-300 shadow-[4px_4px_0_0_#9ca3af]">
                    <h4 className="font-bold text-gray-900 mb-2 uppercase tracking-wider text-sm">
                      👤 {locale === 'pt' ? 'Informações do Submissor' : 'Submitter Info'}
                    </h4>
                    <p className="text-gray-700 font-medium">
                      <strong>{t.submittedBy}:</strong> {question.submitted_by_user?.name || 'Unknown'}
                    </p>
                    <p className="text-gray-700 font-medium">
                      <strong>{t.submittedAt}:</strong> {formatDate(question.submitted_at)}
                    </p>
                  </div>
                  <div className="bg-white p-4 rounded-lg border-2 border-gray-300 shadow-[4px_4px_0_0_#9ca3af]">
                    <h4 className="font-bold text-gray-900 mb-2 uppercase tracking-wider text-sm">
                      🏷️ {locale === 'pt' ? 'Detalhes da Pergunta' : 'Question Details'}
                    </h4>
                    <p className="text-gray-700 font-medium">
                      <strong>{t.originalLanguage}:</strong> 
                      <span className={`ml-2 px-2 py-1 rounded text-xs font-bold ${
                        question.submitted_language === 'en' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                      }`}>
                        {question.submitted_language?.toUpperCase()}
                      </span>
                    </p>
                    <p className="text-gray-700 font-medium">
                      <strong>Category:</strong> {question.assigned_category?.name || 'Unknown'}
                    </p>
                  </div>
                </div>

                {/* Enhanced Options Display */}
                <div className="mb-6">
                  <h4 className="font-bold text-gray-900 mb-4 uppercase tracking-wider flex items-center">
                    📝 {locale === 'pt' ? 'Opções de Resposta' : 'Answer Options'}
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {question.options?.map((option, index) => (
                      <div key={index} className={`p-4 rounded-lg border-2 font-medium ${
                        option.is_correct 
                          ? 'bg-green-100 border-green-500 text-green-900 shadow-[4px_4px_0_0_#16a34a]' 
                          : 'bg-gray-100 border-gray-300 text-gray-800 shadow-[4px_4px_0_0_#9ca3af]'
                      }`}>
                        <div className="flex items-center justify-between">
                          <span className="flex-1">{option.content}</span>
                          {option.is_correct && (
                            <div className="ml-3 flex items-center">
                              <span className="bg-green-600 text-white px-2 py-1 rounded text-xs font-bold border-2 border-black">
                                ✅ {t.correctAnswer}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Enhanced Action Buttons */}
                {question.status === 'pending' && (
                  <div className="flex flex-wrap gap-4 pt-4 border-t-2 border-gray-300">
                    <Button 
                      onClick={() => openReviewModal(question)}
                      variant="brutal"
                      className="flex-1 md:flex-none text-lg font-bold tracking-wide uppercase"
                    >
                      🔍 {t.translate} & {t.approve}
                    </Button>
                    <Button 
                      variant="destructive"
                      className="flex-1 md:flex-none text-lg font-bold tracking-wide uppercase border-4 border-red-600 shadow-[4px_4px_0_0_#dc2626] hover:shadow-[2px_2px_0_0_#dc2626] hover:translate-x-1 hover:translate-y-1"
                      onClick={() => {/* TODO: implement reject */}}
                    >
                      ❌ {t.reject}
                    </Button>
                  </div>
                )}
              </Card>
            ))
          )}
        </div>

        {/* Enhanced Review Modal */}
        {reviewModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-y-auto border-4 border-black shadow-[8px_8px_0_0_#000]">
              <div className="p-8">
                <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-gray-300">
                  <h2 className="text-3xl font-black text-gray-900 uppercase tracking-wide flex items-center">
                    🔍 {t.translate} & {t.approve}
                  </h2>
                  <button
                    onClick={() => setReviewModal(null)}
                    className="w-10 h-10 bg-red-500 rounded-lg border-2 border-black flex items-center justify-center hover:bg-red-600 transition-colors"
                  >
                    <span className="text-white font-bold">✕</span>
                  </button>
                </div>

                <div className="space-y-8">
                  {/* Enhanced Original Content */}
                  <div>
                    <h3 className="text-xl font-bold mb-4 uppercase tracking-wide flex items-center text-gray-900">
                      📄 {locale === 'pt' ? 'Conteúdo Original' : 'Original Content'}
                    </h3>
                    <div className="bg-gray-50 p-6 rounded-lg border-4 border-gray-300 shadow-[4px_4px_0_0_#9ca3af]">
                      <div className="space-y-3">
                        <p className="font-medium"><strong>Title:</strong> {reviewModal.question.title}</p>
                        <p className="font-medium"><strong>Description:</strong> {reviewModal.question.description}</p>
                        <p className="font-medium">
                          <strong>Language:</strong> 
                          <span className={`ml-2 px-3 py-1 rounded font-bold ${
                            reviewModal.question.submitted_language === 'en' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                          }`}>
                            {reviewModal.question.submitted_language?.toUpperCase()}
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Enhanced Translation Forms */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="bg-blue-50 p-6 rounded-lg border-4 border-blue-300 shadow-[4px_4px_0_0_#3b82f6]">
                      <h4 className="font-bold mb-4 text-xl uppercase tracking-wide text-blue-900 flex items-center">
                        🇺🇸 {t.translationForm.english}
                      </h4>
                      <div className="space-y-4">
                        <input
                          type="text"
                          placeholder="English Title"
                          value={reviewModal.translatedTitleEn}
                          onChange={(e) => setReviewModal(prev => prev ? {...prev, translatedTitleEn: e.target.value} : null)}
                          className="w-full p-3 border-2 border-gray-300 rounded-lg font-medium focus:border-blue-500 focus:outline-none"
                        />
                        <textarea
                          placeholder="English Description"
                          value={reviewModal.translatedDescriptionEn}
                          onChange={(e) => setReviewModal(prev => prev ? {...prev, translatedDescriptionEn: e.target.value} : null)}
                          className="w-full p-3 border-2 border-gray-300 rounded-lg h-32 font-medium focus:border-blue-500 focus:outline-none"
                        />
                        {reviewModal.translatedOptions.en.map((option, index) => (
                          <input
                            key={index}
                            type="text"
                            placeholder={`English Option ${index + 1}`}
                            value={option}
                            onChange={(e) => {
                              const newOptions = {...reviewModal.translatedOptions};
                              newOptions.en[index] = e.target.value;
                              setReviewModal(prev => prev ? {...prev, translatedOptions: newOptions} : null);
                            }}
                            className="w-full p-3 border-2 border-gray-300 rounded-lg font-medium focus:border-blue-500 focus:outline-none"
                          />
                        ))}
                      </div>
                    </div>

                    <div className="bg-green-50 p-6 rounded-lg border-4 border-green-300 shadow-[4px_4px_0_0_#16a34a]">
                      <h4 className="font-bold mb-4 text-xl uppercase tracking-wide text-green-900 flex items-center">
                        🇵🇹 {t.translationForm.portuguese}
                      </h4>
                      <div className="space-y-4">
                        <input
                          type="text"
                          placeholder="Portuguese Title"
                          value={reviewModal.translatedTitlePt}
                          onChange={(e) => setReviewModal(prev => prev ? {...prev, translatedTitlePt: e.target.value} : null)}
                          className="w-full p-3 border-2 border-gray-300 rounded-lg font-medium focus:border-green-500 focus:outline-none"
                        />
                        <textarea
                          placeholder="Portuguese Description"
                          value={reviewModal.translatedDescriptionPt}
                          onChange={(e) => setReviewModal(prev => prev ? {...prev, translatedDescriptionPt: e.target.value} : null)}
                          className="w-full p-3 border-2 border-gray-300 rounded-lg h-32 font-medium focus:border-green-500 focus:outline-none"
                        />
                        {reviewModal.translatedOptions.pt.map((option, index) => (
                          <input
                            key={index}
                            type="text"
                            placeholder={`Portuguese Option ${index + 1}`}
                            value={option}
                            onChange={(e) => {
                              const newOptions = {...reviewModal.translatedOptions};
                              newOptions.pt[index] = e.target.value;
                              setReviewModal(prev => prev ? {...prev, translatedOptions: newOptions} : null);
                            }}
                            className="w-full p-3 border-2 border-gray-300 rounded-lg font-medium focus:border-green-500 focus:outline-none"
                          />
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Enhanced Difficulty Selector */}
                  <div className="bg-purple-50 p-6 rounded-lg border-4 border-purple-300 shadow-[4px_4px_0_0_#8b5cf6]">
                    <label className="block font-bold mb-4 text-xl uppercase tracking-wide text-purple-900 flex items-center">
                      ⚡ {t.difficulty}
                    </label>
                    <select
                      value={reviewModal.difficulty}
                      onChange={(e) => setReviewModal(prev => prev ? {...prev, difficulty: parseInt(e.target.value)} : null)}
                      className="w-48 p-3 border-4 border-purple-400 rounded-lg font-bold text-lg bg-white focus:outline-none focus:border-purple-600"
                    >
                      <option value={1}>1 - 🟢 Easy</option>
                      <option value={2}>2 - 🟡 Medium</option>
                      <option value={3}>3 - 🔴 Hard</option>
                    </select>
                  </div>

                  {/* Enhanced Actions */}
                  <div className="flex justify-end space-x-4 pt-6 border-t-4 border-gray-300">
                    <Button
                      variant="brutal-normal"
                      onClick={() => setReviewModal(null)}
                      disabled={isProcessing}
                      className="text-lg font-bold tracking-wide uppercase"
                    >
                      ❌ Cancel
                    </Button>
                    <Button
                      onClick={handleApprove}
                      disabled={isProcessing}
                      variant="brutal"
                      className="text-lg font-bold tracking-wide uppercase bg-green-500 hover:bg-green-600"
                    >
                      {isProcessing ? '⏳ Processing...' : `✅ ${t.approve}`}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
    </>
  );
}
