const video = document.getElementById('video');
const status = document.getElementById('status');
const output = document.getElementById('output');
const canvas = document.getElementById('canvas');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    status.textContent = 'Camera active—scanning every 3s';
    setInterval(captureFrame, 3000);
  })
  .catch(err => status.textContent = 'Camera error: ' + err);

async function captureFrame() {
  canvas.getContext('2d').drawImage(video, 0, 0);
  canvas.toBlob(async blob => {
    const form = new FormData();
    form.append('file', blob, 'frame.jpg');
    try {
      const res = await fetch('http://localhost:8000/analyze/', {
        method: 'POST', body: form
      });
      const json = await res.json();
      if (json.error)
        output.textContent = 'OCR Error: ' + JSON.stringify(json.found);
      else {
        const {fuel, required, final, values} = json;
        output.innerHTML = `
          <strong>Extracted:</strong> L=${values.left}, C=${values.ctr}, R=${values.right}, P=${values.pre}<br>
          <strong>Results:</strong> Fuel=${fuel}, Required=${required}, Final=${final}
        `;
      }
    } catch (e) {
      status.textContent = 'Server error: ' + e;
    }
  }, 'image/jpeg');
}
