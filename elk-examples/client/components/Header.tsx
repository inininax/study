import { Activity, Database, Search } from 'lucide-react'

export function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Database className="h-8 w-8 text-blue-600" />
              <Search className="h-6 w-6 text-orange-500" />
              <Activity className="h-6 w-6 text-green-500" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">
              ELK Stack
            </h1>
          </div>
          <div className="text-sm text-gray-500">
            Elasticsearch + Logstash + Kibana
          </div>
        </div>
      </div>
    </header>
  )
}
