function sortlist(split_by) {
  var container = document.getElementById("list");
  var elements = container.childNodes;
  var sortMe = [];
  var chossing_butons = document.getElementsByClassName("choosed");
  var choosed_button = document.getElementById(split_by.length);

  chossing_butons[0].classList.remove("choosed");
  choosed_button.classList.add("choosed");
  for (var i = 0; i < elements.length; i++) {
    if (!elements[i].id) {
      continue;
    }
    var sortPart = elements[i].id.split(split_by);
    if (sortPart.length > 1) {
      sortMe.push([1 * sortPart[1], elements[i]]);
    }
  }
  sortMe.sort(function (x, y) {
    if (split_by === "----") {
      return x[0] - y[0];
    } else {
      return y[0] - x[0];
    }
  });
  for (var i = 0; i < sortMe.length; i++) {
    container.appendChild(sortMe[i][1]);
  }
}
