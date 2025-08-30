from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

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

    return {
        "message": f"A total of {request.amount}$ has been transferred from {user_account.name} to {second_user_account.name}",
        "from_user_balance": user_account.total,
        "to_user_balance": second_user_account.total,
    }

@app.post('/users/deposit')
def deposit_money(request:depositAndWithdrawal):
    user_account = next((u for u in users if u.name.lower() == request.user_name.lower()),None)
    if not user_account:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    user_account.total += request.amount

    return {
        "message":f"A total of {request.amount} has been deposited to {user_account.name.upper()}",
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

    return {
        "message":f"Atotal of {request.amount} has been withdrawn from {user_account.name.upper()}",
        "user_balance":user_account.total,
    }

