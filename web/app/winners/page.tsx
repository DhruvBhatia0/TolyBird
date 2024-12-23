"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';

const SOL_TO_USD = 235.60;  // Current SOL to USD rate

interface Winner {
  tweet_text: string;
  wallet_address: string;
  payout_amount: number;
  created_at: string;
}

interface PayoutStats {
  total_sol: number;
  total_usd: number;
}

export default function WinnersPage() {
  const [winners, setWinners] = useState<Winner[]>([]);
  const [payoutStats, setPayoutStats] = useState<PayoutStats>({ total_sol: 0, total_usd: 0 });
  const [loading, setLoading] = useState(true);

  const fetchWinners = async () => {
    try {
      const response = await fetch('/api/tweets');
      if (!response.ok) throw new Error('Failed to fetch winners');
      const data = await response.json();
      setWinners(data);
      
      // Calculate totals
      const totalSol = data.reduce((sum: number, winner: Winner) => sum + winner.payout_amount, 0);
      setPayoutStats({
        total_sol: totalSol,
        total_usd: totalSol * SOL_TO_USD
      });
    } catch (err: any) {
      console.error('Error fetching winners:', err?.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWinners();

    // Set up interval to check for new hour
    const interval = setInterval(() => {
      const now = new Date();
      if (now.getMinutes() === 0 && now.getSeconds() === 0) {
        fetchWinners();
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const formatWalletAddress = (address: string) => {
    return `${address.slice(0, 4)}...${address.slice(-4)}`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <main className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold">Previous Winners</h1>
            <div className="mt-2 text-sm opacity-70">
              <p>Total Payouts: {payoutStats.total_sol.toFixed(2)} SOL</p>
              <p>(${payoutStats.total_usd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD)</p>
            </div>
          </div>
          <Link href="/" className="btn">
            Back to Home
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-8 opacity-70">Loading...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Winner</th>
                  <th>Tweet</th>
                  <th>Payout</th>
                </tr>
              </thead>
              <tbody>
                {winners.map((winner, index) => (
                  <tr key={index}>
                    <td>{formatDate(winner.created_at)}</td>
                    <td className="font-mono">
                      {formatWalletAddress(winner.wallet_address)}
                    </td>
                    <td>{winner.tweet_text}</td>
                    <td>{winner.payout_amount.toFixed(2)} SOL</td>
                  </tr>
                ))}
                {winners.length === 0 && (
                  <tr>
                    <td colSpan={4} className="text-center py-8 opacity-70">
                      No winners yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
} 