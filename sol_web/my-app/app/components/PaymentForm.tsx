"use client";

import { useState } from 'react';
import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { LAMPORTS_PER_SOL } from '@solana/web3.js';

export default function PaymentForm() {
  const { connection } = useConnection();
  const { connected, publicKey } = useWallet();
  const [message, setMessage] = useState('');
  const [amount, setAmount] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Your existing submit logic here
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-center">
        <WalletMultiButton className="btn" />
      </div>

      {connected && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-2 text-sm font-bold">
              Your Message
            </label>
            <textarea
              value={message}
              onChange={(e) => {
                if (e.target.value.length <= 280) {
                  setMessage(e.target.value);
                }
              }}
              className="input w-full h-32 resize-none"
              placeholder="Enter your message (max 280 chars)"
              maxLength={280}
              required
            />
            <div className="text-xs text-right opacity-70">
              {message.length}/280 characters
            </div>
          </div>

          <div>
            <label className="block mb-2 text-sm font-bold">
              Bid Amount (SOL)
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="input w-full"
              placeholder="Min 0.1 SOL"
              step="0.1"
              min="0.1"
              required
            />
          </div>

          {error && (
            <div className="p-3 bg-red-100/10 border border-red-500/20 rounded text-red-500 text-sm">
              {error}
            </div>
          )}

          {status === 'success' && (
            <div className="p-3 bg-green-100/10 border border-green-500/20 rounded text-green-500 text-sm">
              Message submitted successfully!
            </div>
          )}

          <button
            type="submit"
            className="btn w-full"
            disabled={status === 'loading'}
          >
            {status === 'loading' ? 'Submitting...' : 'Submit Message'}
          </button>

          {publicKey && (
            <p className="text-xs opacity-70 text-center break-all">
              Connected: {publicKey.toString()}
            </p>
          )}
        </form>
      )}
    </div>
  );
} 