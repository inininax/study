'use client'

import { useState } from 'react'
import { Play, Send, Plus, X } from 'lucide-react'

interface LogGeneratorProps {
  onGenerate: () => void
  onSendCustom: (message: string, level: string, fields: Record<string, any>) => void
  loading: boolean
}

export function LogGenerator({ onGenerate, onSendCustom, loading }: LogGeneratorProps) {
  const [showCustomForm, setShowCustomForm] = useState(false)
  const [customMessage, setCustomMessage] = useState('')
  const [customLevel, setCustomLevel] = useState('info')
  const [customFields, setCustomFields] = useState<Array<{ key: string; value: string }>>([])

  const handleGenerate = () => {
    onGenerate()
  }

  const handleSendCustom = () => {
    const fields: Record<string, any> = {}
    customFields.forEach(field => {
      if (field.key && field.value) {
        // 숫자로 변환 시도
        const numValue = Number(field.value)
        fields[field.key] = isNaN(numValue) ? field.value : numValue
      }
    })

    onSendCustom(customMessage, customLevel, fields)
    setCustomMessage('')
    setCustomFields([])
    setShowCustomForm(false)
  }

  const addField = () => {
    setCustomFields([...customFields, { key: '', value: '' }])
  }

  const removeField = (index: number) => {
    setCustomFields(customFields.filter((_, i) => i !== index))
  }

  const updateField = (index: number, key: string, value: string) => {
    const newFields = [...customFields]
    newFields[index] = { key, value }
    setCustomFields(newFields)
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">로그 생성기</h2>
      
      <div className="space-y-4">
        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
        >
          <Play className="h-4 w-4" />
          <span>샘플 로그 10개 생성</span>
        </button>

        <div className="border-t pt-4">
          <button
            onClick={() => setShowCustomForm(!showCustomForm)}
            className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="h-4 w-4" />
            <span>커스텀 로그 생성</span>
          </button>
        </div>

        {showCustomForm && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                메시지
              </label>
              <input
                type="text"
                value={customMessage}
                onChange={(e) => setCustomMessage(e.target.value)}
                placeholder="로그 메시지를 입력하세요"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                레벨
              </label>
              <select
                value={customLevel}
                onChange={(e) => setCustomLevel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="info">Info</option>
                <option value="warn">Warning</option>
                <option value="error">Error</option>
                <option value="debug">Debug</option>
              </select>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  추가 필드
                </label>
                <button
                  onClick={addField}
                  className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700"
                >
                  <Plus className="h-4 w-4" />
                  <span>필드 추가</span>
                </button>
              </div>
              
              {customFields.map((field, index) => (
                <div key={index} className="flex items-center space-x-2 mb-2">
                  <input
                    type="text"
                    value={field.key}
                    onChange={(e) => updateField(index, e.target.value, field.value)}
                    placeholder="키"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <span className="text-gray-500">:</span>
                  <input
                    type="text"
                    value={field.value}
                    onChange={(e) => updateField(index, field.key, e.target.value)}
                    placeholder="값"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    onClick={() => removeField(index)}
                    className="p-2 text-red-600 hover:text-red-700"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>

            <button
              onClick={handleSendCustom}
              disabled={!customMessage || loading}
              className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
            >
              <Send className="h-4 w-4" />
              <span>로그 전송</span>
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
