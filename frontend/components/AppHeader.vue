<script setup lang="ts">
import { companyName } from "~/constants/company";

const { isMinimumSm } = useScreenSize();
const route = useRoute();
</script>

<template>
  <div class="landing-page-navigator__container">
    <div
      class="flex flex-row items-center justify-center text-white bg-fuchsia-800 w-full py-0.5 cursor-pointer text-center"
      @click="async () => await navigateTo('/user-welcome')"
    >
      <div class="overflow-hidden w-full">
        <div class="marquee-wrapper">
          <span
            v-for="i in [0, 1, 2, 3, 4, 5]"
            :key="i"
            class="marquee-text"
          >
            Expand your business globally with AI! 🚀
          </span>
        </div>
      </div>
    </div>
    <div class="landing-page-navigator">
      <div class="landing-page-navigator__group pe-1">
        <NuxtLink
          class="landing-page-navigator__logo__link"
          :to="route.path === '/' ? '/' : '/user-welcome'"
        >
          <BaseLogo />
          <p>{{ companyName }}</p>
        </NuxtLink>
        <template v-if="route.path !== '/'">
          <UButton
            size="sm"
            class="hidden sm:block sm:text-lg text-gray-700 hover:text-black"
            variant="ghost"
            to="/library"
          >
            Library
          </UButton>
          <UButton
            size="sm"
            class="hidden sm:block sm:text-lg text-gray-700 hover:text-black"
            variant="ghost"
            to="/my-plans"
          >
            My Plans
          </UButton>
          <UButton
            size="sm"
            class="hidden sm:block sm:text-lg text-gray-700 hover:text-black"
            variant="ghost"
            to="/ai-chat"
          >
            AI Chat
          </UButton>
          <UButton
            size="sm"
            class="hidden sm:block sm:text-lg text-gray-700 hover:text-black"
            variant="ghost"
            to="/chat-review"
          >
            Review Chat
          </UButton>
        </template>
      </div>
      <ClientOnly>
        <div class="landing-page-navigator__group !gap-0">
          <UButton
            v-if="route.path === '/'"
            color="gray"
            variant="link"
            aria-label="Ask AI"
            trailing
            class="!gap-x-1 text-base"
            label="Ask AI"
            :size="isMinimumSm ? 'lg' : 'md'"
            to="/user-welcome"
          />
          <UButton
            :label="isMinimumSm ? 'Start Planning' : 'Start'"
            :size="isMinimumSm ? 'lg' : 'md'"
            class="text-base !bg-fuchsia-800"
            :to="route.path === '/' ? '/user-welcome' : '/new-plan'"
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
  padding-right: 15rem;
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
