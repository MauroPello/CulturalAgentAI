import { companyLogo, companyName, companyUrl } from "./constants/company";
import robotsConfig from "./robots.config";
import viewportConfig from "./viewport.config";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  modules: [
    "@nuxt/image",
    "@nuxtjs/robots",
    ["nuxt-viewport", viewportConfig],
    '@nuxt/ui',
    "@nuxt/eslint",
    "@nuxtjs/color-mode",
  ],
  components: ["~/components"],
  robots: robotsConfig,
  site: {
    name: companyName,
    url: companyUrl,
    logo: companyLogo,
  },
  colorMode: {
    preference: "light",
    fallback: "light",
  },
  sourcemap: {
    client: "hidden",
  },
  css: ["~/assets/css/tailwind.css", "~/assets/css/main.scss"],
  postcss: {
    plugins: {
      "tailwindcss/nesting": {},
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  tailwindcss: {
    viewer: false,
  },
  // nitro: {
  //   preset: 'cloudflare-pages',
  // },
  app: {
    head: {
      htmlAttrs: {
        lang: "en",
      },
      meta: [
        { charset: "utf-8" },
        {
          name: "viewport",
          content:
            "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover",
        },
      ],
    },
  },
})