var result = 0;
var rater = document.getElementById("rate");
var stars = Array.from(rater.children);
rater.addEventListener("touchmove", raterEnd);
stars.forEach(function (item) {
  item.addEventListener("mousemove", rateStar.bind(null, item, showResult));
});

function raterEnd(e) {
  e.preventDefault();
  e.stopPropagation();
  var changedTouch = e.changedTouches[0];
  var elem = document.elementFromPoint(
    changedTouch.clientX,
    changedTouch.clientY
  );
  endElem = elem;
  rateStar(elem, showResult);
}

function rateStar(ratedItem, callback) {
  if (stars.includes(ratedItem)) {
    result = parseFloat(ratedItem.dataset.score);
    stars.forEach(function (item) {
      var position = parseFloat(item.dataset.score);
    });
  }
  callback();
}
function showResult() {
  document.getElementById("result").innerHTML = result + "/10";
}
