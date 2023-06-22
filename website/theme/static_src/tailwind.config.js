/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
      extend: {
        colors: {
          gray: {
            "100": "#fffefe",
            "200": "#fcfcfc",
            "300": "#1e1f20",
            "400": "#201919",
            "500": "#0a0303",
            "600": "rgba(0, 0, 0, 0.8)",
          },
          white: "#fff",
          silver: "#bdbfc7",
          darkslateblue: "#243465",
          lightsteelblue: "#cad5f5",
          ghostwhite: "#f6f9ff",
          black: "#000",
          whitesmoke: "#eee",
          limegreen: "#3dd34c",
          mediumslateblue: "#6d62f7",
          darkslategray: "#4b4b4b",
          royalblue: "#2280ff",
        },
        fontFamily: {
          "open-sans": "'Open Sans'",
          "nunito-sans": "'Nunito Sans'",
          inter: "Inter",
          aladin: "Aladin",
        },
        borderRadius: {
          "smi-5": "12.5px",
          "8xs": "5px",
        },
      },
      fontSize: {
        xs: "12px",
        lg: "18px",
        sm: "14px",
        "3xs": "10px",
        smi: "13px",
        "2xs": "11px",
      },
      screens: {
        sm: {
          max: "420px",
        },
      },
    },

    
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}

