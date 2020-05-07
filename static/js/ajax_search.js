$(document).ready(function () {
  $(document).on("input", ".search-input", function () {
    is_changed_input = $(".search-input").val();
    $(".search-input").on("keypress keydown", function () {
      var input_data = $(".search-input").val();
      if (input_data.length >= 3) {
        if (input_data == is_changed_input) {
          is_changed_input = {};
          let timersId = setTimeout(function () {
            $(".search").css("display", "inherit");
            $(".loading").remove();
            $(".search-result").remove();
            $(".results").append(
              "<div class='loading'><p>Searching...</p></div>"
            );
          }, 1300);
          let timerId = setTimeout(function () {
            $.ajax({
              type: "GET",
              async: true,
              url: "/gamelist/ajax/search/",
              data: { data: $(".search-input").val() },
              success: function (data) {
                $(".loading").remove();
                var obj = data["results"];
                for (var counter = 0; counter != obj.length; counter++) {
                  var result = obj[counter];
                  var description;
                  if (
                    (result["summary"].length > 0) &
                    (result["storyline"] == undefined)
                  ) {
                    description = result["summary"];
                  } else if (
                    (result["summary"] == undefined) &
                    (result["storyline"] == undefined)
                  ) {
                    description = "Game description is not provided";
                  } else {
                    description = result["storyline"];
                  }
                  $(".results").append(
                    "<div class='search-result'><div class='result-title'><h3>" +
                      result["name"] +
                      "</h3></div><div class='result-releasedate'><h2>" +
                      result["first_release_date"] +
                      "</h2></div><div class='result-genres'><h2>" +
                      result["genres"] +
                      "</h2></div><div class='result-description'><p>" +
                      description +
                      "</p></div><div class='result-buttons'><h2><a href='" +
                      result["url"] +
                      "' target='_blank'>See more</a></h2></div></div>"
                  );
                }
              },
              dataType: "json",
            });
          }, 1550);
          $(".search-input").on("keydown", function () {
            clearTimeout(timersId);
            clearTimeout(timerId);
          });
        } else {
        }
      } else {
        $(".search").css("display", "none");
      }
    });
  });
  $(document).mouseup(function (e) {
    var container = $(".search");
    if (e.target.className == "search-input") {
      if ($(".results").is(":empty")) {
      } else {
        container.show();
      }
    }
    if (
      (container.has(e.target).length === 0) &
      (e.target.className != "search-input")
    ) {
      container.hide();
    }
  });
});
