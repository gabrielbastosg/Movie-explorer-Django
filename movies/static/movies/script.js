const searchInput = document.getElementById("search-input");
const searchForm = document.getElementById("search-form");
const genreSelect = document.querySelector('select[name="genre"]');

const searchButton = searchForm?.querySelector("button");

function setLoading(isLoading) {
    if (!searchButton) return;

    searchButton.innerText = isLoading ? "Buscando..." : "Buscar";
    searchButton.disabled = isLoading;
}

if (searchInput && searchForm) {
    let timeout;

    searchInput.addEventListener("input", () => {
        clearTimeout(timeout);

        timeout = setTimeout(() => {
            setLoading(true);
            searchForm.submit();
        }, 1000);
    });
}

if (genreSelect && searchForm) {
    genreSelect.addEventListener("change", () => {
        setLoading(true);
        searchForm.submit();
    });
}

window.addEventListener("load", () => {
    setLoading(false);
});