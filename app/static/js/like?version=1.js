var score = document.getElementById("scoreCounter");
score.innerHTML = "0";
var scoreValue = 0;
checkScore();

function upVote() {
  scoreValue++;
  score.innerHTML = scoreValue;
  checkScore();
}

function downVote() {
  scoreValue--;
  score.innerHTML = scoreValue;
  checkScore();
}

function checkScore() {
  if (scoreValue < 0) {
    score.style.color = "#FF586C";
  } else if (scoreValue > 0) {
    score.style.color = "#6CC576";
  } else {
    score.style.color = "#666666";
  }
}