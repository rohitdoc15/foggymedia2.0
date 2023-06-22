var lines = document.getElementsByTagName("text");
var currentLine = 0;

function glow() {
  if (currentLine >= lines.length) {
    currentLine = 0;
  }
  lines[currentLine].classList.remove("glow");
  currentLine++;
  if (currentLine < lines.length) {
    lines[currentLine].classList.add("glow");
  }
}

setInterval(glow, 1000);

