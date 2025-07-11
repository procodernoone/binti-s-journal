window.onload = function () {
  const bio = localStorage.getItem("bintiBio");
  if (bio) {
    document.getElementById("bioDisplay").innerText = bio;
    document.getElementById("bioInput").style.display = "none";
  }
};

function saveBio() {
  const bioText = document.getElementById("bioInput").value;
  localStorage.setItem("bintiBio", bioText);
  document.getElementById("bioDisplay").innerText = bioText;
  document.getElementById("bioInput").style.display = "none";
}
