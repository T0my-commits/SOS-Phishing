// Example:
//
//<body>
//    <div class="container">
//        <!-- Menu des titres des sections -->
//        <nav class="sidebar">
//            <ul>
//                <li><a href="#section1" class="menu-item">Section 1</a></li>
//                <li><a href="#section2" class="menu-item">Section 2</a></li>
//            </ul>
//        </nav>
//
//        <!-- Contenu des sections -->
//        <div class="main-content">
//            <section id="section1">
//                <h2>Section 1</h2>
//                <p>Contenu de la section 1.</p>
//            </section>
//
//            <section id="section2">
//                <h2>Section 2</h2>
//                <p>Contenu de la section 2.</p>
//            </section>
//        </div>
//    </div>
//
//    <script src="script.js"></script>
//</body>
//</html>


//window.addEventListener('scroll', function() {
//    const sections = document.querySelectorAll('.main-content section');
//    const menuItems = document.querySelectorAll('.menu-item');
//
//    let currentSectionId = '';
//
//    sections.forEach(section => {
//        const sectionTop = section.offsetTop - 250; // Pour ajuster légèrement le décalage
//        if (pageYOffset >= sectionTop) {
//            currentSectionId = section.getAttribute('id');
//        }
//    });
//
//    menuItems.forEach(item => {
//        item.classList.remove('active');
//        if (item.getAttribute('href').substring(1) === currentSectionId) {
//            item.classList.add('active');
//        }
//    });
//});

window.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.main-content section');
    const sections_menu = document.getElementById('summary-sections');

    // Créer dynamiquement les items de menu en fonction des sections
    sections.forEach(section => {
        const sectionId = section.getAttribute('id');
        const sectionTitle = section.querySelector('h2').textContent;

        // Créer l'élément <li> et le lien <a>
        const listItem = document.createElement('li');
        const linkItem = document.createElement('a');
        linkItem.classList.add('menu-item');
        linkItem.setAttribute('href', `#${sectionId}`);
        linkItem.textContent = sectionTitle;

        // Ajouter le lien dans la liste
        listItem.appendChild(linkItem);
        sections_menu.appendChild(listItem);
    });
});

window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('.main-content section');
    const menuItems = document.querySelectorAll('.menu-item');

    let currentSectionId = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 250;
        if (pageYOffset >= sectionTop) {
            currentSectionId = section.getAttribute('id');
        }
    });

    menuItems.forEach(item => {
        item.classList.remove('active');
        //item.classList.remove('bi');
        //item.classList.remove('bi-arrow-right-short');
        if (item.getAttribute('href').substring(1) === currentSectionId) {
            item.classList.add('active');
            //item.classList.add('bi');
            //item.classList.add('bi-arrow-right-short');
        }
    });
});

