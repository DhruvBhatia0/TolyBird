"use client";

import dynamic from 'next/dynamic';
import CountdownTimer from './components/CountdownTimer';
import Link from 'next/link';

const PaymentForm = dynamic(
  () => import('./components/PaymentForm'),
  { ssr: false }
);

const ASCII_LOGO = `
  _________  ________  ___       ___           ___    ___      ________  ___  ________  ________     
 |\\___   ___\\\\   __  \\|\\  \\     |\\  \\         |\\  \\  /  /|    |\\   __  \\|\\  \\|\\   __  \\|\\   ___ \\    
 \\|___ \\  \\_\\ \\  \\|\\  \\ \\  \\    \\ \\  \\        \\ \\  \\/  / /    \\ \\  \\|\\ /\\ \\  \\ \\  \\|\\  \\ \\  \\_|\\ \\   
      \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\    \\ \\  \\        \\ \\    / /      \\ \\   __  \\ \\  \\ \\   _  _\\ \\  \\ \\\\ \\  
       \\ \\  \\ \\ \\  \\\\\\  \\ \\  \\____\\ \\  \\____    \\/  /  /        \\ \\  \\|\\  \\ \\  \\ \\  \\\\  \\\\ \\  \\_\\\\ \\ 
        \\ \\__\\ \\ \\_______\\ \\_______\\ \\_______\\__/  / /           \\ \\_______\\ \\__\\ \\__\\\\ _\\\\ \\_______\\
         \\|__|  \\|_______|\\|_______|\\|_______|\\___/ /             \\|_______|\\|__|\\|__|\\|__|\\|_______|
                                             \\|___|/                                                 
`;

export default function Home() {
  return (
    <main className="min-h-screen py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <pre className="ascii-logo text-center">
          {ASCII_LOGO}
        </pre>
        
        <div className="card mb-8">
          <CountdownTimer />
          
          <h1 className="text-2xl font-bold mb-4 text-center">
            Submit a Message with Solana Payment
          </h1>

          <PaymentForm />
        </div>

        <footer className="text-center text-sm opacity-70">
          <div className="mb-2">
            <Link href="/winners" className="btn">
              View Previous Winners
            </Link>
          </div>
          <p>Built with ♠️ for Solana</p>
        </footer>
      </div>
    </main>
  );
}
