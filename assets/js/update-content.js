// assets/js/update-content.js

document.addEventListener("DOMContentLoaded", () => {
    const contentDiv = document.querySelector(".content");
    const buttons = document.querySelectorAll("button[data-page], .lesson-link");

    const loadContent = async (path) => {
        try {
            const response = await fetch(path);
            if (!response.ok) {
                throw new Error("Content not found");
            }
            const content = await response.text();
            contentDiv.innerHTML = content;
        } catch (error) {
            contentDiv.innerHTML = `<p>Error Loading Content: ${error.message}</p>`;
        }
    };

    buttons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const page = button.dataset.page || `lessons/${button.dataset.lesson}`;
            loadContent(`${page}.html`);

            // Temporarily disable hover effect
            const parentLi = button.closest("li");
            if (parentLi) {
                parentLi.classList.add("disable-hover");
                setTimeout(() => {
                    parentLi.classList.remove("disable-hover");
                }, 1000); // Adjust timeout to match the transition duration
            }
        });
    });
});
