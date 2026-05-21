import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'E-Shifa AI - Healthcare Orchestrator',
  description: "Pakistan's First Fully Automated Healthcare Service Platform",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
