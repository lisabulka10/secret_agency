function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

const form = document.getElementById('filter-form');


document.querySelectorAll('select.autosubmit').forEach(function(select) {
    select.addEventListener('change', function() {
        form.submit();
    });
});


document.querySelectorAll('input.autosubmit').forEach(function(input) {
    input.addEventListener('input', debounce(function() {
        form.submit();
    }, 500));
});


document.querySelectorAll('input.autosubmit').forEach(function(input) {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            form.submit();
        }
    });
});
