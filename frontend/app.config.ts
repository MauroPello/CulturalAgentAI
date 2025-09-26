export default defineAppConfig({
  ui: {
    primary: "purple-heart",
    gray: "neutral",
    formGroup: {
      help: "mt-0 text-sm",
      error: "mt-0 text-sm",
    },
    notifications: {
      // Show toasts at the top right of the screen
      position: 'top-0 bottom-[unset]'
    },
    modal: {
      container: 'flex min-h-full items-center justify-center text-center p-4',
      base: 'text-lg',
      padding: 'p-6 sm:p-8',
      header: {
        padding: 'py-6 px-6 sm:px-8',
      },
      body: {
        padding: 'py-6 px-6 sm:px-8',
      },
      footer: {
        padding: 'py-6 px-6 sm:px-8',
      }
    },
    card: {
      body: {
        base: "h-full",
      },
      ring: "ring-0",
    }
  },
});
