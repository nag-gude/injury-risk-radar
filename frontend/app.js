const API_BASE_KEY = "api_base";
const TOKEN_KEY = "access_token";

function getApiBase() {
  return localStorage.getItem(API_BASE_KEY) || "/api";
}

function setApiBase(value) {
  localStorage.setItem(API_BASE_KEY, value);
}

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function apiRequest(path, options = {}) {
  const headers = options.headers || {};
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  headers["Content-Type"] = "application/json";

  const response = await fetch(`${getApiBase()}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}

function showAlert(targetId, message, isSuccess = false) {
  const el = document.getElementById(targetId);
  if (!el) return;
  el.textContent = message;
  el.style.display = "block";
  el.classList.toggle("success", isSuccess);
}

function hideAlert(targetId) {
  const el = document.getElementById(targetId);
  if (!el) return;
  el.style.display = "none";
  el.classList.remove("success");
}

function bindApiBaseInput() {
  const apiInput = document.getElementById("api-base");
  if (!apiInput) return;
  apiInput.value = getApiBase();
  apiInput.addEventListener("change", (event) => {
    setApiBase(event.target.value);
  });
}

async function handleRegister(event) {
  event.preventDefault();
  hideAlert("register-alert");

  const payload = {
    email: event.target.email.value,
    password: event.target.password.value,
    role: event.target.role.value,
    sport: event.target.sport.value,
    age_group: event.target.age_group.value,
  };

  try {
    await apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    showAlert("register-alert", "Account created. Please log in.", true);
    event.target.reset();
  } catch (error) {
    showAlert("register-alert", error.message);
  }
}

async function handleLogin(event) {
  event.preventDefault();
  hideAlert("login-alert");

  const payload = {
    email: event.target.email.value,
    password: event.target.password.value,
  };

  try {
    const data = await apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setToken(data.access_token);
    window.location.href = "dashboard.html";
  } catch (error) {
    showAlert("login-alert", error.message);
  }
}

async function loadDashboard() {
  try {
    const data = await apiRequest("/dashboard");
    const summary = data.today;

    document.getElementById("risk-level").textContent = summary.risk_level;
    document.getElementById("risk-score").textContent = `${summary.risk_score}`;
    document.getElementById("load-ratio").textContent = summary.load_ratio;
    document.getElementById("fatigue-score").textContent = summary.fatigue_score;

    const recList = document.getElementById("recommendations");
    recList.innerHTML = "";
    summary.recommendations.forEach((rec) => {
      const li = document.createElement("li");
      li.textContent = rec;
      recList.appendChild(li);
    });

    const tableBody = document.getElementById("log-table");
    tableBody.innerHTML = "";
    data.logs.slice(-14).forEach((log) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${log.log_date}</td>
        <td>${log.training_duration_min}</td>
        <td>${log.training_intensity}</td>
        <td>${log.soreness}</td>
        <td>${log.sleep_quality}</td>
        <td>${log.training_load}</td>
      `;
      tableBody.appendChild(row);
    });

    if (window.Chart) {
      const labels = data.logs.map((log) => log.log_date);
      const loads = data.logs.map((log) => log.training_load);
      const ctx = document.getElementById("loadChart").getContext("2d");
      if (window.loadChartInstance) {
        window.loadChartInstance.destroy();
      }
      window.loadChartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Training Load",
              data: loads,
              borderColor: "#2563eb",
              backgroundColor: "rgba(37, 99, 235, 0.2)",
              tension: 0.3,
            },
          ],
        },
        options: { responsive: true },
      });
    }
  } catch (error) {
    showAlert("dashboard-alert", error.message);
  }
}

async function handleLogSubmit(event) {
  event.preventDefault();
  hideAlert("log-alert");

  const isRestDay = event.target.rest_day.checked;
  const trainingDuration = isRestDay
    ? 0
    : Number(event.target.training_duration_min.value);
  const trainingIntensity = isRestDay
    ? 1
    : Number(event.target.training_intensity.value);

  const payload = {
    log_date: event.target.log_date.value,
    training_duration_min: trainingDuration,
    training_intensity: trainingIntensity,
    soreness: Number(event.target.soreness.value),
    sleep_quality: Number(event.target.sleep_quality.value),
    rest_day: isRestDay,
  };

  try {
    await apiRequest("/logs", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    showAlert("log-alert", "Log saved successfully.", true);
    await loadDashboard();
    event.target.reset();
    const dateInput = event.target.log_date;
    if (dateInput) {
      dateInput.valueAsDate = new Date();
    }
  } catch (error) {
    showAlert("log-alert", error.message);
  }
}

function handleLogout() {
  clearToken();
  window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", () => {
  bindApiBaseInput();

  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", handleRegister);
  }

  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }

  const dashboard = document.getElementById("dashboard");
  if (dashboard) {
    loadDashboard();
  }

  const logForm = document.getElementById("log-form");
  if (logForm) {
    logForm.addEventListener("submit", handleLogSubmit);
    const restDayToggle = logForm.querySelector("#rest_day");
    const durationInput = logForm.querySelector("#training_duration_min");
    const intensityInput = logForm.querySelector("#training_intensity");
    if (restDayToggle && durationInput && intensityInput) {
      const toggleInputs = () => {
        const isRestDay = restDayToggle.checked;
        durationInput.required = !isRestDay;
        intensityInput.required = !isRestDay;
        durationInput.disabled = isRestDay;
        intensityInput.disabled = isRestDay;
        if (isRestDay) {
          durationInput.value = "0";
          intensityInput.value = "1";
        }
      };
      restDayToggle.addEventListener("change", toggleInputs);
      toggleInputs();
    }
  }

  const logoutButton = document.getElementById("logout");
  if (logoutButton) {
    logoutButton.addEventListener("click", handleLogout);
  }
});
