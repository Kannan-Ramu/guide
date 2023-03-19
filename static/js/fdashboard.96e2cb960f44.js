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
                    csrfmiddlewaretoken: csrftoken 
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
