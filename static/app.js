const form = document.querySelector("#age-form");
const birthDateInput = document.querySelector("#birth-date");
const message = document.querySelector("#form-message");
const results = document.querySelector("#results");

const now = new Date();
const localToday = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
  .toISOString()
  .slice(0, 10);
birthDateInput.max = localToday;
document.querySelector("#today-date").textContent = new Intl.DateTimeFormat("en", {
  year: "numeric",
  month: "long",
  day: "numeric",
}).format(now);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";
  results.hidden = true;

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ birth_date: birthDateInput.value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");

    for (const key of ["years", "months", "days", "total_days", "total_weeks", "total_months"]) {
      const elementId = key.replaceAll("_", "-");
      document.getElementById(elementId).textContent = new Intl.NumberFormat().format(data[key]);
    }

    const days = data.days_until_birthday;
    const birthdayMessage = days === 0
      ? "Your birthday is today. Make it count."
      : `Your next birthday is in ${new Intl.NumberFormat().format(days)} ${days === 1 ? "day" : "days"}.`;
    document.querySelector("#birthday-message").textContent = birthdayMessage;
    results.hidden = false;
  } catch (error) {
    message.textContent = error.message;
  }
});