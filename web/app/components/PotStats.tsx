"use client";

import { useEffect, useState } from 'react';
import { getTotalBidsLastHour } from '../services/api';

export default function PotStats() {
  const [totalBids, setTotalBids] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTotalBids = async () => {
      try {
        setIsLoading(true);
        const total = await getTotalBidsLastHour();
        setTotalBids(total || 0);
      } catch (error) {
        console.error('Error fetching total bids:', error);
        setTotalBids(0);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTotalBids();
    // Refresh every minute
    const interval = setInterval(fetchTotalBids, 60000);
    
    return () => clearInterval(interval);
  }, []);

  const potentialPayout = totalBids * 0.7; // 70% of total bids

  if (isLoading) {
    return (
      <div className="bg-white/10 p-4 rounded-lg backdrop-blur-sm">
        <div className="space-y-2">
          <div className="text-center">
            <p className="text-gray-300 text-sm">Loading pot stats...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/10 p-4 rounded-lg backdrop-blur-sm">
      <div className="space-y-2">
        <div className="text-center">
          <p className="text-gray-300 text-sm">Current Pot</p>
          <p className="text-2xl font-bold text-white">
            ${totalBids.toFixed(2)}
          </p>
        </div>
        
        <div className="text-center">
          <p className="text-gray-300 text-sm">Potential Payout</p>
          <p className="text-2xl font-bold text-green-400">
            ${potentialPayout.toFixed(2)}
          </p>
        </div>
      </div>
    </div>
  );
} 