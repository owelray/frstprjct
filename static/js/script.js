var result = 0;
var rater = document.getElementById("rate");
var stars = Array.from(rater.children);
rater.addEventListener("touchmove", raterEnd);
stars.forEach(function (item) {
  item.addEventListener("mousemove", rateStar.bind(null, item, showResult));
});
stars.forEach(function (item) {
  item.addEventListener("mouseout", changeResult.bind(showResult));
});

add_form.textarea.addEventListener("input", calcChars, false);
add_form.textarea.addEventListener("focus", calcChars, false);

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
    callback();
  }
}

function changeResult(callback) {
  var checkedresult = document.querySelector("input[name=rating]:checked");
  if (checkedresult) {
    result = parseFloat(checkedresult.dataset.score);
    showResult(result);
  } else {
    result = 0;
    showResult(result);
  }
}

function showResult(number) {
  document.getElementById("result").innerHTML = result + "/10";
}

var max = 450;
function calcChars() {
  var left = max - this.value.length;
  if (left < 0) {
    this.value = this.value.substr(0, max);
    return false;
  }
  counter.style.color = left <= 10 ? "#ff3300" : "#67f4fe";
  counter.textContent = max - this.value.length;
}

