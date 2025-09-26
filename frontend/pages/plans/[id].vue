<template>
  <div class="p-4">
    <div class="mb-4 flex justify-between">
      <UButton icon="i-heroicons-arrow-left" to="/my-plans" size="xl">
        Back to plans
      </UButton>
      <div class="flex gap-2">
        <UButton
          icon="i-heroicons-sparkles"
          size="xl"
          @click="handleRefine"
        >
          Refine Plan
        </UButton>
        <UButton
          color="red"
          icon="i-heroicons-trash"
          size="xl"
          @click="handleDelete"
        >
          Delete Plan
        </UButton>
      </div>
    </div>
    <div v-if="plan">
      <h1 class="text-3xl font-bold pb-4">
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

const { getPlanById, deletePlan } = usePlans();
const route = useRoute();
const router = useRouter();
const planId = route.params.id as string;
const plan = ref<Plan | undefined>(undefined);

onMounted(() => {
  plan.value = getPlanById(planId);
});

const handleDelete = () => {
  deletePlan(planId);
  router.push("/my-plans");
};

const handleRefine = () => {
  // TODO: Implement refine logic
};
</script>
