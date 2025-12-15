// ---------- Helpers ----------
const $ = (id) => document.getElementById(id);

function show(el) { el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }

function setMsg(id, text, ok = true) {
  const el = $(id);
  el.textContent = text || "";
  el.classList.toggle("error", !ok);
}

async function api(url, method = "GET", body = null) {
  const opts = { method, headers: {} };
  if (body) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(url, opts);
  const data = await res.json().catch(() => ({}));
  return { res, data };
}

// ---------- UI Sections ----------
const authSection = $("authSection");
const meSection = $("meSection");
const personalSection = $("personalSection");
const profileSection = $("profileSection");
const planSection = $("planSection");

// ---------- Auth Handlers ----------
$("signupBtn").onclick = async () => {
  setMsg("authMsg", "");
  const email = $("email").value.trim();
  const password = $("password").value;

  const { res, data } = await api("/api/signup", "POST", { email, password });
  if (!res.ok) return setMsg("authMsg", data.error || "Signup failed.", false);

  setMsg("authMsg", "Signup successful.");
  await refreshState();
};

$("loginBtn").onclick = async () => {
  setMsg("authMsg", "");
  const email = $("email").value.trim();
  const password = $("password").value;

  const { res, data } = await api("/api/login", "POST", { email, password });
  if (!res.ok) return setMsg("authMsg", data.error || "Login failed.", false);

  setMsg("authMsg", "Login successful.");
  await refreshState();
};

$("logoutBtn").onclick = async () => {
  await api("/api/logout", "POST");
  hide(meSection);
  hide(personalSection);
  hide(profileSection);
  hide(planSection);
  show(authSection);
  setMsg("authMsg", "Logged out.");
};

// ---------- Personal Details ----------
$("savePersonalBtn").onclick = async () => {
  setMsg("personalMsg", "");
  const payload = {
    first_name: $("firstName").value.trim(),
    last_name: $("lastName").value.trim(),
    country: $("country").value.trim(),
    timezone: $("timezone").value.trim(),
  };

  const { res, data } = await api("/api/personal", "POST", payload);
  if (!res.ok) return setMsg("personalMsg", data.error || "Could not save.", false);

  setMsg("personalMsg", "Saved.");
  await refreshState();
};

// ---------- Investment Profile ----------
$("saveProfileBtn").onclick = async () => {
  setMsg("profileMsg", "");
  const payload = {
    monthly_invest_amount: parseFloat($("monthly").value || "0"),
    risk_appetite: $("risk").value,
    time_horizon: $("horizon").value,
    markets: $("markets").value.trim(),
    experience_level: $("experience").value,
  };

  const { res, data } = await api("/api/profile", "POST", payload);
  if (!res.ok) return setMsg("profileMsg", data.error || "Could not save profile.", false);

  setMsg("profileMsg", "Profile saved.");
  await refreshState();
};

// ---------- Daily Plan ----------
$("generatePlanBtn").onclick = async () => {
  $("planOutput").textContent = "Generating...";
  const note = $("note").value.trim();

  const { res, data } = await api("/api/plan/daily", "POST", { note });
  if (!res.ok) {
    $("planOutput").textContent = data.error || "Could not generate plan.";
    return;
  }
  $("planOutput").textContent = data.plan || "";
};

// ---------- State Refresh ----------
async function refreshState() {
  // Check if logged in
  const me = await api("/api/me", "GET");
  const user = me.data.user;

  if (!user) {
    show(authSection);
    hide(meSection);
    hide(personalSection);
    hide(profileSection);
    hide(planSection);
    return;
  }

  // Logged in
  hide(authSection);
  show(meSection);
  show(personalSection);
  show(profileSection);
  show(planSection);

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ").trim();
  $("welcomeTitle").textContent = fullName ? `Welcome, ${fullName}` : "Welcome";
  $("welcomeSub").textContent = "Your disciplined daily investing companion.";

  // Populate personal details if present
  $("firstName").value = user.first_name || "";
  $("lastName").value = user.last_name || "";
  $("country").value = user.country || "South Africa";
  $("timezone").value = user.timezone || "Africa/Johannesburg";

  // Load investment profile
  const prof = await api("/api/profile", "GET");
  const p = prof.data.profile;

  if (p) {
    $("monthly").value = p.monthly_invest_amount;
    $("risk").value = p.risk_appetite;
    $("horizon").value = p.time_horizon;
    $("markets").value = p.markets;
    $("experience").value = p.experience_level;
  }
}

// Run on load
refreshState();
