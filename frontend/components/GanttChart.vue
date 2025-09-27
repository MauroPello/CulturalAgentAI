<template>
  <div ref="gstcEl" class="gstc-wrapper" />
  <TaskDetailsModal
    v-if="selectedTask"
    v-model="isModalVisible"
    :task="selectedTask"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import GSTC, { type GSTCResult, type Row, type Item } from 'gantt-schedule-timeline-calendar';
import { Plugin as TimelinePointer } from 'gantt-schedule-timeline-calendar/dist/plugins/timeline-pointer.esm.min.js';
import { Plugin as Selection } from 'gantt-schedule-timeline-calendar/dist/plugins/selection.esm.min.js';
import { Plugin as ItemResizing } from 'gantt-schedule-timeline-calendar/dist/plugins/item-resizing.esm.min.js';
import { Plugin as ItemMovement } from 'gantt-schedule-timeline-calendar/dist/plugins/item-movement.esm.min.js';
import { Plugin as DependencyLines } from 'gantt-schedule-timeline-calendar/dist/plugins/dependency-lines.esm.min.js';
import { Plugin as ProgressBar } from 'gantt-schedule-timeline-calendar/dist/plugins/progress-bar.esm.min.js';
import { Plugin as HighlightWeekends } from 'gantt-schedule-timeline-calendar/dist/plugins/highlight-weekends.esm.min.js';
import 'gantt-schedule-timeline-calendar/dist/style.css';
import type { Plan, Task } from '~/types/plan';
import TaskDetailsModal from './TaskDetailsModal.vue';

const props = defineProps<{
  plan: Plan;
}>();

const licenseKey = "====BEGIN LICENSE KEY====\nmETos+ErUJZyUsmGUgQlkgRXbC3qZEYa5628cDcSGS49XEcHbxlSa1SfOIYBjilJtAwqmKxGmf1rh+j8TklFAAsrvvAs0D3iGmCJ88PqNk9KVZAXw9HwBKv695WgRMw1D+K1SS9gE4SLI/mg88I/Qze6UPHsj2ip1xa+IRNanaX72tuinxAxg54utxiXM2lKeL6UdkuvsNfMJMiakVvOh+zJ8JmImsUMbIb+SCZhZzgeokm5b7Au62rhBIhJAVBbiyop2ZpOk7l4YEZIv4YMELpQ9hFThhAkpwhC6hi2euGWowKamDq0RLC/eEnoELzif4hNuib/Epf6hx5KOg3Fbg==||U2FsdGVkX18GQzmFDaLCsrFAoK/HL09cV3wYQ+DtAWRyJe70WlszYc4siRnq6HgHPXVOmhMdB3DNDLG/Q6UD5XEVJsnwGMU+5kooM1TFrww=\nlmCFtX6rYtv407DvU331WjBMWfbTzcY7Qy9grgKUG7bw4gJOfKPnH0/ohL8OZRgON1U89aiGH0klou3B2Au+4cXF4ZP0DJDiKYwKgFZWnQbw2C+ulaz0mHQ9iANyrgHpSJ7FqgNohXc5Lm54rkpkX+oiKIboQhsCLQURAwd7Yx/m2FGyzgrjGTvWDAQS3JIOsqDiNGSPeGdP6kMnB9ykcFdYTC6+3c50FgTovTE8kILgIgo59zyCmvfhmXK+KuPf5C4EicOTfsQcqaJmiR1/AX06gma4vSkM+eq8KuD1NQTDODyq0nT+g/4DBg+3y43vzQaqYfO9xNVc/2iKm88/vQ==\n====END LICENSE KEY====";

let gstc: GSTCResult;
const gstcEl = ref<HTMLDivElement | null>(null);
const selectedTask = ref<Task | null>(null);
const isModalVisible = ref(false);

const assigneeIcons: { [key: string]: string } = {};
const availableIcons = ['/assets/icons/fox.png', '/assets/icons/gorilla.png', '/assets/icons/reindeer.png'];
let iconIndex = 0;

function getAssigneeIcon(assignee: string) {
  if (!assignee) return '/assets/icons/user.png';
  if (!assigneeIcons[assignee]) {
    assigneeIcons[assignee] = availableIcons[iconIndex % availableIcons.length];
    iconIndex++;
  }
  return assigneeIcons[assignee];
}

// helper functions
function generateRowsFromData(): { [key: string]: Row } {
  if (!props.plan) return {};
  const rows: { [key: string]: Row } = {};
  props.plan.tasks?.forEach(task => {
    const id = GSTC.api.GSTCID(task.id);
    rows[id] = {
      id,
      label: task.name,
    };
  });
  return rows;
}

function generateItemsFromData(): { [key: string]: Item } {
  if (!props.plan) return {};
  const items: { [key: string]: Item } = {};
  props.plan.tasks?.forEach(task => {
    const id = GSTC.api.GSTCID(task.id);
    items[id] = {
      id,
      label: task.name,
      rowId: id,
      time: {
        start: GSTC.api.date(task.start_date).startOf('day').valueOf(),
        end: GSTC.api.date(task.end_date).endOf('day').valueOf(),
      },
      progress: task.progress,
      dependencies: task.dependencies.map(depId => GSTC.api.GSTCID(depId)),
      assignee: task.assignee,
    };
  });
  return items;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function handleItemClick(element: any, data: { item: Item }) {
  if (!data) return;

  function onClick() {
    const clickedItemId = GSTC.api.sourceID(data.item.id);
    const task = props.plan.tasks?.find(t => t.id === clickedItemId);
    if (task) {
      selectedTask.value = task;
      isModalVisible.value = true;
    }
  }

  element.addEventListener("click", onClick);
}

onMounted(() => {
  if (!props.plan) return;

  const config = {
    licenseKey,
    plugins: [TimelinePointer(), Selection(), ItemResizing(), ItemMovement(), DependencyLines(), ProgressBar(), HighlightWeekends()],
    actions: {
      'chart-timeline-items-row-item': [handleItemClick],
    },
    list: {
      columns: {
        data: {
          [GSTC.api.GSTCID('label')]: {
            id: GSTC.api.GSTCID('label'),
            width: 200,
            data: 'label',
            header: {
              content: 'Task',
            },
          },
          [GSTC.api.GSTCID('start_date')]: {
            id: GSTC.api.GSTCID('start_date'),
            width: 120,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            data: (row: any) => (findTaskByName(props.plan, row?.row?.label)?.start_date),
            header: {
              content: 'Start Date',
            },
          },
          [GSTC.api.GSTCID('end_date')]: {
            id: GSTC.api.GSTCID('end_date'),
            width: 120,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            data: (row: any) => (findTaskByName(props.plan, row?.row?.label)?.end_date),
            header: {
              content: 'End Date',
            },
          },
          [GSTC.api.GSTCID('progress')]: {
            id: GSTC.api.GSTCID('progress'),
            width: 80,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            data: (row: any) => (String(findTaskByName(props.plan, row?.row?.label)?.progress ?? 0) + "%"),
            header: {
              content: 'Progress',
            },
          },
          [GSTC.api.GSTCID('assignee')]: {
            id: GSTC.api.GSTCID('assignee'),
            width: 80,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            data: (row: any) => {
              const assignee = findTaskByName(props.plan, row?.row?.label)?.assignee;
              const iconSrc = getAssigneeIcon(assignee);
              const altText = assignee || 'Unassigned';
              return `<img src="${iconSrc}" alt="${altText}" title="${altText}" style="width: 24px; height: 24px; border-radius: 50%;" />`;
            },
            isHTML: true,
            header: {
              content: 'Assignee',
            },
          },
        },
      },
      rows: generateRowsFromData(),
    },
    chart: {
      items: generateItemsFromData(),
    },
    locale: {
      name: 'en',
      weekdays: 'Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday'.split('_'),
      weekdaysShort: 'Sun_Mon_Tue_Wed_Thu_Fri_Sat'.split('_'),
      weekdaysMin: 'Su_Mo_Tu_We_Th_Fr_Sa'.split('_'),
      months: 'January_February_March_April_May_June_July_August_September_October_November_December'.split('_'),
      monthsShort: 'Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec'.split('_'),
      ordinal: (n: number) => `${n}${n === 1 ? 'st' : n === 2 ? 'nd' : n === 3 ? 'rd' : 'th'}`,
      weekStart: 1,
      relativeTime: {
        future: 'in %s',
        past: '%s ago',
        s: 'a few seconds',
        m: 'a minute',
        mm: '%d minutes',
        h: 'an hour',
        hh: '%d hours',
        d: 'a day',
        dd: '%d days',
        M: 'a month',
        MM: '%d months',
        y: 'a year',
        yy: '%d years',
      },
    },
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const state = GSTC.api.stateFromConfig(config as any);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (globalThis as any).state = state;

  gstc = GSTC({
    element: gstcEl.value as HTMLElement,
    state,
  });

  watch(() => props.plan, (newPlan) => {
    if (newPlan) {
      const rows = generateRowsFromData();
      const items = generateItemsFromData();
      state.update('config.list.rows', rows);
      state.update('config.chart.items', items);
    }
  }, { deep: true });
});

onBeforeUnmount(() => {
  if (gstc) {
    gstc.destroy();
  }
});
</script>

<style scoped>
.gstc-wrapper {
  height: 70vh;
}
</style>
