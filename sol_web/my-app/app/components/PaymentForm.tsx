"use client";

import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";
import { Transaction, SystemProgram, PublicKey, LAMPORTS_PER_SOL } from "@solana/web3.js";
import { useState } from "react";

const PaymentForm = () => {
  const { connection } = useConnection();
  const { publicKey, sendTransaction } = useWallet();
  const [message, setMessage] = useState("");

  // Replace this with your wallet address where you want to receive payments
  const PAYMENT_WALLET = new PublicKey("9QowtwuhQ9rWaF2jcbeid3GcDTDYEtDDFxCgkUfTYjM6");
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!publicKey) {
      alert("Please connect your wallet first!");
      return;
    }

    try {
      // Create a transaction to send 1 SOL
      const transaction = new Transaction().add(
        SystemProgram.transfer({
          fromPubkey: publicKey,
          toPubkey: PAYMENT_WALLET,
          lamports: LAMPORTS_PER_SOL, // 1 SOL = 1000000000 Lamports
        })
      );

      const signature = await sendTransaction(transaction, connection);
      console.log("Transaction sent:", signature);
      
      // Wait for transaction confirmation
      const confirmation = await connection.confirmTransaction(signature, "confirmed");
      
      if (confirmation.value.err) {
        throw new Error("Transaction failed!");
      }

      // If payment successful, log the message (will be replaced with backend call later)
      console.log("Payment successful! Message:", message);
      setMessage(""); // Clear the input
      alert("Payment and message submitted successfully!");
      
    } catch (error) {
      console.error("Error:", error);
      alert("Transaction failed! Please try again.");
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <div className="mb-4 flex justify-end">
        <WalletMultiButton />
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="message" className="block text-sm font-medium mb-2">
            Your Message (1 SOL required)
          </label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full p-2 border rounded-md"
            rows={4}
            placeholder="Enter your message here..."
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={!publicKey || !message}
          className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          Submit Message & Pay 1 SOL
        </button>
      </form>
    </div>
  );
};

export default PaymentForm; 