document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const loader = document.getElementById("loader");
  const audioInput = document.getElementById("audioInput");
  const playBtn = document.getElementById("playBtn");

  // Initialize wavesurfer
  let wavesurfer = WaveSurfer.create({
    container: "#waveform",
    waveColor: "#ccc",
    progressColor: "#4caf50",
    height: 80,
  });

  // Handle file preview
  audioInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = function (evt) {
        wavesurfer.load(evt.target.result);
        playBtn.style.display = "inline-block";
      };

      reader.readAsDataURL(file);
    }
  });

  // Play/pause button
  playBtn.addEventListener("click", function () {
    wavesurfer.playPause();
  });

  // Show loader on form submit
  form.addEventListener("submit", function () {
    loader.style.display = "block";
  });
});
