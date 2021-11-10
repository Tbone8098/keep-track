let itemCompletes = document.querySelectorAll('.task-complete')

for (const complete of itemCompletes) {
    complete.addEventListener('click', function(){
        itemId = this.getAttribute('item_id')
        window.location.href = `/item/${itemId}/complete`
    })
}