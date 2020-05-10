$(document).ready(function () {
  $(document).on("input", ".search-input", function () {
    is_changed_input = $(".search-input").val();
    $(".search-input").on("keyup", function () {
      var input_data = $(".search-input").val();
      if (input_data.length >= 3) {
        if (input_data === is_changed_input && input_data.length >= 3) {
          $("#gameid").val("");
          is_changed_input = {};
          let timersId = setTimeout(function () {
            $(".search").css("display", "inherit");
            $(".loading").remove();
            $(".search-result").remove();
            $(".results").append(
              "<div class='loading'><p>Searching...</p></div>"
            );
          }, 1200);
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
                  if (result["genres"] == undefined) {
                    result["genres"] = "Genres is not provided";
                  }
                  if (result["first_release_date"] == undefined) {
                    result["first_release_date"] =
                      "Release date is not provided";
                  }
                  if (result["id"] == undefined) {
                  } else {
                    if (
                      (result["summary"] == undefined) &
                      (result["storyline"] == undefined)
                    ) {
                      description = "Game description is not provided";
                    } else if (
                      (result["storyline"] != undefined) &
                      (result["summary"] == undefined)
                    ) {
                      description = result["storyline"];
                    } else {
                      description = result["summary"];
                    }
                    $(".results").append(
                      "<div class='search-result' id='" +
                        counter +
                        "'><div class='result-title'><h3><a class='choose-click' data-id='" +
                        result["id"] +
                        "'>" +
                        result["name"] +
                        "</a></h3></div><div class='result-releasedate'><h2>" +
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
                }
              },
              dataType: "json",
            });
          }, 1450);
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
        if ($(".search-input").val().length < 3) {
          $(".results").empty();
        } else {
          container.show();
        }
      }
    }
    if (
      (container.has(e.target).length === 0) &
      (e.target.className != "search-input")
    ) {
      container.hide();
    }
  });
  $(".results").on("click", ".choose-click", function () {
    document.getElementById("id_title").value = this.text;
    document.getElementById("gameid").value = this.dataset.id;
    $(".search").hide();
  });
});
