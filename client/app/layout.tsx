import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className='absolute h-screen w-screen flex overflow-hidden top-0 left-0'>{children}</body>
    </html>
  )
}
