import type { ganttData } from "~/constants/ganttData";

export interface Plan extends Partial<typeof ganttData.gantt_plan> {
  id: string;
  project_name: string;
  project_description: string;
}
