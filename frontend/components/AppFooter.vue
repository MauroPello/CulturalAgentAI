<script setup lang="ts">
import { companyName } from "~/constants/company";
</script>

<template>
  <div class="landing-page-footer">
    <NuxtLink
      class="landing-page-footer__logo__link"
      to="/"
    >
      <BaseLogo />
      <p>{{ companyName }}</p>
    </NuxtLink>
  </div>
</template>

<style lang="postcss" scoped>
.landing-page-footer {
  @apply flex flex-col items-center justify-center gap-2 bg-primary-300 px-4 py-8 mt-10;

  &__logo__link {
    @apply flex items-center gap-2;
    @apply text-2xl;
    font-weight: 500;
  }
}
</style>
