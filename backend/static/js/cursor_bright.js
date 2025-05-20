let lastX = 0;
let lastY = 0;

document.addEventListener('mousemove', function(e) {
  const circle = document.querySelector('.cursor-circle');
  const mouseX = e.clientX;
  const mouseY = e.clientY;

  // Calcul de la vitesse de déplacement
  const deltaX = Math.abs(mouseX - lastX);
  const deltaY = Math.abs(mouseY - lastY);
  const speed = Math.sqrt(deltaX * deltaX + deltaY * deltaY); // Vitesse en fonction du mouvement

  // Ajuster la taille du cercle en fonction de la vitesse
  const newWidth = 30 + speed * 0.8;  // Plus la vitesse est élevée, plus le rond s'allonge
  const newHeight = 30 - speed * 0.2; // Plus la vitesse est élevée, plus il devient aplati

  circle.style.width = `${newWidth}px`;
  circle.style.height = `${Math.max(newHeight, 10)}px`; // Assurer un minimum de hauteur

  // Déplacer le rond aux coordonnées de la souris
  circle.style.left = mouseX + 'px';
  circle.style.top = mouseY + 'px';

  // Mise à jour des dernières positions
  lastX = mouseX;
  lastY = mouseY;
});

