<template>
  <div class="p-4">
    <div v-if="selectedPlan">
      <button class="mb-4 text-blue-500" @click="unselectPlan">
        &larr; Back to plans
      </button>
      <h1 class="text-2xl font-bold">
        {{ selectedPlan.project_name }}
      </h1>
      <ClientOnly>
        <GanttChart :plan="selectedPlan" />
      </ClientOnly>
    </div>
    <div v-else>
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
          v-for="(plan, index) in plans"
          :key="index"
          class="cursor-pointer"
          @click="selectPlan(plan)"
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
  </div>
</template>

<script setup lang="ts">
import { usePlans } from "~/composables/usePlans";

const { plans, selectedPlan, selectPlan, unselectPlan } = usePlans();

const router = useRouter();

const startNewPlanChat = () => {
  router.push("/new-plan");
};
</script>
