'use client'

import { useState, useEffect } from 'react'

interface Stats {
  total_sessions: number
  sessions_with_stress: number
  average_stress_level: number
  stress_percentage: number
  recent_avg_stress: number
  previous_avg_stress: number
  improvement_percentage: number
  most_common_category: string
  crisis_count: number
}

export default function StatsPage() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/stats`)
      .then(res => res.json())
      .then(data => {
        setStats(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="text-center text-neutral-500">Loading...</div>
      </div>
    )
  }

  if (!stats || stats.total_sessions === 0) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="text-center text-neutral-500">
          No data yet. Start chatting with beedu to see your progress!
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold mb-6">Your Progress</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
        {/* Total Sessions */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Total Sessions</div>
          <div className="text-3xl font-semibold">{stats.total_sessions}</div>
        </div>

        {/* Stress Detection Rate */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Stress Detected</div>
          <div className="text-3xl font-semibold">{stats.stress_percentage}%</div>
          <div className="text-xs text-neutral-500 mt-1">
            {stats.sessions_with_stress} of {stats.total_sessions} sessions
          </div>
        </div>

        {/* Average Stress */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Avg Stress Level</div>
          <div className="text-3xl font-semibold">{stats.average_stress_level}/10</div>
        </div>

        {/* Recent vs Previous */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Recent (Last 7)</div>
          <div className="text-3xl font-semibold">{stats.recent_avg_stress}/10</div>
        </div>

        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Previous (7 Before)</div>
          <div className="text-3xl font-semibold">{stats.previous_avg_stress}/10</div>
        </div>

        {/* Improvement */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Change</div>
          <div className={`text-3xl font-semibold ${
            stats.improvement_percentage > 0 ? 'text-green-600' :
            stats.improvement_percentage < 0 ? 'text-red-600' :
            'text-neutral-900'
          }`}>
            {stats.improvement_percentage > 0 && '+'}
            {stats.improvement_percentage}%
          </div>
          {stats.improvement_percentage > 0 && (
            <div className="text-xs text-green-600 mt-1">Getting better 📈</div>
          )}
          {stats.improvement_percentage < 0 && (
            <div className="text-xs text-red-600 mt-1">Recent increase</div>
          )}
        </div>

        {/* Most Common Category */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5 md:col-span-2">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Most Common Concern</div>
          <div className="text-2xl font-semibold capitalize">{stats.most_common_category.replace('_', ' ')}</div>
        </div>

        {/* Crisis Count */}
        <div className="bg-white border border-neutral-200 rounded-lg p-5">
          <div className="text-xs text-neutral-500 uppercase tracking-wide mb-2">Crisis Situations</div>
          <div className="text-3xl font-semibold">{stats.crisis_count}</div>
        </div>

      </div>

      {/* Interpretation */}
      <div className="mt-6 bg-neutral-100 border border-neutral-200 rounded-lg p-5">
        <h2 className="text-sm font-semibold mb-2">What This Means</h2>
        <p className="text-sm text-neutral-600 leading-relaxed">
          {stats.improvement_percentage > 0 ? (
            `Great progress! Your stress levels have decreased by ${stats.improvement_percentage}%. Keep up the good work with self-care and reaching out for support when needed.`
          ) : stats.improvement_percentage < 0 ? (
            `Your stress levels have increased recently. This is completely normal - everyone has ups and downs. Consider reaching out to the resources beedu has shared, or talk to someone you trust.`
          ) : (
            `Your stress levels have been consistent. Keep engaging with beedu to track your mental health journey over time.`
          )}
        </p>
      </div>
    </div>
  )
}
