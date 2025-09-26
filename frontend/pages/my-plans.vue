<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">My Plans</h1>
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
          <h2 class="font-bold">
            {{ plan.project_name }}
          </h2>
        </template>
        <p>{{ plan.project_description }}</p>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePlans } from "~/composables/usePlans";

const { plans } = usePlans();

const router = useRouter();

const startNewPlanChat = () => {
  router.push("/new-plan");
};

const goToPlan = (planId: string) => {
  router.push(`/plans/${planId}`);
};
</script>
