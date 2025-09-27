export type Task = {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  dependencies: string[];
  progress: number;
  assignee: string;
  description: string;
  status: string;
};

export interface Plan {
  id: string;
  project_name: string;
  project_description: string;
  tasks: Task[];
}
