const CS_PREFIX = "jcarousel";
const CS_TRIGGER = `[data-replace='${CS_PREFIX}']`;

/**
 * Carousel Component
 * Transforms elements with `data-replace="jcarousel"` into scrollable carousels.
 * Supports multiple carousels on the same page.
 */
class Carousel {
    /**
     * Constructor to initialize the carousel instance.
     * @param {HTMLElement} element - The carousel container element.
     */
    constructor(element) {
        this.el = element; // The main carousel container
        this.carousel = null; // Scrollable content wrapper (created dynamically)
        this.leftArrow = null; // Left navigation button
        this.rightArrow = null; // Right navigation button
        this.cardWidth = 0; // Width of an individual card, including margin
        this.totalScrollWidth = 0; // Total scrollable width of the carousel
        this.visibleWidth = 0; // Visible width of the carousel
        this.documentStyle = getComputedStyle(document.documentElement);
    }

    checkId() {
        if (!this.el.hasAttribute("id") || this.el.id.length == 0) {
            this.el.id = `${CS_PREFIX}-${+(new Date())}-${Math.random().toString(36).substr(2, 5)}`;
        }
    }

    /**
     * Wraps the original content in a scrollable container and adds navigation buttons.
     */
    setupHTMLStructure() {
        // Save existing content
        const existingContent = Array.from(this.el.children);

        // Create the new scrollable structure
        const wrapper = document.createElement("div");
        wrapper.className = "jcarousel";
        wrapper.classList.add('h-full');
        existingContent.forEach((child) => wrapper.appendChild(child));
        this.el.innerHTML = ""; // Clear the original content
        this.el.appendChild(wrapper);

        // Add navigation buttons
        const leftButton = document.createElement("button");
        leftButton.className = "jcarousel-btn left";
        leftButton.textContent = "❮";
        leftButton.setAttribute("aria-label", "Scroll Left");

        const rightButton = document.createElement("button");
        rightButton.className = "jcarousel-btn right";
        rightButton.textContent = "❯";
        rightButton.setAttribute("aria-label", "Scroll Right");

        this.el.classList.add('jcarousel-container');
        this.el.classList.add('p-0');
        this.el.classList.add('m-2');
        this.el.classList.add('shadow-primary-box');
        this.el.style.width = `${this.el.offsetWidth * 0.99}px`;

        this.el.prepend(leftButton);
        this.el.appendChild(rightButton);

        // Store references to the new elements
        this.carousel = wrapper;
        this.leftArrow = leftButton;
        this.rightArrow = rightButton;
    }

    /**
     * Calculates and updates the dimensions of the carousel.
     */
    calculateDimensions() {
        this.cardWidth = this.carousel.firstElementChild.offsetWidth + 16; // Card width + margin
        this.totalScrollWidth = this.carousel.scrollWidth; // Total scrollable width
        this.visibleWidth = this.carousel.getBoundingClientRect().width; // Visible width of the container

        console.log("Dimensions Updated:", {
            cardWidth: this.cardWidth,
            totalScrollWidth: this.totalScrollWidth,
            visibleWidth: this.visibleWidth,
        });
    }

    /**
     * Updates the state of navigation arrows based on the scroll position.
     */
    updateArrows() {
        const scrollLeft = this.carousel.scrollLeft;
        const maxScrollLeft = this.totalScrollWidth - this.visibleWidth;

        this.leftArrow.disabled = scrollLeft <= 0;
        this.rightArrow.disabled = scrollLeft >= maxScrollLeft;

        console.log("Arrow State Updated:", {
            scrollLeft,
            maxScrollLeft,
            leftArrowDisabled: this.leftArrow.disabled,
            rightArrowDisabled: this.rightArrow.disabled,
        });
    }

    updateChildsWidth() {
        const col2Ref = document.getElementById(`${this.el.dataset.colSize}-ref-content`);
        const elem = this.el.querySelectorAll(`.${this.el.dataset.colSize}-ref`);

        const updateWidth = () => {
            const xlWidth = parseFloat(this.documentStyle.getPropertyValue('--xl'));
            const screenWidth = window.innerWidth;
            const colWidth = col2Ref ? col2Ref.offsetWidth : 0;
            elem.forEach((e) => {
                if (screenWidth >= xlWidth) {
                    e.style.width = `${colWidth}px`;
                } else {
                    e.style.width = `${this.minWidth}px`;
                }
            });
        };

        if (col2Ref) {
            const resizeObserver = new ResizeObserver(updateWidth);
            resizeObserver.observe(col2Ref);
        }

        updateWidth();
    }

    /**
     * Adds event listeners for carousel navigation and dynamic updates.
     */
    attachEventListeners() {
        this.leftArrow.addEventListener("click", () => {
            this.carousel.scrollBy({ left: -this.cardWidth, behavior: "smooth" });
        });

        this.rightArrow.addEventListener("click", () => {
            this.carousel.scrollBy({ left: this.cardWidth, behavior: "smooth" });
        });

        this.carousel.addEventListener("scroll", () => this.updateArrows());

        // Update dimensions and arrow visibility on resize
        const resizeObserver = new ResizeObserver(() => {
            this.calculateDimensions();
            this.updateArrows();
        });
        resizeObserver.observe(this.el);
    }

    /**
     * Initializes the carousel.
     */
    init() {
        this.checkId();
        this.setupHTMLStructure();
        this.calculateDimensions();
        this.updateArrows();
        this.updateChildsWidth();
        this.attachEventListeners();
    }
}

/**
 * Automatically initializes all carousels on the page.
 */
document.querySelectorAll(`[data-replace="jcarousel"]`).forEach((element) => {
    const carousel = new Carousel(element);
    carousel.init();
});
