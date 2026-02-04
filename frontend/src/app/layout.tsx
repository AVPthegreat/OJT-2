import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: '--font-inter'
});

export const metadata: Metadata = {
  title: "AI Viva Platform | Practice DSA Interviews",
  description: "Practice DSA interviews with an AI-powered voice bot that speaks like your professor. Get real-time feedback and scoring.",
  keywords: ["DSA", "interview", "practice", "AI", "voice", "data structures", "algorithms"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
