import PaymentForm from './components/PaymentForm';

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
