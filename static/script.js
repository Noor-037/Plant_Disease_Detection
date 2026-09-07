// const imageInput = document.getElementById('image');
// const preview = document.getElementById('preview');

// imageInput.addEventListener('change', () => {
//   const file = imageInput.files[0];
//   if (file) {
//     preview.src = URL.createObjectURL(file);
//     preview.style.display = 'block';
//   }
// });

// function startAnalysis() {
//   const plantType = document.getElementById('plant_type').value; // may be ""
//   const file = imageInput.files[0];

//   if (!file) {
//     alert("Please capture or select a leaf photo first.");
//     return;
//   }

//   const formData = new FormData();
//   formData.append('plant_type', plantType); // optional, sent even if empty
//   formData.append('image', file);

//   document.getElementById('analyzeBtn').disabled = true;
//   document.getElementById('steps').style.display = 'none';

//   fetch('/analyze', { method: 'POST', body: formData })
//     .then(res => res.json())
//     .then(() => pollStatus())
//     .catch(err => {
//       alert("Failed to send image: " + err);
//       document.getElementById('analyzeBtn').disabled = false;
//     });
// }

// function pollStatus() {
//   fetch('/status')
//     .then(res => res.json())
//     .then(data => {
//       document.getElementById('plant').innerText = data.plant || '-';
//       document.getElementById('disease').innerText = data.disease || '-';
//       document.getElementById('confidence').innerText =
//           data.confidence ? data.confidence + '%' : '-';
//       document.getElementById('pesticide').innerText = data.pesticide || '-';
//       document.getElementById('dosage_ml').innerText =
//           data.dosage_ml ? data.dosage_ml + ' ml' : '-';

//       const stateBadge = document.getElementById('stateBadge');
//       stateBadge.innerText = data.state;
//       stateBadge.className = 'badge ' + data.state;

//       const sevBadge = document.getElementById('severityBadge');
//       sevBadge.innerText = data.severity || '-';
//       sevBadge.className = 'badge sev-' + (data.severity || 'None');

//       if (data.state === 'done') {
//         const stepsList = document.getElementById('steps');
//         stepsList.innerHTML = '';
//         (data.steps || []).forEach(s => {
//           const li = document.createElement('li');
//           li.innerText = s;
//           stepsList.appendChild(li);
//         });
//         stepsList.style.display = 'block';
//         document.getElementById('analyzeBtn').disabled = false;
//         loadHistory();
//       } else if (data.state === 'error') {
//         document.getElementById('analyzeBtn').disabled = false;
//       } else {
//         setTimeout(pollStatus, 700);
//       }
//     });
// }

// function loadHistory() {
//   fetch('/history')
//     .then(res => res.json())
//     .then(items => {
//       const list = document.getElementById('historyList');
//       if (!items.length) {
//         list.innerHTML = '<span id="historyEmpty">No scans yet.</span>';
//         return;
//       }
//       list.innerHTML = items.map(item => `
//         <div class="history-item">
//           <span>${item.time} — ${item.plant}: ${item.disease} (${item.severity})</span>
//           <span>${item.dosage_ml} ml</span>
//         </div>
//       `).join('');
//     });
// }

// loadHistory();

const imageInput = document.getElementById('image');
const preview = document.getElementById('preview');

let cameraStream = null;


// ===============================
// IMAGE UPLOAD PREVIEW
// ===============================

imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];

    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
    }
});


// ===============================
// OPEN CAMERA
// ===============================

function openCamera() {

    const cameraView = document.getElementById('cameraView');
    const video = document.getElementById('video');

    cameraView.style.display = 'block';

    navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: { ideal: "environment" }
        },
        audio: false
    })
    .then((stream) => {

        cameraStream = stream;

        video.srcObject = stream;

        video.play();

    })
    .catch((error) => {

        console.error("Camera Error:", error);

        alert(
            "Camera open nahi ho raha.\n\n" +
            "Please browser me Camera permission Allow karein."
        );

        cameraView.style.display = 'none';
    });
}


// ===============================
// TAKE PHOTO
// ===============================

function takeSnapshot() {

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');

    if (!video.videoWidth || !video.videoHeight) {
        alert("Camera ready nahi hai. Thoda wait karein.");
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');

    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Convert canvas image to file
    canvas.toBlob((blob) => {

        const file = new File(
            [blob],
            "camera-leaf-photo.jpg",
            {
                type: "image/jpeg"
            }
        );

        // Put captured image into file input
        const dataTransfer = new DataTransfer();

        dataTransfer.items.add(file);

        imageInput.files = dataTransfer.files;

        // Show preview
        preview.src = URL.createObjectURL(blob);
        preview.style.display = 'block';

        // Close camera
        closeCamera();

    }, "image/jpeg", 0.9);
}


// ===============================
// CLOSE CAMERA
// ===============================

function closeCamera() {

    const cameraView = document.getElementById('cameraView');
    const video = document.getElementById('video');

    if (cameraStream) {

        cameraStream.getTracks().forEach(track => {
            track.stop();
        });

        cameraStream = null;
    }

    video.srcObject = null;

    cameraView.style.display = 'none';
}


// ===============================
// DISEASE ANALYSIS
// ===============================

function startAnalysis() {

    const plantType =
        document.getElementById('plant_type').value;

    const file = imageInput.files[0];

    if (!file) {

        alert("Please capture or select a leaf photo first.");

        return;
    }

    const formData = new FormData();

    formData.append('plant_type', plantType);
    formData.append('image', file);

    const analyzeBtn =
        document.getElementById('analyzeBtn');

    analyzeBtn.disabled = true;

    document.getElementById('steps').style.display = 'none';

    // Show detecting status
    const stateBadge =
        document.getElementById('stateBadge');

    stateBadge.innerText = 'detecting';
    stateBadge.className = 'badge detecting';


    fetch('/analyze', {
        method: 'POST',
        body: formData
    })

    .then(res => {

        if (!res.ok) {
            throw new Error("Server error");
        }

        return res.json();

    })

    .then(() => {

        pollStatus();

    })

    .catch(err => {

        console.error(err);

        alert("Failed to send image: " + err);

        analyzeBtn.disabled = false;

        stateBadge.innerText = 'error';
        stateBadge.className = 'badge error';
    });
}


// ===============================
// POLL RESULT
// ===============================

function pollStatus() {

    fetch('/status')

    .then(res => res.json())

    .then(data => {

        document.getElementById('plant').innerText =
            data.plant || '-';

        document.getElementById('disease').innerText =
            data.disease || '-';

        document.getElementById('confidence').innerText =
            data.confidence !== null &&
            data.confidence !== undefined
                ? data.confidence + '%'
                : '-';

        document.getElementById('pesticide').innerText =
            data.pesticide || '-';

        document.getElementById('dosage_ml').innerText =
            data.dosage_ml
                ? data.dosage_ml + ' ml'
                : '-';


        // Status badge
        const stateBadge =
            document.getElementById('stateBadge');

        stateBadge.innerText =
            data.state || 'idle';

        stateBadge.className =
            'badge ' + (data.state || 'idle');


        // Severity badge
        const sevBadge =
            document.getElementById('severityBadge');

        sevBadge.innerText =
            data.severity || '-';

        sevBadge.className =
            'badge sev-' +
            (data.severity || 'None');


        // ==========================
        // DONE
        // ==========================

        if (data.state === 'done') {

            const stepsList =
                document.getElementById('steps');

            stepsList.innerHTML = '';

            (data.steps || []).forEach(step => {

                const li =
                    document.createElement('li');

                li.innerText = step;

                stepsList.appendChild(li);
            });

            if (data.steps && data.steps.length > 0) {
                stepsList.style.display = 'block';
            }

            document.getElementById('analyzeBtn')
                .disabled = false;

            loadHistory();

        }

        // ==========================
        // ERROR
        // ==========================

        else if (data.state === 'error') {

            document.getElementById('analyzeBtn')
                .disabled = false;

        }

        // ==========================
        // STILL DETECTING
        // ==========================

        else {

            setTimeout(pollStatus, 700);
        }

    })

    .catch(err => {

        console.error("Status error:", err);

        setTimeout(pollStatus, 1000);
    });
}


// ===============================
// HISTORY
// ===============================

function loadHistory() {

    fetch('/history')

    .then(res => res.json())

    .then(items => {

        const list =
            document.getElementById('historyList');

        if (!items.length) {

            list.innerHTML =
                '<span id="historyEmpty">No scans yet.</span>';

            return;
        }

        list.innerHTML = items.map(item => `

            <div class="history-item">

                <span>
                    ${item.time} —
                    ${item.plant}:
                    ${item.disease}
                    (${item.severity})
                </span>

                <span>
                    ${item.dosage_ml} ml
                </span>

            </div>

        `).join('');
    })

    .catch(err => {
        console.error("History error:", err);
    });
}


// Load history when page opens
loadHistory();
