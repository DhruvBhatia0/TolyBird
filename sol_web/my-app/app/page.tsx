"use client";

import dynamic from 'next/dynamic';

// Dynamically import PaymentForm with ssr disabled
const PaymentForm = dynamic(
  () => import('./components/PaymentForm'),
  { ssr: false }
);

export default function Home() {
  return (
    <main className="min-h-screen py-12 px-4 bg-gradient-to-b from-gray-900 to-gray-800">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8 text-white">
          Submit a Message with Solana Payment
        </h1>
        <PaymentForm />
      </div>
    </main>
  );
}
