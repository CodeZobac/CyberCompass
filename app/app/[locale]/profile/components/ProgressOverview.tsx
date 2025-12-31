'use client';

import { motion } from 'framer-motion';
import { useTranslations } from 'next-intl';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LineChart, Line } from 'recharts';
import type { ProfileAnalytics, ChartDataPoint } from '@lib/types';

interface ProgressOverviewProps {
  analytics: ProfileAnalytics;
}

const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#6b7280'];

export function ProgressOverview({ analytics }: ProgressOverviewProps) {
  const t = useTranslations('profile');

  // Prepare data for charts
  const completionData: ChartDataPoint[] = [
    { name: t('completed'), value: analytics.completedChallenges },
    { name: t('remaining'), value: analytics.totalChallenges - analytics.completedChallenges }
  ];

  const categoryData: ChartDataPoint[] = analytics.categoryBreakdown.map(cat => ({
    name: cat.category,
    value: cat.accuracy,
    completed: cat.completed,
    total: cat.total
  }));

  const activityData: ChartDataPoint[] = analytics.recentActivity.map(activity => ({
    name: new Date(activity.date).toLocaleDateString(),
    value: activity.score,
    challenges: activity.challengesCompleted
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border-4 border-black shadow-brutal p-3">
          <p className="font-bold text-black">{label}</p>
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
      transition={{ delay: 0.1 }}
      className="bg-white border-4 border-black shadow-brutal p-6"
    >
      <h3 className="text-2xl font-black text-black mb-6 text-shadow-brutal">
        {t('progressOverview')}
      </h3>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Completion Pie Chart */}
        <div className="space-y-4">
          <h4 className="text-lg font-bold text-black">{t('overallProgress')}</h4>
          <div className="h-64 relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={completionData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  stroke="#000"
                  strokeWidth={3}
                >
                  {completionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="text-center bg-white border-2 border-black rounded-full w-20 h-20 flex items-center justify-center">
                <div>
                  <div className="text-lg font-black text-black">
                    {analytics.completionRate.toFixed(0)}%
                  </div>
                  <div className="text-xs font-bold text-gray-600">
                    {t('done')}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Category Performance Bar Chart */}
        <div className="space-y-4">
          <h4 className="text-lg font-bold text-black">{t('categoryPerformance')}</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
                <Bar 
                  dataKey="value" 
                  fill="#10b981" 
                  stroke="#000" 
                  strokeWidth={2}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Activity Line Chart */}
      {activityData.length > 0 && (
        <div className="mt-8 space-y-4">
          <h4 className="text-lg font-bold text-black">{t('recentActivity')}</h4>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={activityData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#3b82f6" 
                  strokeWidth={4}
                  dot={{ fill: '#3b82f6', strokeWidth: 3, stroke: '#000', r: 6 }}
                  activeDot={{ r: 8, stroke: '#000', strokeWidth: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8 pt-6 border-t-4 border-black">
        <motion.div 
          className="bg-green-100 border-4 border-black shadow-brutal p-4 text-center"
          whileHover={{ scale: 1.02 }}
        >
          <div className="text-2xl font-black text-green-800">
            {analytics.peerComparison.percentile}%
          </div>
          <div className="text-sm font-bold text-green-700 uppercase">
            {t('percentile')}
          </div>
        </motion.div>

        <motion.div 
          className="bg-blue-100 border-4 border-black shadow-brutal p-4 text-center"
          whileHover={{ scale: 1.02 }}
        >
          <div className="text-2xl font-black text-blue-800">
            #{analytics.peerComparison.rank}
          </div>
          <div className="text-sm font-bold text-blue-700 uppercase">
            {t('rank')}
          </div>
        </motion.div>

        <motion.div 
          className="bg-purple-100 border-4 border-black shadow-brutal p-4 text-center"
          whileHover={{ scale: 1.02 }}
        >
          <div className="text-2xl font-black text-purple-800">
            {analytics.streakData.longestStreak}
          </div>
          <div className="text-sm font-bold text-purple-700 uppercase">
            {t('bestStreak')}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
