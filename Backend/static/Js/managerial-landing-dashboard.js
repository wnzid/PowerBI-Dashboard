document.addEventListener("DOMContentLoaded", function () {
  let allData = [];
  let chartCurrent, chartEnrolled, chartVisa, chartExpiry;

  function renderCharts(data) {
    if (chartCurrent) chartCurrent.destroy();
    if (chartEnrolled) chartEnrolled.destroy();
    if (chartVisa) chartVisa.destroy();
    if (chartExpiry) chartExpiry.destroy();

    const dates = [...new Set(data.map(r => r.StartDate).filter(Boolean))]
      .sort((a, b) => new Date(a) - new Date(b));
    const studentCounts = dates.map(d => data.filter(r => r.StartDate === d && r.Stage === "Student").length);
    const offerCounts = dates.map(d => data.filter(r => r.StartDate === d && r.Stage === "Offer").length);

    chartCurrent = new Chart(document.getElementById("chart-current-enrolled"), {
      type: "line",
      data: {
        labels: dates,
        datasets: [
          { label: "Students", data: studentCounts, fill: false },
          { label: "Offers", data: offerCounts, fill: false }
        ]
      },
      options: { responsive: true }
    });

    const totalStudents = data.filter(r => r.Stage === "Student").length;
    const totalOffers = data.filter(r => r.Stage === "Offer").length;
    chartEnrolled = new Chart(document.getElementById("chart-enrolled-offer"), {
      type: "bar",
      data: {
        labels: ["Students", "Offers"],
        datasets: [{ label: "Count", data: [totalStudents, totalOffers] }]
      },
      options: { responsive: true }
    });

    const visaCounts = {};
    data.forEach(r => {
      const v = r["Visa Status"] || "Unknown";
      visaCounts[v] = (visaCounts[v] || 0) + 1;
    });
    chartVisa = new Chart(document.getElementById("chart-visa-breakdown"), {
      type: "pie",
      data: {
        labels: Object.keys(visaCounts),
        datasets: [{ data: Object.values(visaCounts) }]
      },
      options: { responsive: true }
    });

    const expiryDates = [...new Set(data.map(r => r["Offer Expiry Date"]).filter(Boolean))]
      .sort((a, b) => new Date(a) - new Date(b));
    const expiryCounts = expiryDates.map(d => data.filter(r => r["Offer Expiry Date"] === d).length);
    chartExpiry = new Chart(document.getElementById("chart-offer-expiry-surge"), {
      type: "line",
      data: {
        labels: expiryDates,
        datasets: [{ label: "Expiry Count", data: expiryCounts, fill: false }]
      },
      options: { responsive: true }
    });

    const total = data.length;
    const payYes = data.filter(r => r["Do you want to pay more than 50% upfront fee?"] === "Yes").length;
    const pctPay = total ? Math.round((payYes / total) * 100) : 0;
    document.getElementById("story-due-payments").innerText =
      pctPay + "% opted >50% upfront fee";

    const deferYes = data.filter(r => r["Is the offer deferred?"] === "Yes").length;
    const pctDef = total ? Math.round((deferYes / total) * 100) : 0;
    document.getElementById("story-course-performance").innerText =
      "-" + pctDef + "% deferral rate";

    const reasonCounts = {};
    data.forEach(r => {
      const reason = r["Study Reason"] || "Unknown";
      reasonCounts[reason] = (reasonCounts[reason] || 0) + 1;
    });
    const topReason = Object.keys(reasonCounts).reduce((a, b) =>
      reasonCounts[a] >= reasonCounts[b] ? a : b
    );
    const topPct = total ? Math.round((reasonCounts[topReason] / total) * 100) : 0;
    document.getElementById("story-study-reasons").innerText =
      "+" + topPct + "% chose " + topReason;
  }

  fetch("/api/data")
    .then(res => res.json())
    .then(data => {
      allData = data;
      renderCharts(allData);
    })
    .catch(err => console.error("Data load error:", err));

  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const q = this.value.toLowerCase();
      const filtered = allData.filter(row =>
        Object.values(row).some(v => String(v).toLowerCase().includes(q))
      );
      renderCharts(filtered);
    });
  }

  const toggle = document.querySelector(".dropdown-toggle");
  const menu = document.querySelector(".profile-dropdown");
  if (toggle && menu) {
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      menu.style.display = menu.style.display === "block" ? "none" : "block";
    });
    document.addEventListener("click", function () {
      if (menu.style.display === "block") menu.style.display = "none";
    });
    document.getElementById("logout-link").addEventListener("click", function (e) {
      e.preventDefault();
    });
  }
});
