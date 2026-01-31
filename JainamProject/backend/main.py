from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import hashlib
from web3 import Web3
import json

app = FastAPI()

# --- CONFIGURATION ---
# Connect to Ganache (Update port if needed, e.g. 7545 or 8545)
BLOCKCHAIN_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))

# --- IMPORTANT: UPDATE THESE WITH YOUR DETAILS ---
SENDER_ADDRESS = "0xYourWalletAddressHere" 
PRIVATE_KEY = "YourPrivateKeyHere" 
CONTRACT_ADDRESS = "0xYourDeployedContractAddressHere"

# Standard ABI (Matches the contract provided earlier)
CONTRACT_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"dataHash","type":"bytes32"},{"indexed":false,"internalType":"bool","name":"isFraud","type":"bool"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"NewRecordAdded","type":"event"},{"inputs":[{"internalType":"bytes32","name":"_dataHash","type":"bytes32"},{"internalType":"bool","name":"_isFraud","type":"bool"},{"internalType":"string","name":"_modelVersion","type":"string"}],"name":"addRecord","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"getRecord","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]'

# Load Contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=json.loads(CONTRACT_ABI))

# Load ML Models (Fail fast if files are missing)
try:
    model = joblib.load('fraud_model.pkl')
    scaler = joblib.load('scaler.pkl')
    imputer = joblib.load('imputer.pkl')
    print("Models loaded successfully.")
except FileNotFoundError:
    print("CRITICAL ERROR: Model files not found. Run '
