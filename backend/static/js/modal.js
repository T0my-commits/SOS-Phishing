class Modal {
    constructor(selector, config = {}) {
        this.modal = document.querySelector(selector);
        if (!this.modal) {
            throw new Error(`Modal with selector ${selector} not found.`);
        }

        // Configuration par défaut
        this.config = {
            type: 'card-center', // 'card-center', 'side-left', 'side-right'
            triggers: [],
            options: ['close-x'], // 'close-x', 'close-btn', 'ok-btn'
            ...config,
        };

        this.init();
    }

    // Initialiser la modale
    init() {
        // Ajouter les classes selon le type
        this.modal.classList.add('hidden', this.config.type);

        // Ajouter les options (boutons, etc.)
        this.createOptions();

        // Attacher les événements aux triggers
        this.addTriggers();

        // Fermer la modale en cliquant en dehors
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close();
        });
    }

    // Ajouter des boutons d'options
    createOptions() {
        const modalContent = this.modal.querySelector('.modal');
        if (!modalContent) {
            throw new Error('Modal content element (.modal) not found inside modal overlay.');
        }

        if (this.config.options.includes('close-x')) {
            const closeX = document.createElement('span');
            closeX.textContent = '×';
            closeX.classList.add('close-x');
            closeX.classList.add('btn', 'btn-primary');
            closeX.addEventListener('click', () => this.close());
            modalContent.prepend(closeX);
        }

        if (this.config.options.includes('close-btn')) {
            const closeBtn = document.createElement('button');
            closeBtn.textContent = 'Close';
            closeBtn.classList.add('close-btn');
            closeBtn.classList.add('btn', 'btn-primary');
            closeBtn.addEventListener('click', () => this.close());
            modalContent.appendChild(closeBtn);
        }

        if (this.config.options.includes('ok-btn')) {
            const okBtn = document.createElement('button');
            okBtn.textContent = 'OK';
            okBtn.classList.add('ok-btn');
            okBtn.classList.add('btn', 'btn-primary');
            okBtn.addEventListener('click', () => {
                this.close();
                console.log('OK button clicked');
            });
            modalContent.appendChild(okBtn);
        }
    }

    // Ajouter des triggers
    addTriggers() {
        this.config.triggers.forEach((triggerSelector) => {
            const trigger = document.querySelector(triggerSelector);
            if (trigger) {
                trigger.addEventListener('click', () => this.open());
            } else {
                console.warn(`Trigger with selector ${triggerSelector} not found.`);
            }
        });
    }

    // Ouvrir la modale
    open() {
        this.modal.classList.remove('hidden');
    }

    // Fermer la modale
    close() {
        this.modal.classList.add('hidden');
    }
}

// Utilisation
// new Modal('#modalOverlay', {
//     type: 'card-center', // card-center, side-left, side-right
//     triggers: ['#openModal'], // Boutons ou éléments déclencheurs
//     options: ['close-x', 'close-btn', 'ok-btn'], // Boutons ajoutés
// });
