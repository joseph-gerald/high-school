tailwind.config = {
    content: ["*"],
    theme: {
        extend: {
            fontFamily: {
                'sometype': ['"Sometype Mono"'],
                'merriweather': ['Merriweather', 'serif'],
                'jakarta': ['"Plus Jakarta Sans"', 'sans-serif'],
            },
            colors: {
                'text': '#dcdcdc',
                'background': '#030303',
                'highlight': '#161616',
                'border': '#2f2f2f',
            },
        }
    }
}
