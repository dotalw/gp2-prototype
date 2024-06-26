/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "../templates/**/*.html",
        "../templates/**/*.j2",
        "../*.py",
    ],

    plugins: [
        require('@tailwindcss/typography'),
        require('daisyui')
    ]
};
