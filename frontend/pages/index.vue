<template>
  <div class="space-y-16 md:space-y-24">
    <!-- Hero Section -->
    <UContainer class="py-16 md:py-24 text-center">
      <h1
        class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-4"
      >
        Expand Your Business Globally, Intelligently
      </h1>
      <p
        class="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8"
      >
        Navigate foreign markets with confidence. Our AI assistant, powered by the culturally-aware Apertus LLM, helps you build actionable expansion plans, from initial strategy to an interactive Gantt chart.
      </p>
      <div class="flex flex-col sm:flex-row justify-center items-center gap-4">
        <UButton
          size="xl"
          icon="i-heroicons-rocket-launch-20-solid"
          label="Start Your Expansion Plan"
          aria-label="Start Your Expansion Plan"
          trailing
          to="/user-welcome"
        />
        <UButton
          to="/#features"
          size="xl"
          label="Learn More"
          variant="link"
          color="gray"
          icon="i-heroicons-arrow-down-circle"
          trailing
        />
      </div>
    </UContainer>

    <!-- How it Works Section -->
    <UContainer>
      <div class="max-w-4xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-12">
          From Vision to Action in Three Steps
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          <div class="text-center space-y-3 p-4 rounded-lg">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full mb-4 ring-8 ring-primary-50 dark:ring-primary-950"
            >
              <UIcon name="i-heroicons-chat-bubble-left-right-solid" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold">1. Discuss Your Vision</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Chat with our AI to define your goals. Upload company documents to give the AI context about your business for a tailored strategy.
            </p>
          </div>
          <div class="text-center space-y-3 p-4 rounded-lg">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full mb-4 ring-8 ring-primary-50 dark:ring-primary-950"
            >
              <UIcon name="i-heroicons-document-chart-bar-solid" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold">2. Generate Your Strategy</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Receive a comprehensive plan and an interactive Gantt chart, visualizing milestones and timelines for your market entry.
            </p>
          </div>
          <div class="text-center space-y-3 p-4 rounded-lg">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full mb-4 ring-8 ring-primary-50 dark:ring-primary-950"
            >
              <UIcon name="i-heroicons-pencil-square-solid" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold">3. Refine & Execute</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Review, expand, and ask questions about your plan. Iterate on the strategy until it's perfect, then export it to guide your team.
            </p>
          </div>
        </div>
      </div>
    </UContainer>

    <!-- Feature/Benefit Section -->
    <UContainer id="features" class="py-16">
      <div class="grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h2 class="text-3xl md:text-4xl font-bold mb-4">
            Powered by Apertus: Secure, Transparent & Culturally Fluent
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-300 mb-6">
            Our platform is built on Apertus, the only LLM that combines enterprise-grade security with a deep understanding of global cultures. All training data was 100% legally obtained.
          </p>
          <ul class="space-y-3 text-gray-700 dark:text-gray-200">
            <li class="flex items-center gap-3">
              <UIcon
                name="i-heroicons-lock-closed-solid"
                class="w-6 h-6 text-primary-500"
              />
              <span><span class="font-semibold">Open & Secure:</span> Host it yourself. Your data stays yours, thanks to an open-source model designed for privacy.</span>
            </li>
            <li class="flex items-center gap-3">
              <UIcon
                name="i-heroicons-globe-alt-solid"
                class="w-6 h-6 text-primary-500"
              />
              <span><span class="font-semibold">Cultural Nuance:</span> Leverage an AI trained on every language, providing insights that respect local customs and business etiquette.</span>
            </li>
            <li class="flex items-center gap-3">
              <UIcon
                name="i-heroicons-check-badge-solid"
                class="w-6 h-6 text-primary-500"
              />
              <span><span class="font-semibold">Transparent & Ethical:</span> Work with a transparent, open-weight LLM built on a foundation of legally sourced data.</span>
            </li>
          </ul>
        </div>
        <div class="p-4">
          <BaseLogo class="w-full h-auto max-w-sm mx-auto" />
          <p class="text-center text-gray-500 dark:text-gray-400 mt-4">The open-source, culturally-aware LLM for global business.</p>
        </div>
      </div>
    </UContainer>

    <!-- Final Call to Action -->
    <UContainer class="pb-16 text-center">
      <h2 class="text-3xl md:text-4xl font-bold mb-4">
        Ready to Conquer New Markets?
      </h2>
      <p class="text-lg text-gray-600 dark:text-gray-300 max-w-xl mx-auto mb-8">
        For small businesses dreaming big or consultants seeking an edge. Start building your global expansion strategy today.
      </p>
      <UButton
        to="/user-welcome"
        size="xl"
        icon="i-heroicons-sparkles-20-solid"
        label="Start Planning for Free"
        aria-label="Start Planning for Free"
        trailing
      />
    </UContainer>
  </div>
</template>

<script lang="ts" setup>
</script>
