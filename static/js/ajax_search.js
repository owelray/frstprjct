$(document).ready(function () {
  $(".search-input").keyup(function () {
    $.ajax({
      type: "GET",
      async: true,
      url: "/gamelist/ajax/search/",
      data: { data: $(".search-input").val() },
      success: function (data) {
        var obj = data["name"];
        for (var counter = 0; counter != obj.length; counter++) {
          result = obj[counter];
          $(".search").append(result["name"]);
        }
      },
      dataType: "json",
    });
  });
});
