export interface LogEntry {
  timestamp: string
  level: string
  message: string
  service: string
  fields: Record<string, any>
}

export interface LogRequest {
  message: string
  level: string
  fields: Record<string, any>
}
