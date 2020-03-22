(() => {

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#blinking-cursor').animate(
        [
            { opacity: 0, offset: 0 },
            { opacity: 1, offset: 0.25 },
            { opacity: 0, offset: 0.5 },

            // Cutting off the blink opacity early makes it look a bit nicer.
            { opacity: 0, offset: 1 }],
        {
            duration: 2000,
            iterations: Infinity
        }
    );

    document.querySelector('.logo').addEventListener('click', () => {
        window.location = '/';
    });
});

})();
