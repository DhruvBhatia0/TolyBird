from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair
import os

client = Client("https://api.devnet.solana.com")

private_key = "Ykc4CPB9GC1TqQf4LgDKtErxDUfuTS6wbbbmAqCk5x3PZ8uFjZz9M9bjzrVrYcQHT8s1LqHfE7rGPjub4U826bN"
sender = Keypair.from_private_key(private_key)
receiver = PublicKey("ECabWNyM52hbxm4xNENNVJ22m97iRjAsUVjMEv3T4HYB")
amount = 100000

instruction = transfer(
        from_public_key=sender.public_key,
        to_public_key=receiver, 
        lamports=amount
    )

transaction = Transaction(instructions=[instruction], signers=[sender])

result = client.send_transaction(transaction)
print("Transaction result: ", result)

