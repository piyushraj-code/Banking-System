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
    if (result.success){
        const historyContainer = document.getElementById("history-data");
        historyContainer.innerHTML = "";
        if (result.data.length == 0){
            historyContainer.innerHTML = "<P> No Transactions Found </p>"
        }
        let tableHTML = `
            <table border="1" cellpadding="5" cellspacing="0" style="width: 100%; text-align: center;">
                    <tr>
                        <th>ID</th>
                        <th>Date</th>
                        <th>Type</th>
                        <th>From Account</th>
                        <th>To Account</th>
                        <th>Amount</th>
                    </tr>
        `;
        response.data.forEach(transaction => {
            tableHTML += `
                <tr>
                    <td>${transaction.Transaction_id}</td>
                    <td>${transaction.Date}</td>
                    <td>${transaction.Type}</td>
                    <td>${transaction.Sender}</td>
                    <td>${transaction.Receipent}</td>
                    <td>${transaction.Amount}</td>
                </tr>
            `;
        });
        tableHTML += "</table>";
        historyContainer.innerHTML = tableHTML;
        document.getElementById("hist").style.display = "block";
        document.getElementById("dipo").style.display = "none";
        document.getElementById("with").style.display = "none";
        document.getElementById("tran").style.display = "none";
    }
    else{
        document.getElementById("modalMessage").textContent = result.message || "Failed to load history.";
        document.getElementById("successModal").style.display = "block";
    }
    
}

function dashboard(){
    window.location.href = "/dashboard"
}

function getDeposite(){
    document.getElementById("dipo").style.display = "block";
    document.getElementById("with").style.display = "none";
    document.getElementById("tran").style.display = "none";
    document.getElementById("hist").style.display = "none";
}

function getWithdraw(){
    document.getElementById("with").style.display = "block";
    document.getElementById("dipo").style.display = "none";
    document.getElementById("tran").style.display = "none";
    document.getElementById("hist").style.display = "none";
}

function getTransfer(){
    document.getElementById("tran").style.display = "block";
    document.getElementById("with").style.display = "none";
    document.getElementById("dipo").style.display = "none";
    document.getElementById("hist").style.display = "none";
}

function goToLogin(){
    window.location.href = "/login";
}