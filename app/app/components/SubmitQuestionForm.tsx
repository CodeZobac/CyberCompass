'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface SubmitQuestionFormProps {
  onSuccess?: () => void;
}

export default function SubmitQuestionForm({ onSuccess }: SubmitQuestionFormProps) {
  const t = useTranslations('submitQuestion');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [messageType, setMessageType] = useState<'success' | 'error'>('success');
  
  const [formData, setFormData] = useState({
    language: 'en',
    title: '',
    description: '',
    category: '',
    options: ['', '', '', ''],
    correctAnswer: -1
  });

  const categories = [
    { value: 'catfishing', label: 'Catfishing' },
    { value: 'cyberbullying', label: 'Cyberbullying' },
    { value: 'deepfakes', label: 'Deepfakes' },
    { value: 'disinformation', label: 'Disinformation' }
  ];

  const handleOptionChange = (index: number, value: string) => {
    const newOptions = [...formData.options];
    newOptions[index] = value;
    setFormData({ ...formData, options: newOptions });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage(null);

    // Validate form
    if (!formData.title || !formData.description || !formData.category) {
      setMessage(t('form.validation.required'));
      setMessageType('error');
      setIsSubmitting(false);
      return;
    }

    if (formData.options.some(option => !option.trim())) {
      setMessage(t('form.validation.required'));
      setMessageType('error');
      setIsSubmitting(false);
      return;
    }

    if (formData.correctAnswer === -1) {
      setMessage(t('form.validation.selectCorrect'));
      setMessageType('error');
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch('/api/questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setMessage(t('success'));
        setMessageType('success');
        // Reset form
        setFormData({
          language: 'en',
          title: '',
          description: '',
          category: '',
          options: ['', '', '', ''],
          correctAnswer: -1
        });
        onSuccess?.();
      } else {
        setMessage(t('error'));
        setMessageType('error');
      }
    } catch (error) {
      console.error('Error submitting question:', error);
      setMessage(t('error'));
      setMessageType('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">{t('title')}</h2>
      
      {message && (
        <div className={`p-4 rounded mb-4 ${
          messageType === 'success' 
            ? 'bg-green-100 text-green-700 border border-green-300' 
            : 'bg-red-100 text-red-700 border border-red-300'
        }`}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Language Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('language')}
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                value="en"
                checked={formData.language === 'en'}
                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                className="mr-2"
              />
              English
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                value="pt"
                checked={formData.language === 'pt'}
                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                className="mr-2"
              />
              Português
            </label>
          </div>
        </div>

        {/* Title */}
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('form.title')}
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('form.description')}
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={4}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('form.category')}
          </label>
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            required
          >
            <option value="">{t('form.category')}</option>
            {categories.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>

        {/* Answer Options */}
        <div>
          <label className="block text-sm font-medium mb-2">
            {t('form.options')}
          </label>
          {formData.options.map((option, index) => (
            <div key={index} className="mb-3">
              <div className="flex items-center space-x-3">
                <input
                  type="radio"
                  name="correctAnswer"
                  checked={formData.correctAnswer === index}
                  onChange={() => setFormData({ ...formData, correctAnswer: index })}
                  className="mt-1"
                />
                <div className="flex-1">
                  <label className="block text-sm text-gray-600 mb-1">
                    {t('form.option')} {index + 1}
                  </label>
                  <input
                    type="text"
                    value={option}
                    onChange={(e) => handleOptionChange(index, e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
              </div>
            </div>
          ))}
          <p className="text-sm text-gray-600 mt-2">
            {t('form.correctAnswer')}
          </p>
        </div>

        <Button
          type="submit"
          disabled={isSubmitting}
          className="w-full"
        >
          {isSubmitting ? '...' : t('form.submit')}
        </Button>
      </form>
    </Card>
  );
}
