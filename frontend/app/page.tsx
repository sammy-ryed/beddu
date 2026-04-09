'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

interface ChatSession {
  id: string
  title: string
  created_at: string
  last_message_at: string
  message_count: number
  preview: string
}

// Component to render message content with collapsible coping tips
function MessageContent({ content }: { content: string }) {
  const [expandedTips, setExpandedTips] = useState<Set<number>>(new Set())

  const toggleTip = (index: number) => {
    setExpandedTips(prev => {
      const next = new Set(prev)
      if (next.has(index)) {
        next.delete(index)
      } else {
        next.add(index)
      }
      return next
    })
  }

  // Parse the content for coping tips
  const parseContent = (text: string) => {
    const parts: JSX.Element[] = []
    let currentIndex = 0
    const tipRegex = /\[COPING_TIP_START:(\d+)\](.*?)\[COPING_TIP_CONTENT:\d+\](.*?)\[COPING_TIP_END:\d+\]/gs

    let match
    let lastIndex = 0

    while ((match = tipRegex.exec(text)) !== null) {
      const tipIndex = parseInt(match[1])
      const tipHeader = match[2].trim()
      const tipContent = match[3].trim()

      // Add text before this tip
      if (match.index > lastIndex) {
        const beforeText = text.substring(lastIndex, match.index).trim()
        if (beforeText) {
          parts.push(
            <span key={`text-${lastIndex}`} className="whitespace-pre-wrap">
              {beforeText}
            </span>
          )
        }
      }

      // Add the collapsible tip
      const isExpanded = expandedTips.has(tipIndex)
      parts.push(
        <div key={`tip-${tipIndex}`} className="my-3 border border-neutral-300 rounded-lg overflow-hidden bg-neutral-50">
          <button
            onClick={() => toggleTip(tipIndex)}
            className="w-full px-3 py-2 text-left text-sm font-medium text-neutral-700 hover:bg-neutral-100 transition-colors flex items-center justify-between"
          >
            <span>💡 Coping tip (click to {isExpanded ? 'hide' : 'reveal'})</span>
            <span className="text-neutral-500">{isExpanded ? '−' : '+'}</span>
          </button>
          {isExpanded && (
            <div className="px-3 py-2 text-sm text-neutral-800 border-t border-neutral-200 whitespace-pre-wrap">
              {tipContent}
            </div>
          )}
        </div>
      )

      lastIndex = match.index + match[0].length
    }

    // Add remaining text after last tip
    if (lastIndex < text.length) {
      const remainingText = text.substring(lastIndex).trim()
      if (remainingText) {
        parts.push(
          <span key={`text-${lastIndex}`} className="whitespace-pre-wrap">
            {remainingText}
          </span>
        )
      }
    }

    return parts.length > 0 ? parts : <span className="whitespace-pre-wrap">{text}</span>
  }

  return <div>{parseContent(content)}</div>
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [historyLoaded, setHistoryLoaded] = useState(false)
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load sessions on mount
  useEffect(() => {
    loadSessions()
  }, [])

  // Load sessions on mount
  useEffect(() => {
    loadSessions()
  }, [])

  // Don't auto-load history - each chat should start fresh
  // useEffect(() => {
  //   if (currentSessionId && !historyLoaded) {
  //     fetch(`${process.env.NEXT_PUBLIC_API_URL}/history?limit=10`)
  //       .then(res => res.json())
  //       .then(data => {
  //         if (data.success && data.history && data.history.length > 0) {
  //           const previousMessages: Message[] = []
  //           data.history.forEach((conv: any) => {
  //             previousMessages.push({
  //               role: 'user',
  //               content: conv.user_input,
  //               timestamp: conv.timestamp
  //             })
  //             previousMessages.push({
  //               role: 'assistant',
  //               content: conv.bot_response,
  //               timestamp: conv.timestamp
  //             })
  //           })
  //           setMessages(previousMessages)
  //         }
  //         setHistoryLoaded(true)
  //       })
  //       .catch(() => setHistoryLoaded(true))
  //   }
  // }, [currentSessionId, historyLoaded])

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadSessions = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sessions`)
      const data = await res.json()
      if (data.success) {
        setSessions(data.sessions)
        setCurrentSessionId(data.current_session_id)
      }
    } catch (error) {
      console.error('Error loading sessions:', error)
    }
  }

  const createNewChat = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
      const data = await res.json()
      if (data.success) {
        await loadSessions()
        setCurrentSessionId(data.session_id)
        setMessages([])
        setHistoryLoaded(false)
      }
    } catch (error) {
      console.error('Error creating chat:', error)
    }
  }

  const switchChat = async (sessionId: string) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sessions/${sessionId}/switch`, {
        method: 'POST'
      })
      const data = await res.json()
      if (data.success) {
        setCurrentSessionId(sessionId)
        setMessages([])
        setHistoryLoaded(false)
      }
    } catch (error) {
      console.error('Error switching chat:', error)
    }
  }

  const deleteChat = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm('Delete this chat?')) return
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sessions/${sessionId}`, {
        method: 'DELETE'
      })
      const data = await res.json()
      if (data.success) {
        await loadSessions()
        if (data.current_session_id !== currentSessionId) {
          setCurrentSessionId(data.current_session_id)
          setHistoryLoaded(false)
        }
      }
    } catch (error) {
      console.error('Error deleting chat:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      })

      const data = await res.json()
      
      if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
        // Reload sessions to update preview
        loadSessions()
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' }])
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Connection error. Is the backend running?' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-[calc(100vh-120px)]">
      {/* Sidebar - ChatGPT style */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-200 bg-neutral-900 text-white flex flex-col overflow-hidden`}>
        {/* New Chat Button */}
        <div className="p-3 border-b border-neutral-700">
          <button
            onClick={createNewChat}
            className="w-full px-4 py-2.5 bg-neutral-800 hover:bg-neutral-700 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
          >
            <span>+</span> New Chat
          </button>
        </div>

        {/* Chat List */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => switchChat(session.id)}
              className={`group relative px-3 py-2.5 rounded-lg cursor-pointer transition-colors ${
                currentSessionId === session.id
                  ? 'bg-neutral-800'
                  : 'hover:bg-neutral-800'
              }`}
            >
              <div className="text-sm font-medium truncate pr-6">{session.title}</div>
              <div className="text-xs text-neutral-400 truncate">{session.preview || 'No messages yet'}</div>
              <button
                onClick={(e) => deleteChat(session.id, e)}
                className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 text-neutral-400 hover:text-red-400 transition-opacity"
              >
                ×
              </button>
            </div>
          ))}
        </div>

        {/* Navigation Links */}
        <div className="p-3 border-t border-neutral-700 space-y-1 text-sm">
          <Link href="/history" className="block px-3 py-2 hover:bg-neutral-800 rounded-lg transition-colors">
            History
          </Link>
          <Link href="/stats" className="block px-3 py-2 hover:bg-neutral-800 rounded-lg transition-colors">
            Progress
          </Link>
        </div>
      </div>

      {/* Sidebar Toggle */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="fixed left-0 top-20 z-50 px-2 py-3 bg-neutral-900 text-white rounded-r-lg hover:bg-neutral-800 transition-colors"
      >
        {sidebarOpen ? '←' : '→'}
      </button>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 py-8">
        {/* Chat container */}
        <div className="bg-white border border-neutral-200 rounded-lg shadow-sm overflow-hidden flex-1 flex flex-col">
          
          {/* Messages area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.length === 0 && !loading && (
              <div className="flex items-center justify-center h-full text-neutral-400 text-center">
                <div>
                  <p className="text-lg mb-2">Start a conversation</p>
                  <p className="text-sm">Type a message below to begin</p>
                </div>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[80%] ${
                  msg.role === 'user'
                    ? 'bg-neutral-900 text-white rounded-2xl rounded-tr-sm'
                    : 'bg-neutral-100 text-neutral-900 rounded-2xl rounded-tl-sm'
                } px-4 py-3 text-[15px] leading-relaxed`}>
                  {msg.role === 'assistant' ? (
                    <MessageContent content={msg.content} />
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-neutral-100 rounded-2xl rounded-tl-sm px-4 py-3">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="border-t border-neutral-200 p-4 bg-white">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your message..."
                disabled={loading}
                className="flex-1 px-4 py-2.5 border border-neutral-300 rounded-lg text-[15px] placeholder:text-neutral-400 disabled:opacity-50 disabled:cursor-not-allowed focus:border-neutral-900 focus:outline-none focus:ring-2 focus:ring-neutral-900 focus:ring-offset-0"
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="px-6 py-2.5 bg-neutral-900 text-white rounded-lg text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-neutral-800 active:scale-95 transition-all"
              >
                Send
              </button>
            </div>
          </div>
        </div>

        {/* Help text - moved inside main area */}
        <div className="text-center text-xs text-neutral-500 mt-4 px-4">
          <p>💡 Tip: You can update my memory by saying "Actually..." or "Update memory:"</p>
        </div>
      </div>
    </div>
  )
}
