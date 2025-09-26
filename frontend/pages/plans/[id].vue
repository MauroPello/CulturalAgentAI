<template>
  <div class="p-4">
    <div class="mb-4 flex justify-between">
      <UButton icon="i-heroicons-arrow-left" to="/my-plans" size="lg">
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
      <h1 class="text-3xl font-bold pb-4">
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
            <UButton color="gray" @click="isModalOpen = false">
              Cancel
            </UButton>
            <UButton color="red" @click="confirmDelete">
              Delete
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

const { getPlanById, deletePlan } = usePlans();
const route = useRoute();
const router = useRouter();
const planId = route.params.id as string;
const plan = ref<Plan | undefined>(undefined);
const isModalOpen = ref(false);

onMounted(() => {
  plan.value = getPlanById(planId);
});

const handleDelete = () => {
  isModalOpen.value = true;
};

const confirmDelete = () => {
  deletePlan(planId);
  router.push("/my-plans");
};

const handleRefine = () => {
  // TODO: Implement refine logic
};
</script>
