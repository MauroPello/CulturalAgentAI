<script setup lang="ts">
import { companyName } from "~/constants/company";

const { isMinimumSm, width } = useScreenSize();
</script>

<template>
  <div class="landing-page-navigator__container">
    <div
      class="flex flex-row items-center justify-center text-white bg-primary-500 w-full py-0.5 cursor-pointer text-center"
      @click="async () => await navigateTo('/#find-meal')"
    >
      <div class="overflow-hidden w-full">
        <div class="marquee-wrapper">
          <span
            v-for="i in [0, 1, 2, 3, 4, 5]"
            :key="i"
            class="marquee-text"
          >
            {{ companyName }} is free! Try it out now! 🚀
          </span>
        </div>
      </div>
    </div>
    <div class="landing-page-navigator">
      <div class="landing-page-navigator__group pe-1">
        <NuxtLink
          class="landing-page-navigator__logo__link"
          to="/"
        >
          <BaseLogo
            :small="true"
          />
          <p>{{ companyName }}</p>
        </NuxtLink>
        <UButton
          size="sm"
          class="hidden sm:block sm:text-lg text-gray-700 hover:text-black"
          variant="ghost"
          to="/upload"
        >
          Upload
        </UButton>
        <UButton
          size="sm"
          class="hidden sm:block sm:text-lg text-gray-700 hover:text-black"
          variant="ghost"
          to="/chat-review"
        >
          Review Chat
        </UButton>
      </div>
      <ClientOnly>
        <div class="landing-page-navigator__group !gap-0">
          <UButton
            icon="i-heroicons-clock"
            color="gray"
            variant="link"
            aria-label="History"
            trailing
            class="!gap-x-1"
            :label="width > 450 ? 'History' : ''"
            :size="isMinimumSm ? 'lg' : 'sm'"
          />
          <UButton
            :label="isMinimumSm ? 'Find a Meal' : 'Try it!'"
            :size="isMinimumSm ? 'lg' : 'md'"
            class="sm:text-lg"
          />
        </div>
      </ClientOnly>
    </div>
  </div>
</template>

<style lang="postcss" scoped>
.landing-page-navigator {
  @apply flex items-center justify-between h-20 bg-primary-100 px-3 sm:px-4 md:px-6;

  &__container {
    @apply fixed top-0 left-0 right-0 z-50;
  }

  &__group {
    @apply flex items-center gap-1 sm:gap-2 md:gap-4 lg:gap-6;
  }

  &__link {
    @apply text-xl font-medium text-slate-500;
  }

  &__link:hover {
    @apply text-slate-700;
  }

  &__logo__link {
    @apply flex items-center gap-2;
    @apply text-xl sm:text-2xl;
    font-weight: 500;
  }
}

.marquee-text {
  display: inline-block;
  padding-left: 1rem;
  padding-right: 10rem;
}

.marquee-wrapper {
  display: inline-flex;
  white-space: nowrap;
  animation: marquee 15s linear infinite;
  animation-delay: 0.5s;
}

@keyframes marquee {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}
</style>
