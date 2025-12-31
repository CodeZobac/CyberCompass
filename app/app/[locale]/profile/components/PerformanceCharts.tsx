'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import type { ProfileAnalytics, ChartDataPoint } from '@lib/types';

interface PerformanceChartsProps {
  analytics: ProfileAnalytics;
}

export function PerformanceCharts({ analytics }: PerformanceChartsProps) {
  const t = useTranslations('profile');

  // Prepare radar chart data for skill assessment
  const skillData: ChartDataPoint[] = analytics.categoryBreakdown.map(cat => ({
    name: cat.category,
    value: cat.accuracy,
    fullMark: 100
  }));

  // Prepare area chart data for progress over time
  const progressData: ChartDataPoint[] = analytics.recentActivity.map(activity => ({
    name: new Date(activity.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    value: activity.score,
    challenges: activity.challengesCompleted
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border-4 border-black shadow-brutal p-3">
          <p className="font-bold text-black mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value}
              {entry.payload.challenges && (
                <span className="text-gray-600"> ({entry.payload.challenges} challenges)</span>
              )}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-2xl font-black text-black mb-6 text-shadow-brutal">
        {t('performanceAnalysis')}
      </h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Skill Radar Chart */}
        <div className="space-y-4">
          <h4 className="text-lg font-bold text-black">{t('skillAssessment')}</h4>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={skillData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
                <PolarGrid stroke="#000" strokeWidth={2} />
                <PolarAngleAxis 
                  dataKey="name" 
                  tick={{ fontSize: 12, fontWeight: 'bold', fill: '#000' }}
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]}
                  tick={{ fontSize: 10, fontWeight: 'bold', fill: '#666' }}
                />
                <Radar
                  name="Accuracy"
                  dataKey="value"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.3}
                  strokeWidth={3}
                  dot={{ fill: '#3b82f6', strokeWidth: 2, stroke: '#000', r: 4 }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          
          {/* Skill Breakdown */}
          <div className="grid grid-cols-2 gap-2 text-xs">
            {analytics.categoryBreakdown.map((cat, index) => (
              <div 
                key={cat.categoryId}
                className={`text-center border-2 border-black p-2 ${
                  cat.accuracy >= 80 ? 'bg-green-100' : 
                  cat.accuracy >= 60 ? 'bg-yellow-100' : 'bg-red-100'
                }`}
              >
                <div className="font-black text-black">
                  {cat.accuracy.toFixed(1)}%
                </div>
                <div className="font-bold text-gray-700 uppercase">
                  {cat.category}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Progress Trend Area Chart */}
        <div className="space-y-4">
          <h4 className="text-lg font-bold text-black">{t('progressTrend')}</h4>
          {progressData.length > 0 ? (
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={progressData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#ccc" strokeWidth={2} />
                  <XAxis 
                    dataKey="name" 
                    tick={{ fontSize: 12, fontWeight: 'bold' }}
                    stroke="#000"
                    strokeWidth={2}
                  />
                  <YAxis 
                    tick={{ fontSize: 12, fontWeight: 'bold' }}
                    stroke="#000"
                    strokeWidth={2}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area 
                    type="monotone" 
                    dataKey="value" 
                    stroke="#10b981" 
                    fill="#10b981"
                    fillOpacity={0.3}
                    strokeWidth={3}
                    dot={{ fill: '#10b981', strokeWidth: 2, stroke: '#000', r: 4 }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-80 flex items-center justify-center border-2 border-dashed border-gray-300">
              <div className="text-center">
                <div className="text-4xl mb-2">📊</div>
                <p className="text-gray-600 font-bold">{t('noProgressData')}</p>
                <p className="text-sm text-gray-500">{t('completeMoreChallenges')}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Performance Insights */}
      <div className="mt-8 pt-6 border-t-4 border-black">
        <h4 className="text-lg font-bold text-black mb-4">{t('performanceInsights')}</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <motion.div 
            className="bg-blue-100 border-4 border-black shadow-brutal p-4 text-center"
            whileHover={{ scale: 1.02 }}
          >
            <div className="text-2xl mb-2">🎯</div>
            <div className="text-xl font-black text-blue-800">
              {analytics.averageScore.toFixed(1)}%
            </div>
            <div className="text-sm font-bold text-blue-700 uppercase">
              {t('avgAccuracy')}
            </div>
          </motion.div>

          <motion.div 
            className="bg-green-100 border-4 border-black shadow-brutal p-4 text-center"
            whileHover={{ scale: 1.02 }}
          >
            <div className="text-2xl mb-2">🏆</div>
            <div className="text-xl font-black text-green-800">
              {analytics.categoryBreakdown.filter(cat => cat.accuracy >= 80).length}
            </div>
            <div className="text-sm font-bold text-green-700 uppercase">
              {t('strongAreas')}
            </div>
          </motion.div>

          <motion.div 
            className="bg-yellow-100 border-4 border-black shadow-brutal p-4 text-center"
            whileHover={{ scale: 1.02 }}
          >
            <div className="text-2xl mb-2">📈</div>
            <div className="text-xl font-black text-yellow-800">
              {analytics.categoryBreakdown.filter(cat => cat.accuracy < 60).length}
            </div>
            <div className="text-sm font-bold text-yellow-700 uppercase">
              {t('improvementAreas')}
            </div>
          </motion.div>

          <motion.div 
            className="bg-purple-100 border-4 border-black shadow-brutal p-4 text-center"
            whileHover={{ scale: 1.02 }}
          >
            <div className="text-2xl mb-2">⚡</div>
            <div className="text-xl font-black text-purple-800">
              {analytics.ethicalDevelopmentScore}
            </div>
            <div className="text-sm font-bold text-purple-700 uppercase">
              {t('ethicalScore')}
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}
