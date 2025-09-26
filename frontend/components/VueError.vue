<script setup lang="ts">
const props = defineProps<{ error: unknown }>();
const { error } = toRefs(props);

const isPageNotFound = computed(
  () =>
    error.value instanceof Object &&
    "message" in error.value &&
    String(error.value.message).includes("Page not found"),
);
</script>

<template>
  <div class="error-page">
    <h1 class="error-page__title">Fatal Error!</h1>
    <p class="w-[90%] text-lg bg-slate-200 rounded-lg p-4">
      {{ isPageNotFound ? "Page not Found" : error }}
    </p>
    <div class="flex flex-row gap-4">
      <UButton
        size="xl"
        class="text-lg"
        @click="$router.go(0)"
      >
        Refresh the page
      </UButton>
      <UButton
        size="xl"
        class="text-lg"
        @click="
          async () => {
            await $router.push('/');
            $router.go(0);
          }
        "
      >
        Go back to home
      </UButton>
    </div>
  </div>
</template>

<style lang="postcss" scoped>
.error-page {
  @apply w-full py-10 gap-7 flex flex-col items-center justify-center;

  &__title {
    @apply text-3xl font-medium;
  }
}
</style>
