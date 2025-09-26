import { ganttData } from "~/constants/ganttData";
import type { Plan } from "~/types/plan";

const plansData: Plan[] = [
  {
    ...ganttData.gantt_plan,
    id: "1",
    project_name: "Cultural Agent AI",
    project_description: "An AI-powered tool for cultural project management.",
  },
  {
    ...ganttData.gantt_plan,
    id: "2",
    project_name: "Another Plan",
    project_description: "A different project plan.",
  },
];

const plans = ref<Plan[]>(plansData);

export const usePlans = () => {
  const getPlanById = (id: string) => {
    return plans.value.find((p) => p.id === id);
  };

  const deletePlan = (id: string) => {
    plans.value = plans.value.filter((p) => p.id !== id);
  };

  return {
    plans,
    getPlanById,
    deletePlan,
  };
};
