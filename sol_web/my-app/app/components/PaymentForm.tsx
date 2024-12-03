"use client";

import { useState } from 'react';
import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { LAMPORTS_PER_SOL, SystemProgram, Transaction } from '@solana/web3.js';
import { createSubmission } from '../services/api';

export default function PaymentForm() {
  const { connection } = useConnection();
  const { publicKey, sendTransaction } = useWallet();
  const [amount, setAmount] = useState('');
  const [tweet, setTweet] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

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
          toPubkey: publicKey,
          lamports: parseFloat(amount) * LAMPORTS_PER_SOL,
        })
      );

      // Send the transaction
      const signature = await sendTransaction(transaction, connection);
      
      // Wait for confirmation
      await connection.confirmTransaction(signature, 'processed');

      // Create submission in the database
      const response = await createSubmission({
        tweet_text: tweet,
        bid_amount: parseFloat(amount),
        wallet_address: publicKey.toString()
      });

      console.log('Payment successful!');
      console.log('Signature:', signature);
      
      // Show success message
      setSuccessMessage(
        `Success! Transaction signature: ${signature.slice(0, 8)}...${signature.slice(-8)}\n${response.message}`
      );
      
      // Clear form
      setAmount('');
      setTweet('');

    } catch (err: unknown) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white/10 rounded-lg shadow-lg">
      <div className="mb-6 flex justify-center">
        <WalletMultiButton />
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Tweet Text</label>
          <textarea
            value={tweet}
            onChange={(e) => setTweet(e.target.value)}
            placeholder="Enter your tweet"
            className="w-full p-3 border rounded-md text-black bg-white/90"
            required
            rows={3}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Amount (SOL)</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount in SOL"
            className="w-full p-3 border rounded-md text-black bg-white/90"
            required
            step="0.000000001"
            min="0"
          />
        </div>
        {error && (
          <div className="text-red-500 text-sm p-2 bg-red-100/10 rounded">{error}</div>
        )}
        {successMessage && (
          <div className="text-green-500 text-sm p-2 bg-green-100/10 rounded whitespace-pre-line">{successMessage}</div>
        )}
        <button
          type="submit"
          disabled={loading || !publicKey}
          className="w-full bg-purple-600 text-white py-3 px-4 rounded-md hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Processing...' : 'Submit Tweet'}
        </button>
      </form>
    </div>
  );
} 