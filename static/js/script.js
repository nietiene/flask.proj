function updateName() {
    const input = document.getElementById("nameInput").value;
    const span = document.getElementById("username")

    if (input.trim() === "") {
        alert("Please enter a name.")
        return;
    }

    span.textContent = input;
}