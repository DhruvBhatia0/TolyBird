"use client";

import { useState, useCallback } from 'react';
import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { LAMPORTS_PER_SOL, SystemProgram, Transaction, PublicKey } from '@solana/web3.js';
import { calculatePotentialPayout } from '../services/api';
import { useRouter } from 'next/navigation';

// Treasury wallet that receives the bids
const BUFFER_PUBKEY = new PublicKey(process.env.NEXT_PUBLIC_BUFFER_PUBKEY || '');

export default function PaymentForm() {
  const { connection } = useConnection();
  const { publicKey, sendTransaction } = useWallet();
  const [message, setMessage] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [potentialPayout, setPotentialPayout] = useState<number | null>(null);
  const router = useRouter();

  const updatePotentialPayout = useCallback(async (amount: string) => {
    if (!amount || isNaN(parseFloat(amount))) {
      setPotentialPayout(null);
      return;
    }
    
    try {
      const result = await calculatePotentialPayout(parseFloat(amount));
      setPotentialPayout(result.potential_payout);
    } catch (error) {
      console.error('Error calculating potential payout:', error);
      setPotentialPayout(null);
    }
  }, []);

  const handleBidAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setAmount(value);
    updatePotentialPayout(value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!publicKey) {
      setError('Please connect your wallet first');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccessMessage(null);

      // Create the transaction
      const transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey: publicKey,
          toPubkey: BUFFER_PUBKEY,
          lamports: parseFloat(amount) * LAMPORTS_PER_SOL,
        })
      );

      // Send the transaction
      const signature = await sendTransaction(transaction, connection);
      
      // Wait for confirmation
      await connection.confirmTransaction(signature, 'processed');

      // Submit to backend
      const response = await fetch('/api/submissions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tweet_text: message,
          bid_amount: parseFloat(amount),
          wallet_address: publicKey.toString(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit message to backend');
      }

      const data = await response.json();
      console.log('Submission successful:', data);
      
      // Show success message
      setSuccessMessage(
        `Success! Transaction signature: ${signature.slice(0, 8)}...${signature.slice(-8)}`
      );
      
      // Clear form
      setMessage('');
      setAmount('');

    } catch (err: unknown) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-center">
        <WalletMultiButton className="btn" />
      </div>

      <div className="text-sm text-center opacity-70">
        <p>Your bid will be sent to:</p>
        <code className="text-xs break-all block mt-1">
          {BUFFER_PUBKEY.toString()}
        </code>
      </div>

      {publicKey && (
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
              onChange={handleBidAmountChange}
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

          {successMessage && (
            <div className="p-3 bg-green-100/10 border border-green-500/20 rounded text-green-500 text-sm whitespace-pre-line">
              {successMessage}
            </div>
          )}

          <button
            type="submit"
            className="btn w-full"
            disabled={loading}
          >
            {loading ? 'Processing...' : (
              potentialPayout ? 
              `Submit - Potential Payout: ${potentialPayout.toFixed(2)} SOL` : 
              "Submit"
            )}
          </button>

          <p className="text-xs opacity-70 text-center break-all">
            Connected: {publicKey.toString()}
          </p>
        </form>
      )}
    </div>
  );
} 