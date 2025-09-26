import { ganttData } from "~/constants/ganttData";
import type { Plan } from "~/types/plan";

export const usePlans = () => {
  const plans = ref([ganttData.gantt_plan, { ...ganttData.gantt_plan, project_name: "Another Plan" }]);
  const selectedPlan = ref<Plan | null>(null);

  const selectPlan = (plan: Plan) => {
    selectedPlan.value = plan;
  };

  const unselectPlan = () => {
    selectedPlan.value = null;
  };

  return {
    plans,
    selectedPlan,
    selectPlan,
    unselectPlan,
  };
};
