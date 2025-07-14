 // Debounce-функция: запускает колбэк через delay мс после последнего вызова
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

const form = document.getElementById('filter-form');

  // Автосабмит при изменении селектов
document.querySelectorAll('select.autosubmit').forEach(function(select) {
    select.addEventListener('change', function() {
        form.submit();
    });
});

  // Автосабмит input-ов с debounce
document.querySelectorAll('input.autosubmit').forEach(function(input) {
    input.addEventListener('input', debounce(function() {
        form.submit();
    }, 500)); // 500 мс задержка
});

  // При нажатии Enter — сразу отправить (без ожидания debounce)
document.querySelectorAll('input.autosubmit').forEach(function(input) {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            form.submit();
        }
    });
});
