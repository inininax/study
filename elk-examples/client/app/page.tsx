'use client'

import { useState, useEffect } from 'react'
import { LogEntry } from '@/types/log'
import { LogViewer } from '@/components/LogViewer'
import { LogGenerator } from '@/components/LogGenerator'
import { Header } from '@/components/Header'

export default function Home() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchLogs = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs`)
      if (!response.ok) {
        throw new Error('Failed to fetch logs')
      }
      const data = await response.json()
      setLogs(data.logs)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const generateLogs = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate-logs`, {
        method: 'GET',
      })
      if (!response.ok) {
        throw new Error('Failed to generate logs')
      }
      // 로그 생성 후 다시 조회
      await fetchLogs()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const sendCustomLog = async (message: string, level: string, fields: Record<string, any>) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/logs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, level, fields }),
      })
      if (!response.ok) {
        throw new Error('Failed to send log')
      }
      // 로그 전송 후 다시 조회
      await fetchLogs()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLogs()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            ELK Stack Example
          </h1>
          <p className="text-gray-600">
            Go Fiber 서버와 Next.js 클라이언트를 통한 로그 수집 및 분석 시스템
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <LogGenerator 
              onGenerate={generateLogs}
              onSendCustom={sendCustomLog}
              loading={loading}
            />
            
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">서버 상태</h2>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Go Server:</span>
                  <span className="text-green-600">Running</span>
                </div>
                <div className="flex justify-between">
                  <span>Elasticsearch:</span>
                  <span className="text-green-600">Connected</span>
                </div>
                <div className="flex justify-between">
                  <span>Logstash:</span>
                  <span className="text-green-600">Processing</span>
                </div>
                <div className="flex justify-between">
                  <span>Kibana:</span>
                  <span className="text-green-600">Available</span>
                </div>
              </div>
            </div>
          </div>

          <div>
            <LogViewer 
              logs={logs}
              loading={loading}
              error={error}
              onRefresh={fetchLogs}
            />
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Kibana 대시보드 접속
          </h3>
          <p className="text-blue-700 mb-4">
            생성된 로그를 시각화하고 분석하려면 Kibana에 접속하세요.
          </p>
          <a 
            href="http://localhost:5601" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Kibana 열기
          </a>
        </div>
      </main>
    </div>
  )
}
