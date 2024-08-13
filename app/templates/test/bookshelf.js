const searchBar = document.getElementById("search_bar")

function search_book() {
	let input = document.getElementById("search_bar").value
	input = input.toLowerCase()
	let books = document.getElementsByClassName("book-title")

	for (i = 0; i < books.length; i++) {
		if (!books[i].innerHTML.toLowerCase().includes(input)) {
			books[i].parentElement.style.display = "none"
		} else {
			books[i].parentElement.style.display = "block"
		}
	}
}
searchBar.addEventListener("change", () => {
	search_book()
})
