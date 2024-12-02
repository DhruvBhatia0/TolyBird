"use client";

import dynamic from 'next/dynamic';

// Dynamically import PaymentForm with ssr disabled
const PaymentForm = dynamic(
  () => import('./components/PaymentForm'),
  { ssr: false }
);

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-2xl font-bold text-center mb-8">
        Submit a Message with Solana Payment
      </h1>
      <PaymentForm />
    </main>
  );
}
