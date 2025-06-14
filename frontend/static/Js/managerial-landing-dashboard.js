document.addEventListener("DOMContentLoaded", function () {
  if (typeof Chart !== 'undefined' && typeof ChartDataLabels !== 'undefined') {
    Chart.register(ChartDataLabels);
  }
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
      let status = r["Visa Status"];
      if (!status) {
        for (const key in r) {
          if (key && key.toLowerCase().replace(/\s+/g, "") === "visastatus") {
            status = r[key];
            break;
          }
        }
      }
      const v = (status || "Unknown").trim();
      visaCounts[v] = (visaCounts[v] || 0) + 1;
    });
    chartVisa = new Chart(document.getElementById("chart-visa-breakdown"), {
      type: "doughnut",
      data: {
        labels: Object.keys(visaCounts),
        datasets: [{
          data: Object.values(visaCounts),
          backgroundColor: ['#5e4ae3', '#f06595', '#74c69d', '#ffd43b', '#adb5bd'],
          borderColor: '#fff',
          borderWidth: 2,
          spacing: 2
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom', labels: { padding: 20 } },
          datalabels: {
            color: '#000',
            formatter: (value, ctx) => {
              const sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
              return sum ? ((value / sum) * 100).toFixed(1) + '%';
            }
          }
        }
      }
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

  function loadData(data) {
    allData = data;
    renderCharts(allData);
  }

  if (window.APPROVED_DATA) {
    loadData(window.APPROVED_DATA);
  } else {
    fetch("/api/imported")
      .then(res => res.json())
      .then(loadData)
      .catch(err => console.error("Data load error:", err));
  }

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
});
