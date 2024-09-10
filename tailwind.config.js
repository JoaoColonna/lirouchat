/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './chatbot/templates/**/*.html',
    './chatbot/static/chatbot/js/**/*.js'
    // Adicione mais caminhos se necessário
  ],
    theme: {
    extend: {
      fontFamily: {
        title: ['Inter', 'sans-serif'],
        subtitle: ['Inter', 'sans-serif'],
        body: ['Aptos', 'sans-serif'],
      },
      colors: {
        primary: '#cca9dd',          // Cor principal
        complementary: '#bbd4b2',    // Cor complementar
        analogous1: '#9caaea',       // Cor análoga 1
        analogous2: '#e5a1c4',       // Cor análoga 2
        divide: '#d5d4b1',           // Cor dividida
        'gray-light': '#f7f7f7',     // Branco acinzentado para o fundo
        'gray-100': '#e5e5e5',       // Cinza claro
        'gray-200': '#cccccc',       // Cinza médio
        'gray-300': '#999999',       // Cinza escuro
        'gray-dark': '#666666',      // Cinza mais escuro
        'white': '#ffffff',          // Branco puro
        'black': '#000000',          // Preto
      },
    },
  },

  plugins: [],
}
