
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

var hamburger = document.querySelector(".hamburger");
    hamburger.addEventListener("click", function(){
        document.querySelector("body").classList.toggle("active");
    })

$(document).ready(function () {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $('#approved-checkbox').change(function() {
            let guide_url = "{% url 'guide-approve' id=team.teamID %}"
            if (this.checked)
            {
                console.log("Guide URL: ",guide_url)
                console.log("Inside If")
                $.post(guide_url, {
                    // id: '{{team.teamID}}',
                    guide_approved: this.checked, 
                    csrfmiddlewaretoken: getCookie('csrftoken') 
                });

            }
            else {
                console.log("Guide URL: ",guide_url)
                console.log("Inside else ")
                $.post(guide_url, {
                    // id: '{{team.teamID}}',
                    guide_approved: this.checked, 
                    csrfmiddlewaretoken: '{{ csrf_token }}' 
                });
            }
        });
    }); 
