<template>
  <div class="gantt-container">
    <!-- Project Header with Collapsible Description -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold">{{ plan?.project_name || 'Project Plan' }}</h2>
        <div class="flex items-center gap-2">
          <!-- Zoom Controls -->
          <div class="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
            <UButton 
              size="xs" 
              variant="ghost" 
              icon="i-heroicons-minus" 
              @click="zoomOut"
              :disabled="currentZoomLevel <= 0"
              title="Zoom Out"
            />
            <span class="text-xs px-2 py-1 text-gray-600 dark:text-gray-400">
              {{ zoomLevels[currentZoomLevel].label }}
            </span>
            <UButton 
              size="xs" 
              variant="ghost" 
              icon="i-heroicons-plus" 
              @click="zoomIn"
              :disabled="currentZoomLevel >= zoomLevels.length - 1"
              title="Zoom In"
            />
          </div>
          <!-- Description Toggle -->
          <UButton
            size="sm"
            variant="outline"
            :icon="showDescription ? 'i-heroicons-chevron-up' : 'i-heroicons-chevron-down'"
            @click="showDescription = !showDescription"
          >
            {{ showDescription ? 'Hide' : 'Show' }} Description
          </UButton>
        </div>
      </div>
      
      <!-- Collapsible Description -->
      <div v-if="showDescription" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 mb-4">
        <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
          {{ plan?.project_description || 'No description available.' }}
        </p>
        <div v-if="plan" class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
          <div>
            <span class="font-semibold text-gray-600 dark:text-gray-400">Start Date:</span>
            <p>{{ formatDate(plan.project_start_date) }}</p>
          </div>
          <div>
            <span class="font-semibold text-gray-600 dark:text-gray-400">End Date:</span>
            <p>{{ formatDate(plan.project_end_date) }}</p>
          </div>
          <div>
            <span class="font-semibold text-gray-600 dark:text-gray-400">Duration:</span>
            <p>{{ plan.total_duration_weeks }} weeks</p>
          </div>
          <div>
            <span class="font-semibold text-gray-600 dark:text-gray-400">Tasks:</span>
            <p>{{ plan.tasks?.length || 0 }} tasks</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Navigation and Filter Controls -->
    <div class="space-y-4 mb-4">
      <!-- Navigation Row -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <!-- Quick Navigation -->
          <div class="flex items-center gap-1">
            <UButton
              size="sm"
              variant="outline"
              icon="i-heroicons-home"
              @click="navigateToProjectStart"
              title="Go to Project Start"
            >
              Start
            </UButton>
            <UButton
              size="sm"
              variant="outline"
              icon="i-heroicons-calendar"
              @click="navigateToToday"
              title="Go to Today"
            >
              Today
            </UButton>
            <UButton
              size="sm"
              variant="outline"
              icon="i-heroicons-flag"
              @click="navigateToProjectEnd"
              title="Go to Project End"
            >
              End
            </UButton>
          </div>
          
          <!-- Navigation Controls -->
          <div class="h-6 w-px bg-gray-300 dark:bg-gray-600 mx-2"></div>
          <div class="flex items-center gap-1">
            <UButton
              size="sm"
              variant="ghost"
              icon="i-heroicons-backward"
              @click="navigateBackward"
              title="Previous Period"
            />
            <UButton
              size="sm"
              variant="ghost"
              icon="i-heroicons-forward"
              @click="navigateForward"
              title="Next Period"
            />
          </div>
        </div>
        
        <!-- Current View Info -->
        <div class="flex items-center gap-4">
          <div class="text-sm text-gray-600 dark:text-gray-400">
            <span class="font-medium">View:</span> {{ getCurrentViewPeriod() }}
          </div>
          <div v-if="selectedTask" class="text-sm text-blue-600 dark:text-blue-400">
            <span class="font-medium">Selected:</span> {{ selectedTask.name }}
          </div>
        </div>
      </div>
      
      <!-- Task Filter Row -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <!-- Priority Filter -->
          <USelect
            v-model="selectedPriorityFilter"
            :options="priorityFilterOptions"
            placeholder="Filter by Priority"
            size="sm"
            class="w-40"
            @change="updateTaskFilter"
          />
          
          <!-- Status Filter -->
          <USelect
            v-model="selectedStatusFilter"
            :options="statusFilterOptions"
            placeholder="Filter by Status"
            size="sm"
            class="w-40"
            @change="updateTaskFilter"
          />
          
          <!-- Search -->
          <UInput
            v-model="searchQuery"
            placeholder="Search tasks..."
            size="sm"
            icon="i-heroicons-magnifying-glass"
            class="w-48"
            @input="updateTaskFilter"
          />
          
          <!-- Clear Filters -->
          <UButton
            v-if="hasActiveFilters"
            size="sm"
            variant="ghost"
            icon="i-heroicons-x-mark"
            @click="clearAllFilters"
            title="Clear All Filters"
          />
        </div>
        
        <!-- Task Count Info -->
        <div class="text-sm text-gray-500 dark:text-gray-400">
          {{ filteredTaskCount }} / {{ totalTaskCount }} tasks
        </div>
      </div>
    </div>

    <!-- Gantt Chart Container -->
    <div ref="gstcEl" class="gstc-wrapper" />
    
    <!-- Help Panel -->
    <div class="mt-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <details class="group">
        <summary class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer list-none">
          <UIcon name="i-heroicons-question-mark-circle" class="w-4 h-4" />
          Keyboard Shortcuts & Tips
          <UIcon name="i-heroicons-chevron-down" class="w-3 h-3 transition-transform group-open:rotate-180" />
        </summary>
        <div class="mt-2 pl-6 text-xs text-gray-600 dark:text-gray-400 space-y-1">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <p class="font-medium text-gray-700 dark:text-gray-300">Navigation:</p>
              <ul class="space-y-1 mt-1">
                <li><kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Home</kbd> - Go to project start</li>
                <li><kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">End</kbd> - Go to project end</li>
                <li><kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Ctrl/Cmd + ←/→</kbd> - Navigate periods</li>
                <li><kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Ctrl/Cmd + 0</kbd> - Go to today</li>
              </ul>
            </div>
            <div>
              <p class="font-medium text-gray-700 dark:text-gray-300">Zoom & Selection:</p>
              <ul class="space-y-1 mt-1">
                <li><kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Ctrl/Cmd + +/-</kbd> - Zoom in/out</li>
                <li><kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Esc</kbd> - Clear selection</li>
                <li><span class="text-gray-500">Click tasks to select them</span></li>
                <li><span class="text-gray-500">Use filters to narrow down tasks</span></li>
              </ul>
            </div>
          </div>
        </div>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import GSTC, { type GSTCResult, type Row, type Item } from 'gantt-schedule-timeline-calendar';
import { Plugin as TimelinePointer } from 'gantt-schedule-timeline-calendar/dist/plugins/timeline-pointer.esm.min.js';
import { Plugin as Selection } from 'gantt-schedule-timeline-calendar/dist/plugins/selection.esm.min.js';
import { Plugin as ItemResizing } from 'gantt-schedule-timeline-calendar/dist/plugins/item-resizing.esm.min.js';
import { Plugin as ItemMovement } from 'gantt-schedule-timeline-calendar/dist/plugins/item-movement.esm.min.js';
import { Plugin as DependencyLines } from 'gantt-schedule-timeline-calendar/dist/plugins/dependency-lines.esm.min.js';
import 'gantt-schedule-timeline-calendar/dist/style.css';
import type { Plan } from '~/types/plan';

// Props
interface Props {
  plan?: Plan;
}

const props = withDefaults(defineProps<Props>(), {
  plan: undefined,
});

// Reactive state
const showDescription = ref(false);
const currentZoomLevel = ref(2); // Default to 'Weeks' view
const gstcEl = ref<HTMLDivElement | null>(null);
const selectedTask = ref<any>(null);

// Filter state
const selectedPriorityFilter = ref('all');
const selectedStatusFilter = ref('all');
const searchQuery = ref('');

// Filter options
const priorityFilterOptions = [
  { label: 'All Priorities', value: 'all' },
  { label: 'Critical', value: 'critical' },
  { label: 'High', value: 'high' },
  { label: 'Medium', value: 'medium' },
  { label: 'Low', value: 'low' }
];

const statusFilterOptions = [
  { label: 'All Status', value: 'all' },
  { label: 'Not Started', value: 'not_started' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
  { label: 'On Hold', value: 'on_hold' }
];

// Zoom levels configuration
const zoomLevels = [
  { label: 'Years', period: 'year', format: 'YYYY' },
  { label: 'Months', period: 'month', format: 'YYYY-MM' },
  { label: 'Weeks', period: 'week', format: 'YYYY-MM-DD' },
  { label: 'Days', period: 'day', format: 'YYYY-MM-DD' },
  { label: 'Hours', period: 'hour', format: 'YYYY-MM-DD HH' },
];

let gstc: GSTCResult;

// Use the plan data or fallback to sample data
const ganttData = computed(() => {
  if (props.plan) {
    return {
      success: true,
      gantt_plan: props.plan,
    };
  }
  
  // Fallback sample data
  return {
    "success": true,
    "gantt_plan": {
      "confidence": 0.92,
      "project_name": "Sample Project",
      "project_description": "Sample project for demonstration purposes",
      "project_owner": "Project Manager",
      "project_start_date": "2025-01-01",
      "project_end_date": "2025-06-30",
      "total_duration_weeks": 26,
      "tasks": []
    }
  };
});

const licenseKey = "====BEGIN LICENSE KEY====\nmETos+ErUJZyUsmGUgQlkgRXbC3qZEYa5628cDcSGS49XEcHbxlSa1SfOIYBjilJtAwqmKxGmf1rh+j8TklFAAsrvvAs0D3iGmCJ88PqNk9KVZAXw9HwBKv695WgRMw1D+K1SS9gE4SLI/mg88I/Qze6UPHsj2ip1xa+IRNanaX72tuinxAxg54utxiXM2lKeL6UdkuvsNfMJMiakVvOh+zJ8JmImsUMbIb+SCZhZzgeokm5b7Au62rhBIhJAVBbiyop2ZpOk7l4YEZIv4YMELpQ9hFThhAkpwhC6hi2euGWowKamDq0RLC/eEnoELzif4hNuib/Epf6hx5KOg3Fbg==||U2FsdGVkX18GQzmFDaLCsrFAoK/HL09cV3wYQ+DtAWRyJe70WlszYc4siRnq6HgHPXVOmhMdB3DNDLG/Q6UD5XEVJsnwGMU+5kooM1TFrww=\nlmCFtX6rYtv407DvU331WjBMWfbTzcY7Qy9grgKUG7bw4gJOfKPnH0/ohL8OZRgON1U89aiGH0klou3B2Au+4cXF4ZP0DJDiKYwKgFZWnQbw2C+ulaz0mHQ9iANyrgHpSJ7FqgNohXc5Lm54rkpkX+oiKIboQhsCLQURAwd7Yx/m2FGyzgrjGTvWDAQS3JIOsqDiNGSPeGdP6kMnB9ykcFdYTC6+3c50FgTovTE8kILgIgo59zyCmvfhmXK+KuPf5C4EicOTfsQcqaJmiR1/AX06gma4vSkM+eq8KuD1NQTDODyq0nT+g/4DBg+3y43vzQaqYfO9xNVc/2iKm88/vQ==\n====END LICENSE KEY====";

// Utility functions
const formatDate = (dateString: string | undefined): string => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};

// Computed properties for filtering
const filteredTasks = computed(() => {
  const tasks = ganttData.value.gantt_plan?.tasks || [];
  
  return tasks.filter(task => {
    // Priority filter
    if (selectedPriorityFilter.value !== 'all' && task.priority?.toLowerCase() !== selectedPriorityFilter.value) {
      return false;
    }
    
    // Status filter
    if (selectedStatusFilter.value !== 'all' && task.status?.toLowerCase() !== selectedStatusFilter.value) {
      return false;
    }
    
    // Search query filter
    if (searchQuery.value.trim() && !task.name?.toLowerCase().includes(searchQuery.value.toLowerCase().trim())) {
      return false;
    }
    
    return true;
  });
});

const hasActiveFilters = computed(() => {
  return selectedPriorityFilter.value !== 'all' ||
         selectedStatusFilter.value !== 'all' ||
         searchQuery.value.trim().length > 0;
});

const filteredTaskCount = computed(() => filteredTasks.value.length);
const totalTaskCount = computed(() => ganttData.value.gantt_plan?.tasks?.length || 0);

const getCurrentViewPeriod = (): string => {
  const level = zoomLevels[currentZoomLevel.value];
  return level.label;
};

// Navigation functions
const navigateToToday = () => {
  if (gstc && gstc.api && gstc.api.scroll && gstc.api.scroll.to) {
    try {
      const today = GSTC.api.date().startOf('day').valueOf();
      gstc.api.scroll.to.time(today);
    } catch (error) {
      console.warn('Navigation to today failed:', error);
    }
  }
};

const navigateToProjectStart = () => {
  if (gstc && gstc.api && gstc.api.scroll && gstc.api.scroll.to && ganttData.value.gantt_plan?.project_start_date) {
    try {
      const startDate = GSTC.api.date(ganttData.value.gantt_plan.project_start_date).startOf('day').valueOf();
      gstc.api.scroll.to.time(startDate);
    } catch (error) {
      console.warn('Navigation to project start failed:', error);
    }
  }
};

const navigateToProjectEnd = () => {
  if (gstc && gstc.api && gstc.api.scroll && gstc.api.scroll.to && ganttData.value.gantt_plan?.project_end_date) {
    try {
      const endDate = GSTC.api.date(ganttData.value.gantt_plan.project_end_date).startOf('day').valueOf();
      gstc.api.scroll.to.time(endDate);
    } catch (error) {
      console.warn('Navigation to project end failed:', error);
    }
  }
};

const navigateForward = () => {
  if (gstc && gstc.api && gstc.api.scroll && gstc.api.scroll.to && gstc.state) {
    try {
      const currentTime = gstc.state.get('config.chart.time.from') || Date.now();
      const timeAmount = getTimeAmountForZoom();
      const newTime = GSTC.api.date(currentTime).add(timeAmount.value, timeAmount.unit).valueOf();
      gstc.api.scroll.to.time(newTime);
    } catch (error) {
      console.warn('Forward navigation failed:', error);
    }
  }
};

const navigateBackward = () => {
  if (gstc && gstc.api && gstc.api.scroll && gstc.api.scroll.to && gstc.state) {
    try {
      const currentTime = gstc.state.get('config.chart.time.from') || Date.now();
      const timeAmount = getTimeAmountForZoom();
      const newTime = GSTC.api.date(currentTime).subtract(timeAmount.value, timeAmount.unit).valueOf();
      gstc.api.scroll.to.time(newTime);
    } catch (error) {
      console.warn('Backward navigation failed:', error);
    }
  }
};

// Filter functions
const updateTaskFilter = () => {
  // Update the Gantt chart with filtered tasks
  if (gstc && gstc.state) {
    try {
      const filteredRows = generateRowsFromFilteredData();
      const filteredItems = generateItemsFromFilteredData();
      
      gstc.state.update('config.list.rows', filteredRows);
      gstc.state.update('config.chart.items', filteredItems);
    } catch (error) {
      console.warn('Task filter update failed:', error);
    }
  }
};

const clearAllFilters = () => {
  selectedPriorityFilter.value = 'all';
  selectedStatusFilter.value = 'all';
  searchQuery.value = '';
  updateTaskFilter();
};

const getTimeAmountForZoom = () => {
  const level = zoomLevels[currentZoomLevel.value];
  switch (level.period) {
    case 'year': return { value: 1, unit: 'year' };
    case 'month': return { value: 3, unit: 'months' };
    case 'week': return { value: 4, unit: 'weeks' };
    case 'day': return { value: 7, unit: 'days' };
    case 'hour': return { value: 24, unit: 'hours' };
    default: return { value: 1, unit: 'week' };
  }
};

// Zoom functions
const zoomIn = () => {
  if (currentZoomLevel.value < zoomLevels.length - 1) {
    currentZoomLevel.value++;
    updateChartZoom();
  }
};

const zoomOut = () => {
  if (currentZoomLevel.value > 0) {
    currentZoomLevel.value--;
    updateChartZoom();
  }
};

const updateChartZoom = () => {
  if (!gstc || !gstc.state) {
    console.warn('GSTC not fully initialized for zoom update');
    return;
  }
  
  try {
    const level = zoomLevels[currentZoomLevel.value];
    let timeZoomConfig = {};
    
    switch (level.period) {
      case 'year':
        timeZoomConfig = {
          'chart.time.zoom': 20,
          'chart.time.scale': 'year'
        };
        break;
      case 'month':
        timeZoomConfig = {
          'chart.time.zoom': 21,
          'chart.time.scale': 'month'
        };
        break;
      case 'week':
        timeZoomConfig = {
          'chart.time.zoom': 22,
          'chart.time.scale': 'week'
        };
        break;
      case 'day':
        timeZoomConfig = {
          'chart.time.zoom': 23,
          'chart.time.scale': 'day'
        };
        break;
      case 'hour':
        timeZoomConfig = {
          'chart.time.zoom': 24,
          'chart.time.scale': 'hour'
        };
        break;
    }
    
    gstc.state.update('config', timeZoomConfig);
  } catch (error) {
    console.warn('Zoom update failed:', error);
  }
};

// Helper functions for generating chart data
function generateRowsFromData(): { [key: string]: Row } {
  const rows: { [key: string]: Row } = {};
  const tasks = ganttData.value.gantt_plan?.tasks || [];
  
  tasks.forEach(task => {
    if (task && task.id && task.name) {
      const id = GSTC.api.GSTCID(task.id);
      rows[id] = {
        id,
        label: task.name,
      };
    }
  });
  return rows;
}

function generateItemsFromData(): { [key: string]: Item } {
  const items: { [key: string]: Item } = {};
  const tasks = ganttData.value.gantt_plan?.tasks || [];
  
  tasks.forEach(task => {
    if (task && task.id && task.name && task.start_date && task.end_date) {
      const id = GSTC.api.GSTCID(task.id);
      items[id] = {
        id,
        label: task.name,
        rowId: id,
        time: {
          start: GSTC.api.date(task.start_date).startOf('day').valueOf(),
          end: GSTC.api.date(task.end_date).endOf('day').valueOf(),
        },
        dependencies: (task.dependencies || []).map(depId => GSTC.api.GSTCID(depId)),
        style: {
          backgroundColor: getPriorityColor(task.priority || 'medium'),
        },
      };
    }
  });
  return items;
}

// Filtered data generation functions
function generateRowsFromFilteredData(): { [key: string]: Row } {
  const rows: { [key: string]: Row } = {};
  const tasks = filteredTasks.value;
  
  tasks.forEach(task => {
    if (task && task.id && task.name) {
      const id = GSTC.api.GSTCID(task.id);
      rows[id] = {
        id,
        label: task.name,
      };
    }
  });
  return rows;
}

function generateItemsFromFilteredData(): { [key: string]: Item } {
  const items: { [key: string]: Item } = {};
  const tasks = filteredTasks.value;
  
  tasks.forEach(task => {
    if (task && task.id && task.name && task.start_date && task.end_date) {
      const id = GSTC.api.GSTCID(task.id);
      items[id] = {
        id,
        label: task.name,
        rowId: id,
        time: {
          start: GSTC.api.date(task.start_date).startOf('day').valueOf(),
          end: GSTC.api.date(task.end_date).endOf('day').valueOf(),
        },
        dependencies: (task.dependencies || []).filter(depId => 
          tasks.some(t => t.id === depId)
        ).map(depId => GSTC.api.GSTCID(depId)),
        style: {
          backgroundColor: getPriorityColor(task.priority || 'medium'),
        },
      };
    }
  });
  return items;
}

function getPriorityColor(priority: string): string {
  switch (priority?.toLowerCase()) {
    case 'critical': return '#dc2626'; // red-600
    case 'high': return '#ea580c'; // orange-600
    case 'medium': return '#ca8a04'; // yellow-600
    case 'low': return '#16a34a'; // green-600
    default: return '#6b7280'; // gray-500
  }
}

onMounted(() => {
  const config = {
    licenseKey,
    plugins: [TimelinePointer(), Selection(), ItemResizing(), ItemMovement(), DependencyLines()],
    list: {
      columns: {
        data: {
          [GSTC.api.GSTCID('label')]: {
            id: GSTC.api.GSTCID('label'),
            width: 250,
            data: 'label',
            header: {
              content: 'Task Name',
            },
          },
        },
      },
      rows: generateRowsFromData(),
    },
    chart: {
      items: generateItemsFromData(),
      time: {
        zoom: currentZoomLevel.value + 20,
      },
    },
    locale: {
      name: 'en',
      Now: 'Now',
      X_years: '{0} years',
      X_months: '{0} months',
      X_weeks: '{0} weeks',
      X_days: '{0} days',
    },
  };

  const state = GSTC.api.stateFromConfig(config);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (globalThis as any).state = state;

  gstc = GSTC({
    element: gstcEl.value as HTMLElement,
    state,
  });

  // Add event listeners for task interactions
  if (gstc.state) {
    // Task selection handler
    gstc.state.subscribe('config.chart.items', (items: any) => {
      // Listen for selection changes
      const selectedItemIds = gstc.state?.get('config.chart.selection.items') || [];
      if (selectedItemIds.length > 0) {
        const selectedId = selectedItemIds[0];
        const tasks = ganttData.value.gantt_plan?.tasks || [];
        const selectedTaskData = tasks.find(task => GSTC.api.GSTCID(task.id) === selectedId);
        selectedTask.value = selectedTaskData || null;
      } else {
        selectedTask.value = null;
      }
    });
  }

  // Add keyboard navigation
  const handleKeyDown = (event: KeyboardEvent) => {
    if (!gstc) return;
    
    switch (event.key) {
      case 'Home':
        event.preventDefault();
        navigateToProjectStart();
        break;
      case 'End':
        event.preventDefault();
        navigateToProjectEnd();
        break;
      case 'ArrowLeft':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          navigateBackward();
        }
        break;
      case 'ArrowRight':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          navigateForward();
        }
        break;
      case '+':
      case '=':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          zoomIn();
        }
        break;
      case '-':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          zoomOut();
        }
        break;
      case '0':
        if (event.ctrlKey || event.metaKey) {
          event.preventDefault();
          navigateToToday();
        }
        break;
      case 'Escape':
        selectedTask.value = null;
        break;
    }
  };

  // Add event listener
  document.addEventListener('keydown', handleKeyDown);

  // Clean up keyboard listener on unmount
  onBeforeUnmount(() => {
    document.removeEventListener('keydown', handleKeyDown);
  });

  // Set initial view to show project timeline - with delay to ensure GSTC is fully initialized
  if (ganttData.value.gantt_plan?.project_start_date) {
    // Use setTimeout to ensure GSTC is fully initialized before scrolling
    setTimeout(() => {
      try {
        if (gstc && gstc.api && gstc.api.scroll && gstc.api.scroll.to) {
          const startDate = GSTC.api.date(ganttData.value.gantt_plan.project_start_date).startOf('day').valueOf();
          gstc.api.scroll.to.time(startDate);
        }
      } catch (error) {
        console.warn('Initial scroll to project start failed:', error);
      }
    }, 100);
  }
});

onBeforeUnmount(() => {
  if (gstc) {
    gstc.destroy();
  }
});
</script>

<style scoped>
.gantt-container {
  @apply w-full;
}

.gstc-wrapper {
  height: 60vh;
  min-height: 400px;
  @apply border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s ease;
}

.gstc-wrapper:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Enhanced styling for better visual appeal and interactions */
.gstc-wrapper :deep(.gstc-list-column-header) {
  @apply bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-semibold;
}

.gstc-wrapper :deep(.gstc-list-row) {
  @apply border-b border-gray-100 dark:border-gray-700;
  transition: background-color 0.2s ease;
}

.gstc-wrapper :deep(.gstc-list-row:hover) {
  @apply bg-blue-50 dark:bg-blue-900/20;
}

.gstc-wrapper :deep(.gstc-list-row--selected) {
  @apply bg-blue-100 dark:bg-blue-800/30;
}

.gstc-wrapper :deep(.gstc-chart-timeline-items-item) {
  @apply rounded-md shadow-sm;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.gstc-wrapper :deep(.gstc-chart-timeline-items-item:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  opacity: 0.9;
}

.gstc-wrapper :deep(.gstc-chart-timeline-items-item--selected) {
  border: 2px solid #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Grid and timeline enhancements */
.gstc-wrapper :deep(.gstc-timeline-grid-line) {
  stroke: rgba(156, 163, 175, 0.6);
}

.dark .gstc-wrapper :deep(.gstc-timeline-grid-line) {
  stroke: rgba(75, 85, 99, 0.6);
}

/* Today pointer styling */
.gstc-wrapper :deep(.gstc-timeline-pointer) {
  stroke: #ef4444;
  stroke-width: 2px;
  opacity: 0.8;
}

/* Dependency lines */
.gstc-wrapper :deep(.gstc-dependency-line) {
  stroke: #6b7280;
  stroke-width: 1.5px;
  opacity: 0.7;
  transition: all 0.2s ease;
}

.gstc-wrapper :deep(.gstc-dependency-line:hover) {
  stroke: #3b82f6;
  opacity: 1;
  stroke-width: 2px;
}

/* Scrollbars */
.gstc-wrapper :deep(.gstc-list-main-scroll) {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.gstc-wrapper :deep(.gstc-list-main-scroll::-webkit-scrollbar) {
  width: 6px;
  height: 6px;
}

.gstc-wrapper :deep(.gstc-list-main-scroll::-webkit-scrollbar-track) {
  background: transparent;
}

.gstc-wrapper :deep(.gstc-list-main-scroll::-webkit-scrollbar-thumb) {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.gstc-wrapper :deep(.gstc-list-main-scroll::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(156, 163, 175, 0.7);
}
</style>
