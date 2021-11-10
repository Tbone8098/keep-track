var listOfClickables = document.querySelectorAll('.clickable')

for (const btn of listOfClickables) {
    btn.addEventListener('click', function(){
        url = this.getAttribute('url')
        window.location.href = url
    })
}