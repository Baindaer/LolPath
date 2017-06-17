var date = new Date();
var day = date.getDate();
var month = date.getMonth() + 1;
var year = date.getFullYear();
if (month < 10)
  month = "0" + month;
if (day < 10)
  day = "0" + day;
var today = year + "-" + month + "-" + day;
var mes = year + "-" + month;
$("#match_date").val(today)
$('#fancy-checkbox-success').prop('checked', true);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};



$(document).ready(function() {
    $("#champion_id").change(function() {
        var data = {
            "champion_id" : $("#champion_id").val(),
            "csrfmiddlewaretoken" : getCookie('csrftoken')
        }
        $.ajax({
            type: "POST",
            url: "/get/champion_lane/",
            dataType: "json",
            data: data,
            success: function(data) {
                $("#match_date").focus();
                $("#lane").val(data.lane);
            }
        });
    });
    $('#fancy-checkbox-success').click(function() {
      if ($(this).is(':checked')) {
        $('#checkbox_button').removeClass("btn-danger");
        $('#checkbox_button').addClass("btn-success");
        $('#checkbox_tag').text("Victory");
      } else {
        $('#checkbox_button').removeClass("btn-success");
        $('#checkbox_button').addClass("btn-danger");
        $('#checkbox_tag').text("Defeat");
      }
    });
});