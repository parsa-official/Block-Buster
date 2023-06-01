document.addEventListener("DOMContentLoaded", function() {
    // Get all delete icons
    var deleteIcons = document.querySelectorAll(".delete-icon");

    // Add click event listener to each delete icon
    deleteIcons.forEach(function(deleteIcon) {
        deleteIcon.addEventListener("click", function(event) {
            event.preventDefault();
            var movieId = this.getAttribute("data-movie-id");
            deleteMovie(movieId);
        });
    });

    // Function to handle movie deletion
    function deleteMovie(movieId) {
        // Add your delete movie logic here
        console.log('Deleting movie with ID:', movieId);
        // ...
    }
});
