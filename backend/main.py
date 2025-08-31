from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional, List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_methods=["*"],
    allow_headers=["*"],
)

transactions : List[Dict] = []


class BankAcc:
    def __init__(self,name:str,id:int,total:int):
        self.name = name
        self.id = id
        self.total = total
     
user1=BankAcc('zoy',1,2000)
user2=BankAcc('rafal',2,4000)
user3=BankAcc('tabarak',3,5500)

users = [user1,user2,user3]

class TransferRequest(BaseModel):
    from_user: str
    to_user:str
    amount:int

class depositAndWithdrawal(BaseModel):
    user_name:str
    amount:int


@app.get('/users/{username}')
def get_user(username: str):
    user_account = next((u for u in users if u.name.lower() == username.lower()), None)
    if not user_account:
        raise HTTPException(status_code=404, detail="User not found")
    return {"name": user_account.name, "total": user_account.total}


@app.get('/users')
def show_users():
        return [
            {"name":i.name, "total":i.total}
            for i in users
        ]

@app.post('/users/transfer')
def transfer_money(request:TransferRequest):
    user_account = next((u for u in users if u.name.lower() == request.from_user.lower()),None)
    if not user_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    second_user_account = next((u for u in users if u.name.lower() == request.to_user.lower() and u.name.lower() != request.from_user.lower()),None)
    if not second_user_account:
        raise HTTPException(status_code=404, detail="Destination account not found")
    
    if request.amount > user_account.total:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    user_account.total -= request.amount
    second_user_account.total += request.amount


    transactions.append({
        "type": "transfer",
        "amount": request.amount,
        "at": datetime.now().isoformat(timespec="seconds"),
        "from_user": user_account.name,
        "to_user": second_user_account.name,
        "balance_after": user_account.total,
        "owner": user_account.name
    })

    return {
        "message": f"A total of {request.amount}$ has been transferred from {user_account.name.upper()} to {second_user_account.name.upper()}",
        "from_user_balance": user_account.total,
        "to_user_balance": second_user_account.total,
    }

@app.post('/users/deposit')
def deposit_money(request:depositAndWithdrawal):
    user_account = next((u for u in users if u.name.lower() == request.user_name.lower()),None)
    if not user_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    user_account.total += request.amount

    transactions.append({
        "type": "deposit",
        "amount": request.amount,
        "at": datetime.now().isoformat(timespec="seconds"),
        "from_user": None,
        "to_user": user_account.name,
        "balance_after": user_account.total,
        "owner": user_account.name
    })


    return {
        "message":f"A total of $ {request.amount} has been deposited to {user_account.name.upper()}",
        "user_balance":user_account.total,
    }


@app.post('/users/withdrawal')
def withdrawal_money(request:depositAndWithdrawal):
    user_account = next ((u for u in users if u.name.lower() == request.user_name.lower()),None)
    if not user_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    if request.amount > user_account.total:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    user_account.total -= request.amount

    transactions.append({
        "type": "withdrawal",
        "amount": request.amount,
        "at": datetime.now().isoformat(timespec="seconds"),
        "from_user":user_account.name,
        "to_user": None,
        "balance_after": user_account.total,
        "owner": user_account.name
    })

    return {
        "message":f"Atotal of $ {request.amount} has been withdrawn from {user_account.name.upper()}",
        "user_balance":user_account.total,
    }

