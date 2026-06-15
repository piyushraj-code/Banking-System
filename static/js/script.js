async function login(){
    const account_number = document.getElementById("account_number").value;
    const password = document.getElementById("password").value;
    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            account_number: account_number,
            password: password
        })
    });
    const result = await response.json();
    if (result.success){
        window.location.href = "/dashboard";
    }
    else{
        document.getElementById("modalMessage").textContent = result.message;
        document.getElementById("successModal").style.display = "block";
    }
}

async function register(){
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const balance = document.getElementById("balance").value;
    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            balance: balance,
            password: password
        })
    });
    const result = await response.json()
    if (result.success){
        document.getElementById("modalMessage").textContent = result.message;
        document.getElementById("successModal").style.display = "block";
    }
}

async function deposite() {
    amount = document.getElementById("dipo-amount").value;
    const response = await fetch("/deposite", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            amount: amount
        })
    });
    const result = await response.json()
    document.getElementById("modalMessage").textContent = result.message;
    document.getElementById("successModal").style.display = "block";
}

async function withdraw() {
    amount = document.getElementById("with-amount").value;
    const response = await fetch("/withdraw", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            amount: amount
        })
    });
    const result = await response.json()
    document.getElementById("modalMessage").textContent = result.message;
    document.getElementById("successModal").style.display = "block";
}

async function transfer() {
    const recipient = document.getElementById("recipient").value;
    const amount = document.getElementById("amount").value;
    const response = await fetch("/transfer", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            recipient: recipient,
            amount: amount
        })
    });
    const result = await response.json()
    document.getElementById("modalMessage").textContent = result.message;
    document.getElementById("successModal").style.display = "block";
}

async function view_balance(){
    const response = await fetch("/view_balance", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({

        })
    });
    const result = await response.json()

    document.getElementById("modalMessage").textContent = result.message;
    document.getElementById("successModal").style.display = "block";
}

async function logout(){
    const response = await fetch("/logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({

        })
    });
    const result = await response.json()
    
    document.getElementById("modalMessage").textContent = result.message;
    document.getElementById("successModal").style.display = "block";
}

async function transaction_history(){
    const response = await fetch("transaction_history",{
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({

        })
    });
    const result = await response.json()
}

function dashboard(){
    window.location.href = "/dashboard"
}

function getDeposite(){
    document.getElementById("dipo").style.display = "block";
}

function getWithdraw(){
    document.getElementById("with").style.display = "block";
}

function getTransfer(){
    document.getElementById("tran").style.display = "block";
}

function goToLogin(){
    window.location.href = "/login";
}