'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import { useState } from 'react';

interface ExportControlsProps {
  onExport: (format: 'json' | 'pdf') => void;
  isExporting: boolean;
}

export function ExportControls({ onExport, isExporting }: ExportControlsProps) {
  const t = useTranslations('profile');
  const [selectedFormat, setSelectedFormat] = useState<'json' | 'pdf'>('pdf');

  const handleExport = () => {
    onExport(selectedFormat);
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.7 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-xl font-black text-black mb-4 text-shadow-brutal">
        {t('exportProgress')}
      </h3>

      <div className="space-y-4">
        {/* Format Selection */}
        <div>
          <h4 className="text-sm font-bold text-black mb-3 uppercase">
            {t('selectFormat')}
          </h4>
          <div className="space-y-2">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelectedFormat('pdf')}
              className={`w-full p-3 border-2 border-black text-left transition-colors ${
                selectedFormat === 'pdf' 
                  ? 'bg-blue-400 text-black' 
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">📄</span>
                  <div>
                    <div className="font-bold text-sm">PDF Report</div>
                    <div className="text-xs text-gray-600">
                      {t('pdfDescription')}
                    </div>
                  </div>
                </div>
                <div className={`w-4 h-4 border-2 border-black rounded-full ${
                  selectedFormat === 'pdf' ? 'bg-black' : 'bg-white'
                }`} />
              </div>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSelectedFormat('json')}
              className={`w-full p-3 border-2 border-black text-left transition-colors ${
                selectedFormat === 'json' 
                  ? 'bg-green-400 text-black' 
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">💾</span>
                  <div>
                    <div className="font-bold text-sm">JSON Data</div>
                    <div className="text-xs text-gray-600">
                      {t('jsonDescription')}
                    </div>
                  </div>
                </div>
                <div className={`w-4 h-4 border-2 border-black rounded-full ${
                  selectedFormat === 'json' ? 'bg-black' : 'bg-white'
                }`} />
              </div>
            </motion.button>
          </div>
        </div>

        {/* Export Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleExport}
          disabled={isExporting}
          className={`w-full py-4 px-6 border-4 border-black shadow-brutal font-black uppercase text-sm tracking-wide transition-colors ${
            isExporting
              ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
              : selectedFormat === 'pdf'
              ? 'bg-blue-400 text-black hover:bg-blue-500'
              : 'bg-green-400 text-black hover:bg-green-500'
          }`}
        >
          {isExporting ? (
            <div className="flex items-center justify-center gap-2">
              <div className="animate-spin w-4 h-4 border-2 border-black border-t-transparent rounded-full" />
              {t('exporting')}...
            </div>
          ) : (
            <div className="flex items-center justify-center gap-2">
              <span>{selectedFormat === 'pdf' ? '📄' : '💾'}</span>
              {t('exportAs', { format: selectedFormat.toUpperCase() })}
            </div>
          )}
        </motion.button>

        {/* Export Info */}
        <div className="bg-gray-100 border-2 border-black p-3">
          <h4 className="text-sm font-bold text-black mb-2 uppercase">
            {t('whatsIncluded')}
          </h4>
          <div className="space-y-1 text-xs text-gray-700">
            <div className="flex items-center gap-2">
              <span className="text-blue-500">✓</span>
              <span>{t('progressAnalytics')}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              <span>{t('categoryBreakdown')}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-purple-500">✓</span>
              <span>{t('achievementHistory')}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-yellow-500">✓</span>
              <span>{t('learningRecommendations')}</span>
            </div>
          </div>
        </div>

        {/* Sharing Section */}
        <div className="pt-4 border-t-2 border-black">
          <h4 className="text-sm font-bold text-black mb-3 uppercase">
            {t('shareProgress')}
          </h4>
          <div className="grid grid-cols-2 gap-2">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="p-2 bg-blue-500 text-white border-2 border-black shadow-brutal text-xs font-bold uppercase"
              onClick={() => {
                if (navigator.share) {
                  navigator.share({
                    title: 'My CyberCompass Progress',
                    text: 'Check out my cybersecurity learning progress!',
                    url: window.location.href
                  });
                }
              }}
            >
              <div className="flex items-center justify-center gap-1">
                <span>📱</span>
                <span>{t('share')}</span>
              </div>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="p-2 bg-gray-800 text-white border-2 border-black shadow-brutal text-xs font-bold uppercase"
              onClick={() => {
                navigator.clipboard.writeText(window.location.href);
                // Could add a toast notification here
              }}
            >
              <div className="flex items-center justify-center gap-1">
                <span>🔗</span>
                <span>{t('copy')}</span>
              </div>
            </motion.button>
          </div>
        </div>

        {/* Privacy Note */}
        <div className="bg-yellow-50 border-2 border-yellow-400 p-3">
          <div className="flex items-start gap-2">
            <span className="text-yellow-500">🔒</span>
            <div className="text-xs text-gray-700">
              <p className="font-bold text-yellow-800 mb-1">{t('privacyNote')}</p>
              <p>{t('privacyDescription')}</p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
