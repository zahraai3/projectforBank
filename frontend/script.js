const API_URL = "http://127.0.0.1:8000"; 

function loadUser() {
    const userName = document.getElementById('username').value.trim();

    if (!userName) {
        alert("Please enter a username");
        return;
    }

    console.log("Fetching user:", userName);

    fetch(`${API_URL}/users/${userName}`)
        .then(res => {
            if (!res.ok) {
                throw new Error("User not found");
            }
            return res.json();
        })
        .then(data => {
            const userDiv = document.getElementById("user");
            userDiv.innerHTML = `Name: ${data.name} | Balance: ${data.total}$`;
        })
        .catch(err => {
            alert(err.message);
        });
}

function depositMoney(){
     const depositamount = parseInt(document.getElementById("depositamount").value.trim());
     const username = document.getElementById("username").value.trim();

     if(!depositamount || depositamount <=0 ){
        alert("please enter avalid amount ");
        return;
     }

     fetch(`${API_URL}/users/deposit`,{
        method:"POST",
        headers:  { "Content-Type": "application/json" },
        body: JSON.stringify({
        user_name: document.getElementById("username").value.trim(),
        amount: depositamount
    })
     })
      .then(res =>{
        if(!res.ok){
            throw new Error("funds not available")
        }
        return res.json();
      })
      .then(data =>{
        const usernameh1 = document.getElementById("forusername");
        usernameh1.innerHTML = `Name: ${username}`
        const amounth3 = document.getElementById("forurtotal")
        amounth3.innerHTML = `Your balance : ${data.user_balance} $`;
        alert(`${data.message}`)
      })
      .catch(err =>{
        alert(err.message)
      })

}



function withdrawMoney(){
     const withdrawamount = parseInt(document.getElementById("withdrawamount").value.trim());
     const username = document.getElementById("username").value.trim();

     if(!withdrawamount || withdrawamount <=0 ){
        alert("please enter avalid amount ");
        return;
     }

     fetch(`${API_URL}/users/withdrawal`,{
        method:"POST",
        headers:  { "Content-Type": "application/json" },
        body: JSON.stringify({
        user_name: document.getElementById("username").value.trim(),
        amount: withdrawamount
    })
     })
      .then(res =>{
        if(!res.ok){
            throw new Error("funds not available")
        }
        return res.json();
      })
      .then(data =>{
        const usernameh1 = document.getElementById("forusername");
        usernameh1.innerHTML = `Name: ${username}`
        const amounth3 = document.getElementById("forurtotal")
        amounth3.innerHTML = `Your balance : ${data.user_balance} $`;
        alert(`${data.message}`)
      })
      .catch(err =>{
        alert(err.message)
      })

}

function transferMoney(){
    const username = document.getElementById("username").value.trim();
    const usertransferto = document.getElementById("transferTo").value.trim();
    const transferamount = parseInt(document.getElementById("transferAmount").value.trim());

    if(!username || !usertransferto){
        alert("Please Enter a name");
        return;
    }

     if(transferamount <= 0){
        alert("invalid amount !");
        return;
     }

    fetch(`${API_URL}/users/transfer`,{
     method: "POST",
     headers: {"Content-Type": "application/json"},
     body:JSON.stringify({
        from_user: document.getElementById("username").value.trim(),
        to_user: document.getElementById("transferTo").value.trim(),
        amount : transferamount
     })
    }).then(res =>{
        if(!res.ok){
            throw new Error("funds not available")
        }
        return res.json();
    }).then(data =>{
        const forusername = document.getElementById("forusername");
        forusername.innerHTML = `Name: ${username}`;
        const parentdiv = document.getElementById("user");
        const childdiv = document.createElement("h3");
        childdiv.id = "transferedtouser";
        childdiv.innerHTML = `User transferred to : ${usertransferto}`;
        parentdiv.appendChild(childdiv);
        const money = document.getElementById("forurtotal");
        money.innerHTML= `Your balance : ${data.from_user_balance} $`
        alert( data.message);

    }).catch(err => {
        alert(err.message)
    })

}
