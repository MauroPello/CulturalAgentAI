<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold pb-4">My Plans</h1>
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      <UCard
        class="flex flex-col items-center justify-center text-center cursor-pointer hover:bg-gray-100"
        @click="startNewPlanChat"
      >
        <UIcon
          name="i-heroicons-plus-circle"
          class="w-12 h-12 text-gray-400"
        />
        <h2 class="mt-2 font-bold">New Plan</h2>
        <p class="text-sm text-gray-500">
          Start a chat with our AI to create a new plan
        </p>
      </UCard>
      <UCard
        v-for="plan in plans"
        :key="plan.id"
        class="cursor-pointer"
        @click="goToPlan(plan.id)"
      >
        <template #header>
          <div class="flex items-center justify-between">
            <h2 class="font-bold">
              {{ plan.project_name }}
            </h2>
            <UButton
              icon="i-heroicons-trash"
              color="red"
              variant="ghost"
              @click.stop="handleDeletePlan(plan.id)"
            />
          </div>
        </template>
        <p>{{ plan.project_description }}</p>
      </UCard>
    </div>
    <UModal v-model="isDeleteModalOpen">
      <UCard>
        <template #header>
          <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
            Confirm Deletion
          </h3>
        </template>

        <p>Are you sure you want to delete this plan?</p>

        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton color="gray" variant="ghost" @click="isDeleteModalOpen = false">
              Cancel
            </UButton>
            <UButton color="red" @click="confirmDeletePlan">
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

const { plans, deletePlan } = usePlans();

const router = useRouter();
const isDeleteModalOpen = ref(false);
const planToDeleteId = ref<string | null>(null);

const startNewPlanChat = () => {
  router.push("/new-plan");
};

const goToPlan = (planId: string) => {
  router.push(`/plans/${planId}`);
};

const handleDeletePlan = (planId: string) => {
  planToDeleteId.value = planId;
  isDeleteModalOpen.value = true;
};

const confirmDeletePlan = () => {
  if (planToDeleteId.value) {
    deletePlan(planToDeleteId.value);
  }
  isDeleteModalOpen.value = false;
};
</script>
