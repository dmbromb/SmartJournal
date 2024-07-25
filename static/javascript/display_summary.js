document.addEventListener("DOMContentLoaded", function() {
    const dates = document.querySelectorAll("td a");

    dates.forEach(date => {
        date.addEventListener("mouseover", function(event) {
            const summary = event.target.getAttribute("data-summary") || "No summary available";
            const popup = document.createElement("div");
            popup.textContent = summary;
            popup.style.position = "absolute";
            popup.style.backgroundColor = "white";
            popup.style.border = "1px solid black";
            popup.style.padding = "5px";
            popup.style.borderRadius = "5px";
            popup.style.boxShadow = "0 0 10px rgba(0,0,0,0.1)";
            popup.style.zIndex = 1000;

            document.body.appendChild(popup);

            const rect = event.target.getBoundingClientRect();
            popup.style.left = `${rect.left + window.scrollX}px`;
            popup.style.top = `${rect.bottom + window.scrollY}px`;

            event.target.addEventListener("mouseout", function() {
                popup.remove();
            }, { once: true });
        });
    });
});
