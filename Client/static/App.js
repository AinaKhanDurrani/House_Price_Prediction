function predictPrice() {
    const data = {
      Area: parseFloat(document.getElementById('area').value),
      Bedrooms: parseInt(document.getElementById('bedrooms').value),
      Bathrooms: parseFloat(document.getElementById('bathrooms').value),
      Floors: parseInt(document.getElementById('floors').value),
      YearBuilt: parseInt(document.getElementById('yearBuilt').value),
      Location: document.getElementById('location').value,
      Condition: document.getElementById('condition').value,
      Garage: document.getElementById('garage').value
    };
  
    const url = "/predict";  // Since both the frontend and backend are on the same server
    document.getElementById('result').innerText = "Predicting...";
  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.predicted_price !== undefined) {
        document.getElementById('result').innerHTML =
          `🏠 Predicted Price: <strong style="color: green;">$${data.predicted_price}</strong>`;
      } else {
        document.getElementById('result').innerText = "Prediction failed.";
      }
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById('result').innerText = 'Error: ' + error.message;
    });
  }
  