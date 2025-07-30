// Enhanced Chart Configuration
document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('macdChart').getContext('2d');
  
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        { 
          label: 'MACD',
          borderColor: 'rgb(75, 192, 192)',
          borderWidth: 2,
          tension: 0.1
        },
        { 
          label: 'Signal',
          borderColor: 'rgb(255, 159, 64)',
          borderWidth: 2
        },
        { 
          label: 'Histogram',
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 1,
          type: 'bar'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { 
          type: 'realtime',
          realtime: {
            duration: 60000,
            refresh: 1000,
            delay: 200
          }
        },
        y: {
          title: { display: true, text: 'Value' }
        }
      },
      plugins: {
        legend: { position: 'top' },
        tooltip: { mode: 'index', intersect: false }
      }
    }
  });

  // WebSocket handlers remain unchanged
});
