const navItems = document.querySelectorAll(".nav-item");
const sections = document.querySelectorAll(".dashboard-section");
const pageTitle = document.getElementById("page-title");
const sectionLinks = document.querySelectorAll("[data-section-link]");

const pageTitles = {
    overview: "Audience Overview",
    segments: "Audience Segments",
    analyzer: "Viewer Analyzer",
    recommendations: "Recommendations",
    insights: "Audience Insights",
    simulator: "What-If Simulator"
};


function showSection(sectionId) {

    sections.forEach(section => {
        section.classList.remove("active-section");
    });

    const selectedSection = document.getElementById(sectionId);

    if (selectedSection) {
        selectedSection.classList.add("active-section");
    }

    navItems.forEach(item => {
        item.classList.remove("active");

        if (item.dataset.section === sectionId) {
            item.classList.add("active");
        }
    });

    pageTitle.textContent =
        pageTitles[sectionId] || "WatchWise AI";
}


navItems.forEach(item => {

    item.addEventListener("click", () => {

        const sectionId = item.dataset.section;

        showSection(sectionId);

    });

});


sectionLinks.forEach(link => {

    link.addEventListener("click", () => {

        const sectionId = link.dataset.sectionLink;

        showSection(sectionId);

    });

});