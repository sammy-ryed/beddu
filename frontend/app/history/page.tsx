'use client'

import { useState, useEffect } from 'react'

interface Conversation {
  timestamp: string
  user_input: string
  bot_response: string
  stress_detected?: boolean
  stress_level?: number
  stress_category?: string
  is_crisis?: boolean
}

interface MemoryFact {
  fact: string
  category: string
  timestamp: string
}

export default function HistoryPage() {
  const [activeTab, setActiveTab] = useState<'conversations' | 'memory'>('conversations')
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [memoryFacts, setMemoryFacts] = useState<MemoryFact[]>([])
  const [filter, setFilter] = useState<'all' | 'stress' | 'crisis'>('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load conversations
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/history`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setConversations(data.history || [])
        }
        setLoading(false)
      })
      .catch(() => setLoading(false))

    // Load memory
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/permanent-memory`)
      .then(res => res.json())
      .then(data => {
        if (data.success && data.permanent_memory) {
          setMemoryFacts(data.permanent_memory.facts || [])
        }
      })
  }, [])

  const filteredConversations = conversations.filter(conv => {
    if (filter === 'stress') return conv.stress_detected
    if (filter === 'crisis') return conv.is_crisis
    return true
  }).reverse() // Show newest first

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    return date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })
  }

  const getStressBadge = (conv: Conversation) => {
    if (conv.is_crisis) {
      return <span className="text-xs px-2 py-0.5 bg-red-100 text-red-700 rounded">Crisis</span>
    }
    if (conv.stress_detected && conv.stress_level) {
      if (conv.stress_level >= 8) {
        return <span className="text-xs px-2 py-0.5 bg-orange-100 text-orange-700 rounded">High</span>
      }
      if (conv.stress_level >= 5) {
        return <span className="text-xs px-2 py-0.5 bg-yellow-100 text-yellow-700 rounded">Moderate</span>
      }
      return <span className="text-xs px-2 py-0.5 bg-blue-100 text-blue-700 rounded">Mild</span>
    }
    return <span className="text-xs px-2 py-0.5 bg-neutral-100 text-neutral-600 rounded">Casual</span>
  }

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="text-center text-neutral-500">Loading...</div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold mb-6">Your Journey</h1>

      {/* Tab switcher - clean design */}
      <div className="flex gap-1 mb-6 border-b border-neutral-200">
        <button
          onClick={() => setActiveTab('conversations')}
          className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors ${
            activeTab === 'conversations'
              ? 'border-neutral-900 text-neutral-900'
              : 'border-transparent text-neutral-600 hover:text-neutral-900'
          }`}
        >
          Conversations
        </button>
        <button
          onClick={() => setActiveTab('memory')}
          className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors ${
            activeTab === 'memory'
              ? 'border-neutral-900 text-neutral-900'
              : 'border-transparent text-neutral-600 hover:text-neutral-900'
          }`}
        >
          What I Remember
        </button>
      </div>

      {/* Conversations tab */}
      {activeTab === 'conversations' && (
        <div className="space-y-4">
          {/* Filter buttons */}
          <div className="flex gap-2">
            {(['all', 'stress', 'crisis'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${
                  filter === f
                    ? 'bg-neutral-900 text-white border-neutral-900'
                    : 'bg-white text-neutral-600 border-neutral-300 hover:border-neutral-900'
                }`}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>

          {/* Conversation list */}
          {filteredConversations.length === 0 ? (
            <div className="text-center py-12 text-neutral-500 text-sm">
              No conversations {filter !== 'all' && `matching "${filter}" filter`}
            </div>
          ) : (
            <div className="space-y-3">
              {filteredConversations.map((conv, idx) => (
                <div key={idx} className="bg-white border border-neutral-200 rounded-lg p-4 hover:border-neutral-300 transition-colors">
                  <div className="flex items-center justify-between mb-3 text-xs text-neutral-500">
                    <span>{formatDate(conv.timestamp)}</span>
                    {getStressBadge(conv)}
                  </div>
                  <div className="space-y-2">
                    <div className="text-sm">
                      <div className="font-medium text-neutral-900 mb-1">You:</div>
                      <div className="text-neutral-600">{conv.user_input}</div>
                    </div>
                    <div className="text-sm">
                      <div className="font-medium text-neutral-900 mb-1">beedu:</div>
                      <div className="text-neutral-600">{conv.bot_response}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Memory tab */}
      {activeTab === 'memory' && (
        <div className="space-y-4">
          {memoryFacts.length === 0 ? (
            <div className="text-center py-12 text-neutral-500 text-sm">
              No memories yet. Chat with beedu to build your memory!
            </div>
          ) : (
            <div className="bg-white border border-neutral-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold mb-4">Key Facts About You</h2>
              <div className="space-y-3">
                {memoryFacts.map((fact, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-neutral-50 rounded-lg">
                    <div className="flex-1">
                      <div className="text-xs text-neutral-500 uppercase mb-1">{fact.category}</div>
                      <div className="text-sm text-neutral-900">{fact.fact}</div>
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-xs text-neutral-500 mt-4">
                Tip: Say "Actually..." or "Update memory:" to correct any information
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
