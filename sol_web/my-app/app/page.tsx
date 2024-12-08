"use client";

import dynamic from 'next/dynamic';

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
          <h1 className="text-2xl font-bold mb-4 text-center">
            Submit a Message with Solana Payment
          </h1>
          
          <div className="data-table mb-6">
            <table>
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Network</td>
                  <td>Solana Devnet</td>
                </tr>
                <tr>
                  <td>Min Bid</td>
                  <td>0.1 SOL</td>
                </tr>
                <tr>
                  <td>Max Length</td>
                  <td>280 characters</td>
                </tr>
              </tbody>
            </table>
          </div>

          <PaymentForm />
        </div>

        <footer className="text-center text-sm opacity-70">
          <p>Built with ♠️ for Solana</p>
        </footer>
      </div>
    </main>
  );
}
