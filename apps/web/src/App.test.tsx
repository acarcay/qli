import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'

function App() {
  return <h1>Hello Qlick</h1>
}

describe('App', () => {
  it('renders hello', () => {
    render(<App />)
    expect(screen.getByText('Hello Qlick')).toBeInTheDocument()
  })
})


