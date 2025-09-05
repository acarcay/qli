export type UUID = string

export interface HealthResponse {
  status: 'ok'
}

export function invariant(condition: unknown, message: string): asserts condition {
  if (!condition) {
    throw new Error(message)
  }
}


