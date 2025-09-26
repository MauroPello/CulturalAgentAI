<template>
  <div class="p-4">
    <NuxtLink class="mb-4 text-blue-500" to="/my-plans">
      &larr; Back to plans
    </NuxtLink>
    <div v-if="plan">
      <h1 class="text-2xl font-bold">
        {{ plan.project_name }}
      </h1>
      <ClientOnly>
        <GanttChart :plan="plan" />
      </ClientOnly>
    </div>
    <div v-else>
      <p>Plan not found.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePlans } from "~/composables/usePlans";
import type { Plan } from "~/types/plan";

const { getPlanById } = usePlans();
const route = useRoute();
const planId = route.params.id as string;
const plan = ref<Plan | undefined>(undefined);

onMounted(() => {
  plan.value = getPlanById(planId);
});
</script>
