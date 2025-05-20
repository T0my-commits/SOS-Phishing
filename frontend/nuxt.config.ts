// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // runtimeConfig: {
  //   public: {
  //     apiBase: process.env.NUXT_API_URL || 'http://localhost:8000',
  //     apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/',
  //   }
  // },

  runtimeConfig: {
    apiKey: '', // Default to an empty string, automatically set at runtime using process.env.NUXT_API_KEY
    public: {
      apiBaseUrl: process.env.BASE_API_URL, // Exposed to the frontend as well.
      debug: true,
    }
  },

  devtools: { enabled: true },
  modules: [
    '@nuxt/image',
    'nuxt-primevue',
  ],

  primevue: {
    usePrimeVue: true,
    components: {
      exclude: []
    }
      /* Options */
  },

  // publicRuntimeConfig: {
  //   apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/', // URL de ton API
  // },

  css: [
    'primevue/resources/themes/aura-light-green/theme.css',
    'primevue/resources/primevue.min.css',
    "primeicons/primeicons.css",
    '/node_modules/primeflex/primeflex.css',
    '@/assets/css/codemirror.min.css',
    '@/assets/css/monokai.min.css',
    '@/assets/css/main.css',
    '@/assets/css/custom_sidenav.css',
    '@/assets/css/custom_header.css',
    '@/assets/css/custom_components.css',
    '@/assets/css/custom_tabview.css',
    '@/assets/css/custom_text.css',
    '@/assets/css/dashboard.css',
    '@/assets/css/icons/bootstrap-icons.css',
    '@/assets/css/custom_transitions.css',
  ],

  ui: {
    colorMode: false
  },

  compatibilityDate: '2025-04-03',
})
