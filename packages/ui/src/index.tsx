import React from 'react'

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>

export function Button(props: ButtonProps) {
  return (
    <button
      {...props}
      style={{
        padding: '8px 12px',
        borderRadius: 8,
        background: '#1d4ed8',
        color: 'white',
        border: 'none',
      }}
    />
  )
}


