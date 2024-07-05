document.addEventListener("DOMContentLoaded", function() {
    setTimeout(showMainPage, 3000);

    window.addEventListener('popstate', function(event) {
        if (event.state) {
            document.getElementById("welcome-page").classList.toggle("hidden", !event.state.showWelcomePage);
            document.getElementById("main-page").classList.toggle("hidden", event.state.showWelcomePage);
        }
    });

    document.getElementById('main-page').addEventListener('click', function() {
        history.pushState({ showWelcomePage: false }, 'Main Page', 'index.html');
    });
});

function showMainPage() {
    document.getElementById("welcome-page").classList.add("hidden");
    document.getElementById("main-page").classList.remove("hidden");
    history.pushState({ showWelcomePage: false }, 'Main Page', 'index.html');
}

function navigateTo(page) {
    window.location.href = page;
}
