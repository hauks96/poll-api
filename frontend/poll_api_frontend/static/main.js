function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


$('.nav-item').on('click', function (){
    let current_element = $(this)
    let all_elements = document.getElementsByClassName('nav-item');
    for (let i=0; i<all_elements.length; i++){
        all_elements[i].classList.remove('nav-focused');
    }
    current_element.addClass('nav-focused');
})