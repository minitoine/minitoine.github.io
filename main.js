// @minitoine
// axantoine.com
// ax.antoine [at] gmail [dot] com

function onNavClick(activeNavItem) {

  const navbar = document.getElementById("navigation-bar");
  const navItems = navbar.getElementsByClassName("navigation-item");

  for (const item of navItems) {
    item.classList.remove("active");
  }

  activeNavItem.classList.add("active");

  const target_id = activeNavItem.getAttribute("href").replace("#","");
  const target = document.getElementById(target_id);

  scrollToSmoothly(target.offsetTop - navbar.clientHeight, 500);
}

/**
 *
 * From : https://stackoverflow.com/questions/51229742/javascript-window-scroll-behavior-smooth-not-working-in-safari
 */
function scrollToSmoothly(pos, time) {

    const content = window.pageYOffset;
    const currentPos = window.pageYOffset;

    let start = null;
    if(time == null) time = 500;
    pos = +pos, time = +time;
    window.requestAnimationFrame(function step(currentTime) {
        start = start ?? currentTime;
        const progress = currentTime - start;
        if (currentPos < pos) {
            window.scrollTo(0, ((pos - currentPos) * progress / time) + currentPos);
        } else {
            window.scrollTo(0, currentPos - ((currentPos - pos) * progress / time));
        }
        if (progress < time) {
            window.requestAnimationFrame(step);
        } else {
            window.scrollTo(0, pos);
        }
    });
}

// Setup masonry grids if any present of the document
// Allows for dynamic grids of cards in js
const masonries = []
const grids = document.getElementsByClassName('masonry-grid');
for (const grid of grids) {

    const masonry = new Masonry(grid, {
        percentProsition:true,
        transitionDuration: '0.2s',
    });

    masonries.push(masonry);

    const layout = () => {
        masonry.layout();
    }

    // Update the layout of the current grid for each details element is toggled
    // as its height can change
    const detailsElements = grid.getElementsByTagName('details')

    for (const detailsElement of detailsElements) {
        detailsElement.ontoggle = () => {
            layout();
        }
    }
}

// Update layout (slowly with debounce) when window is resized
window.addEventListener('resize', debounce(() => {
    for (const masonry of masonries) {
        masonry.layout();
    }
}), 100);

/**
 * From: http://www.kevinsubileau.fr/informatique/boite-a-code/php-html-css/javascript-debounce-throttle-reduire-appels-fonction.html
 *
 * Retourne une fonction qui, tant qu'elle continue à être invoquée,
 * ne sera pas exécutée. La fonction ne sera exécutée que lorsque
 * l'on cessera de l'appeler pendant plus de N millisecondes.
 * Si le paramètre `immediate` vaut vrai, alors la fonction
 * sera exécutée au premier appel au lieu du dernier.
 * Paramètres :
 *  - func : la fonction à `debouncer`
 *  - wait : le nombre de millisecondes (N) à attendre avant
 *           d'appeler func()
 *  - immediate (optionnel) : Appeler func() à la première invocation
 *                            au lieu de la dernière (Faux par défaut)
 *  - context (optionnel) : le contexte dans lequel appeler func()
 *                          (this par défaut)
 */
function debounce(func, wait, immediate, context) {
    var result;
    var timeout = null;
    return function() {
        var ctx = context || this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) result = func.apply(ctx, args);
        };
        var callNow = immediate && !timeout;
        // Tant que la fonction est appelée, on reset le timeout.
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) result = func.apply(ctx, args);
        return result;
    };
}

/**
 * From: http://www.kevinsubileau.fr/informatique/boite-a-code/php-html-css/javascript-debounce-throttle-reduire-appels-fonction.html
 *
 * Retourne une fonction qui, tant qu'elle est appelée,
 * n'est exécutée au plus qu'une fois toutes les N millisecondes.
 * Paramètres :
 *  - func : la fonction à contrôler
 *  - wait : le nombre de millisecondes (période N) à attendre avant
 *           de pouvoir exécuter à nouveau la function func()
 *  - leading (optionnel) : Appeler également func() à la première
 *                          invocation (Faux par défaut)
 *  - trailing (optionnel) : Appeler également func() à la dernière
 *                           invocation (Faux par défaut)
 *  - context (optionnel) : le contexte dans lequel appeler func()
 *                          (this par défaut)
 */
function throttle(func, wait, leading, trailing, context) {
    var ctx, args, result;
    var timeout = null;
    var previous = 0;
    var later = function() {
        previous = new Date;
        timeout = null;
        result = func.apply(ctx, args);
    };
    return function() {
        var now = new Date;
        if (!previous && !leading) previous = now;
        var remaining = wait - (now - previous);
        ctx = context || this;
        args = arguments;
        // Si la période d'attente est écoulée
        if (remaining <= 0) {
            // Réinitialiser les compteurs
            clearTimeout(timeout);
            timeout = null;
            // Enregistrer le moment du dernier appel
            previous = now;
            // Appeler la fonction
            result = func.apply(ctx, args);
        } else if (!timeout && trailing) {
            // Sinon on s’endort pendant le temps restant
            timeout = setTimeout(later, remaining);
        }
        return result;
    };
};
