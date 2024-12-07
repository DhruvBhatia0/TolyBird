from theblockchainapi import SolanaAPIResource, SolanaCurrencyUnit, SolanaNetwork, SolanaWallet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from .env
MY_API_KEY_ID = os.getenv("BLOCKCHAIN_API_KEY")
MY_API_SECRET_KEY = os.getenv("BLOCKCHAIN_API_SECRET")

BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
    api_key_id=MY_API_KEY_ID,
    api_secret_key=MY_API_SECRET_KEY
)

def check_wallet_balance():
    # Create wallet instance using your existing private key
    wallet = SolanaWallet(
        b58_private_key=os.getenv("TREASURY_PRIVATE_KEY")
    )
    
    # Derive public key from wallet
    public_key = BLOCKCHAIN_API_RESOURCE.derive_public_key(wallet=wallet)
    print(f"Public Key: {public_key}")
    
    # Get wallet balance
    balance_result = BLOCKCHAIN_API_RESOURCE.get_balance(
        public_key,
        unit=SolanaCurrencyUnit.SOL,
        network=SolanaNetwork.DEVNET
    )
    print(f"Balance: {balance_result['balance']} SOL")
    

if __name__ == '__main__':
    check_wallet_balance()
