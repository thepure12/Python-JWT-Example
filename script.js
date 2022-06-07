const storeToken = false; // Locally store token?
let token = "";
// Load token if storeToken is true
if (storeToken) token = localStorage.token ? localStorage.token : ""

async function doRequest(url, method, body) {
  let data = await fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token,
    },
    body: JSON.stringify(body),
  }).then(resp => resp.json())
  return data;
}

async function getToken() {
  document.querySelector("#res").value = ""
  console.log("Getting token")
  data = await doRequest("/token", "POST", {
    username: document.querySelector("#username").value,
    password: document.querySelector("#password").value,
  })
  token = data.token
  if (storeToken) localStorage.token = token // Locally store token?
  document.querySelector("#res").value = JSON.stringify(data, null, 2);
}

async function getUser() {
  document.querySelector("#res").value = ""
  console.log("Getting user")
  data = await doRequest("/user", "GET")
  document.querySelector("#res").value = JSON.stringify(data, null, 2);
}

async function getProtected() {
  document.querySelector("#res").value = ""
  console.log("Getting protected")
  data = await doRequest("/protected", "GET")
  document.querySelector("#res").value = JSON.stringify(data, null, 2);
}

async function getAdminOnly() {
  document.querySelector("#res").value = ""
  console.log("Getting admin only")
  data = await doRequest("/adminonly", "GET")
  document.querySelector("#res").value = JSON.stringify(data, null, 2);
}

async function invalidateTokens() {
  document.querySelector("#res").value = ""
  console.log("Invalidating all tokens")
  data = await doRequest("/invalidateall", "GET")
  document.querySelector("#res").value = JSON.stringify(data, null, 2);
}

// Add more gets here


/** Get template **
async function get<Something>() {
  document.querySelector("#res").value = ""
  console.log("<Logging text>")
  data = await doRequest("/route", "GET")
  document.querySelector("#res").value = JSON.stringify(data, null, 2);
}
*/