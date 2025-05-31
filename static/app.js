document.getElementById('astro-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const form = e.target;
  const data = {
    name: form.name.value,
    birthdate: form.birthdate.value,
    birthtime: form.birthtime.value,
    birthplace: form.birthplace.value
  };
  
  const response = await fetch('http://localhost:5000/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  const result = await response.json();
  document.getElementById('report').innerText = result.report;
});
