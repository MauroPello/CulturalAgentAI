<template>
  <div class="flex flex-col min-h-screen">
    <NuxtLoadingIndicator color="rgb(var(--color-primary-600))" />
    <main class="flex-grow">
    <NuxtLayout>
      <NuxtErrorBoundary>
        <NuxtPage />

        <template #error="{ error }">
          <VueError :error="error" />
        </template>
      </NuxtErrorBoundary>
    </NuxtLayout>
    </main>
    <UNotifications />
  </div>
</template>
