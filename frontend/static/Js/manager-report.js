// Render report specific charts
function renderReport(data) {
  let ctx = document.getElementById('reportChart');
  if (!ctx) return;

  let chartType = 'bar';
  let chartData = {};
  let options = { responsive: true };

  if (reportName === 'current-student') {
    chartType = 'line';
    const dates = [...new Set(data.map(r => r.StartDate).filter(Boolean))]
      .sort((a, b) => new Date(a) - new Date(b));
    const studentCounts = dates.map(d => data.filter(r => r.StartDate === d && r.Stage === 'Student').length);
    const offerCounts = dates.map(d => data.filter(r => r.StartDate === d && r.Stage === 'Offer').length);
    chartData = {
      labels: dates,
      datasets: [
        { label: 'Students', data: studentCounts, fill: false, borderColor: '#5e4ae3' },
        { label: 'Offers', data: offerCounts, fill: false, borderColor: '#f06595' }
      ]
    };
  } else if (reportName === 'enrolled-offer') {
    chartType = 'bar';
    const totalStudents = data.filter(r => r.Stage === 'Student').length;
    const totalOffers = data.filter(r => r.Stage === 'Offer').length;
    chartData = {
      labels: ['Students', 'Offers'],
      datasets: [{ label: 'Count', data: [totalStudents, totalOffers], backgroundColor: ['#5e4ae3', '#74c69d'] }]
    };
  } else if (reportName === 'visa-breakdown') {
    chartType = 'doughnut';
    const visaCounts = {};
    data.forEach(r => {
      let status = r['Visa Status'];
      if (!status) {
        for (const key in r) {
          if (key && key.toLowerCase().replace(/\s+/g, '') === 'visastatus') {
            status = r[key];
            break;
          }
        }
      }
      const v = (status || 'Unknown').trim();
      visaCounts[v] = (visaCounts[v] || 0) + 1;
    });
    chartData = {
      labels: Object.keys(visaCounts),
      datasets: [{
        data: Object.values(visaCounts),
        backgroundColor: ['#5e4ae3', '#f06595', '#74c69d', '#ffd43b', '#adb5bd'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    };
    options.plugins = { legend: { position: 'bottom' } };
  } else if (reportName === 'offer-expiry') {
    chartType = 'line';
    const expiryDates = [...new Set(data.map(r => r['Offer Expiry Date']).filter(Boolean))]
      .sort((a, b) => new Date(a) - new Date(b));
    const expiryCounts = expiryDates.map(d => data.filter(r => r['Offer Expiry Date'] === d).length);
    chartData = {
      labels: expiryDates,
      datasets: [{ label: 'Expiry Count', data: expiryCounts, fill: false, borderColor: '#5e4ae3' }]
    };
  }

  new Chart(ctx, {
    type: chartType,
    data: chartData,
    options
  });
}

fetch('/api/data')
  .then(r => r.json())
  .then(renderReport)
  .catch(err => console.error('Data load error:', err));
