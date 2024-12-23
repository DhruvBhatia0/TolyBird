"use client";

import dynamic from 'next/dynamic';
import CountdownTimer from './components/CountdownTimer';
import Link from 'next/link';

const PaymentForm = dynamic(
  () => import('./components/PaymentForm'),
  { ssr: false }
);

const ASCII_LOGO = `
_______  _        _______  _______  _______  _______   _________          _______    _______  _______  ______   _______ 
(  ____ )( \\      (  ____ \\(  ___  )(  ____ \\(  ____ \\  \\__   __/|\\     /|(  ____ \\  (  ____ \\(  ___  )(  __  \\ (  ____ \\
| (    )|| (      | (    \\/| (   ) || (    \\/| (    \\/     ) (   | )   ( || (    \\/  | (    \\/| (   ) || (  \\  )| (    \\/
| (____)|| |      | (__    | (___) || (_____ | (__         | |   | (___) || (__      | |      | |   | || |   ) || (_____ 
|  _____)| |      |  __)   |  ___  |(_____  )|  __)        | |   |  ___  ||  __)     | | ____ | |   | || |   | |(_____  )
| (      | |      | (      | (   ) |      ) || (           | |   | (   ) || (        | | \\_  )| |   | || |   ) |      ) |
| )      | (____/\\| (____/\\| )   ( |/\\____) || (____/\\     | |   | )   ( || (____/\\  | (___) || (___) || (__/  )/\\____) |
|/       (_______/(_______/|/     \\|\\_______)(_______/     )_(   |/     \\|(_______/  (_______)(_______)(______/ \\_______)
`;

export default function Home() {
  return (
    <main className="min-h-screen py-12 px-4">
      <div className="max-w-2xl mx-auto">
      <strong>
        <pre className="ascii-logo text-center">
          {ASCII_LOGO}
        </pre>
      </strong>
        
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
