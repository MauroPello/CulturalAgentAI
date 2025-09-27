<template>
  <div class="p-4 xl:md-32 lg:px-24 md:px-16 px-8">
    <div class="mb-4 flex justify-between">
      <UButton icon="i-heroicons-arrow-left" to="/my-plans" size="lg" color="white">
        Back to plans
      </UButton>
      <div class="flex gap-2">
        <UButton
          icon="i-heroicons-sparkles"
          size="lg"
          @click="handleRefine"
        >
          Refine Plan
        </UButton>
        <UButton
          color="red"
          icon="i-heroicons-trash"
          size="lg"
          @click="handleDelete"
        >
          Delete Plan
        </UButton>
      </div>
    </div>
    <div v-if="plan">
      <h1 class="text-3xl font-bold pb-4 pt-3">
        {{ plan.project_name }}
      </h1>
      <p class="mb-4 text-lg text-gray-500 dark:text-gray-400">
        {{ plan.project_description }}
      </p>
      <ClientOnly>
        <GanttChart :plan="plan" />
      </ClientOnly>
    </div>
    <div v-else>
      <p>Plan not found.</p>
    </div>

    <UModal v-model="isModalOpen">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold">
            Confirm Deletion
          </h2>
        </template>

        <p>Are you sure you want to delete this plan?</p>

        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton color="gray" size="xl" @click="isModalOpen = false">
              Cancel
            </UButton>
            <UButton color="red" size="xl" @click="confirmDelete">
              Delete
            </UButton>
          </div>
        </template>
      </UCard>
    </UModal>

    <UModal v-model="isRefineModalOpen">
      <UCard>
        <template #header>
          <h2 class="text-xl font-bold">
            Refine Plan
          </h2>
        </template>

        <p class="mb-4 text-base text-gray-600">Describe the changes you'd like to make to your plan. The AI will update the Gantt chart based on your prompt.</p>
        <UTextarea v-model="refinePrompt" :rows="12" :disabled="isRefining" placeholder="e.g., 'Add a new task called Design Mockups after the Research phase and before the Development phase. It should take 5 days.'" />

        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton color="gray" size="xl" :disabled="isRefining" @click="isRefineModalOpen = false">
              Cancel
            </UButton>
            <UButton size="xl" :loading="isRefining" @click="confirmRefine">
              Refine Plan
            </UButton>
          </div>
        </template>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import { usePlans } from "~/composables/usePlans";
import type { Plan } from "~/types/plan";

const { getPlanById, deletePlan, updatePlan } = usePlans();
const route = useRoute();
const router = useRouter();
const planId = route.params.id as string;
const plan = ref<Plan | undefined>(undefined);
const isModalOpen = ref(false);
const isRefineModalOpen = ref(false);
const refinePrompt = ref('');
const isRefining = ref(false);

onMounted(() => {
  plan.value = getPlanById(planId);

  // If plan is not found immediately, try again after a short delay
  // This handles cases where localStorage might need a moment to sync
  if (!plan.value) {
    setTimeout(() => {
      plan.value = getPlanById(planId);
    }, 100);
  }
});

const handleDelete = () => {
  isModalOpen.value = true;
};

const confirmDelete = () => {
  deletePlan(planId);
  router.push("/my-plans");
};

const handleRefine = () => {
  isRefineModalOpen.value = true;
};

const confirmRefine = async () => {
  if (!plan.value || !refinePrompt.value.trim()) {
    return;
  }

  try {
    isRefining.value = true;
    const response = await fetch('http://localhost:8000/modify_gantt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        gantt_plan: plan.value,
        prompt: refinePrompt.value,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to refine plan');
    }

    const result = await response.json();

    if (result.success && result.gantt_plan) {
      // The backend returns a complete, updated plan object.
      // We need to preserve the top-level ID from the original plan.
      const updatedPlanData: Plan = {
        ...result.gantt_plan,
        id: plan.value.id, // Preserve the original plan ID
      };

      updatePlan(planId, updatedPlanData);
      plan.value = updatedPlanData; // Refresh the local state
      isRefineModalOpen.value = false;
      refinePrompt.value = '';
    } else {
      console.error("Error refining plan:", result.error);
      // Optionally, show a toast or notification to the user
    }
  } catch (error) {
    console.error("An error occurred during plan refinement:", error);
    // Optionally, show a toast or notification to the user
  } finally {
    isRefining.value = false;
  }
};
</script>
