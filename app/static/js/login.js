function getIPAddress() {
    fetch("https://api.ipify.org?format=json")
    .then(response => response.json())
    .then(data => {
        console.log("IP Address", data.ip)
    })
    .catch(error => {
        console.error("Error: ", error);
    });
}

function getTimeNow() {
    const timeNow = new Date().toLocaleString();
    console.log("Time Now", timeNow);
}

function getUserAgent() {
    const userAgent = navigator.userAgent
    console.log("User Agent:", userAgent);
}

function signInHandler() {
    getIPAddress()
    getTimeNow()
    getUserAgent()

}