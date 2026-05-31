'use client'

import { useState } from 'react'
import { LogEntry } from '@/types/log'
import { RefreshCw, Filter, ChevronDown, ChevronUp } from 'lucide-react'

interface LogViewerProps {
  logs: LogEntry[]
  loading: boolean
  error: string | null
  onRefresh: () => void
}

export function LogViewer({ logs, loading, error, onRefresh }: LogViewerProps) {
  const [filter, setFilter] = useState('all')
  const [expandedLog, setExpandedLog] = useState<number | null>(null)

  const filteredLogs = logs.filter(log => 
    filter === 'all' || log.level === filter
  )

  const getLevelClass = (level: string) => {
    switch (level) {
      case 'info': return 'log-level-info'
      case 'warn': return 'log-level-warn'
      case 'error': return 'log-level-error'
      case 'debug': return 'log-level-debug'
      default: return 'log-level-info'
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('ko-KR')
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">로그 뷰어</h2>
          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            <span>새로고침</span>
          </button>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-600">필터:</span>
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">모든 레벨</option>
            <option value="info">Info</option>
            <option value="warn">Warning</option>
            <option value="error">Error</option>
            <option value="debug">Debug</option>
          </select>
        </div>
      </div>

      <div className="p-6">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="h-6 w-6 animate-spin text-blue-600" />
            <span className="ml-2 text-gray-600">로딩 중...</span>
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            표시할 로그가 없습니다.
          </div>
        ) : (
          <div className="space-y-3">
            {filteredLogs.map((log, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className={getLevelClass(log.level)}>
                        {log.level.toUpperCase()}
                      </span>
                      <span className="text-sm text-gray-500">
                        {formatTimestamp(log.timestamp)}
                      </span>
                      <span className="text-sm text-gray-400">
                        {log.service}
                      </span>
                    </div>
                    <p className="text-gray-900 mb-2">{log.message}</p>
                    
                    {Object.keys(log.fields).length > 0 && (
                      <button
                        onClick={() => setExpandedLog(expandedLog === index ? null : index)}
                        className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700"
                      >
                        <span>필드 보기</span>
                        {expandedLog === index ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </button>
                    )}
                  </div>
                </div>

                {expandedLog === index && Object.keys(log.fields).length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">추가 필드:</h4>
                    <div className="bg-gray-50 rounded p-3">
                      <pre className="text-xs text-gray-600 whitespace-pre-wrap">
                        {JSON.stringify(log.fields, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
