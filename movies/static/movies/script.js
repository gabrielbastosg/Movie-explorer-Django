const searchInput = document.getElementById("search-input");
const searchForm = document.getElementById("search-form");
const genreSelect = document.querySelector('select[name="genre"]');


if (searchInput && searchForm) {
    let timeout;

    searchInput.addEventListener("input", () => {
        clearTimeout(timeout);

        timeout = setTimeout(() => {
            searchForm.submit();
        }, 1000);
    });
}

if (genreSelect && searchForm) {
    genreSelect.addEventListener("change", () => {
        searchForm.submit();
    });
}