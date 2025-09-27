import { ganttData } from "~/constants/ganttData";
import type { Plan } from "~/types/plan";

const STORAGE_KEY = "gantt-plans";

const initialPlans: Plan[] = [];

if (import.meta.client) {
  const storedPlans = localStorage.getItem(STORAGE_KEY);
  if (storedPlans) {
    initialPlans.push(...JSON.parse(storedPlans));
  }
}

const plans = ref<Plan[]>(initialPlans);

if (import.meta.client) {
  watch(
    plans,
    (newPlans) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newPlans));
    },
    { deep: true }
  );
}

export const usePlans = () => {
  const getPlanById = (id: string) => {
    return plans.value.find((p) => p.id === id);
  };

  const deletePlan = (id: string) => {
    plans.value = plans.value.filter((p) => p.id !== id);
  };

  const updatePlan = (id: string, updatedPlan: Plan) => {
    const index = plans.value.findIndex((p) => p.id === id);
    if (index !== -1) {
      plans.value[index] = { ...plans.value[index], ...updatedPlan };
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const createPlan = (projectName: string, projectDescription: string, ganttPlan?: any) => {
    const newPlan: Plan = {
      ...(ganttPlan || ganttData.gantt_plan),
      id: String(new Date().getTime()),
      project_name: projectName,
      project_description: projectDescription,
    };
    plans.value.push(newPlan);
    return newPlan;
  };

  return {
    plans,
    getPlanById,
    deletePlan,
    updatePlan,
    createPlan,
  };
};
