document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const loader = document.getElementById("loader");
  const audioInput = document.getElementById("audioInput");
  const playBtn = document.getElementById("playBtn");

  let wavesurfer = WaveSurfer.create({
    container: "#waveform",
    waveColor: "#ccc",
    progressColor: "#4caf50",
    height: 80,
  });

  playBtn.disabled = true; // disable until ready

  audioInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
      wavesurfer.loadBlob(file);
      playBtn.style.display = "inline-block";
      playBtn.disabled = true;  // disable while loading
    }
  });

  wavesurfer.on('ready', () => {
    playBtn.disabled = false;
  });

  playBtn.addEventListener("click", function () {
    wavesurfer.playPause();
  });

  form.addEventListener("submit", function () {
    loader.style.display = "block";
  });
});
