<template>
  <div ref="gstcEl" class="gstc-wrapper" />
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import GSTC, { type GSTCResult, type Row, type Item } from 'gantt-schedule-timeline-calendar';
import { Plugin as TimelinePointer } from 'gantt-schedule-timeline-calendar/dist/plugins/timeline-pointer.esm.min.js';
import { Plugin as Selection } from 'gantt-schedule-timeline-calendar/dist/plugins/selection.esm.min.js';
import { Plugin as ItemResizing } from 'gantt-schedule-timeline-calendar/dist/plugins/item-resizing.esm.min.js';
import { Plugin as ItemMovement } from 'gantt-schedule-timeline-calendar/dist/plugins/item-movement.esm.min.js';
import { Plugin as DependencyLines } from 'gantt-schedule-timeline-calendar/dist/plugins/dependency-lines.esm.min.js';
import 'gantt-schedule-timeline-calendar/dist/style.css';

const ganttData = {
  "success": true,
  "gantt_plan": {
    "confidence": 0.92,
    "project_name": "CraftHub E-commerce Platform",
    "project_description": "Multi-vendor marketplace for handmade crafts with comprehensive vendor management and customer experience features",
    "project_owner": "E-commerce Product Manager",
    "project_start_date": "2025-01-01",
    "project_end_date": "2025-06-30",
    "total_duration_weeks": 26,
    "tasks": [
      {
        "id": "T001",
        "name": "Market Research & Competitor Analysis",
        "description": "Analyze existing platforms and define unique value proposition for artisan marketplace",
        "start_date": "2025-01-01",
        "end_date": "2025-01-14",
        "duration_days": 14,
        "dependencies": [],
        "priority": "high",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Business Analyst", "Product Manager"],
        "resources": [],
        "tags": ["research", "planning"],
        "estimated_effort_hours": 80
      },
      {
        "id": "T002",
        "name": "Technical Architecture Design",
        "description": "Design scalable microservices architecture for multi-vendor platform",
        "start_date": "2025-01-15",
        "end_date": "2025-02-01",
        "duration_days": 17,
        "dependencies": ["T001"],
        "priority": "critical",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Lead Architect", "Backend Developer"],
        "resources": [],
        "tags": ["architecture", "technical"],
        "estimated_effort_hours": 120
      },
      {
        "id": "T003",
        "name": "Database Schema & API Design",
        "description": "Design multi-vendor database schema and RESTful API specifications",
        "start_date": "2025-02-01",
        "end_date": "2025-02-15",
        "duration_days": 14,
        "dependencies": ["T002"],
        "priority": "high",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Database Designer", "Backend Developer"],
        "resources": [],
        "tags": ["database", "api"],
        "estimated_effort_hours": 100
      },
      {
        "id": "T004",
        "name": "User Experience Design",
        "description": "Create user personas and journey maps for vendors and customers",
        "start_date": "2025-02-15",
        "end_date": "2025-03-01",
        "duration_days": 14,
        "dependencies": ["T001"],
        "priority": "high",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["UX Designer", "UI Designer"],
        "resources": [],
        "tags": ["design", "ux"],
        "estimated_effort_hours": 90
      },
      {
        "id": "T005",
        "name": "Brand Identity & Design System",
        "description": "Develop brand identity and comprehensive design system for platform",
        "start_date": "2025-03-01",
        "end_date": "2025-03-15",
        "duration_days": 14,
        "dependencies": ["T004"],
        "priority": "medium",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Brand Designer", "UI Designer"],
        "resources": [],
        "tags": ["branding", "design"],
        "estimated_effort_hours": 70
      },
      {
        "id": "T006",
        "name": "Backend Infrastructure Development",
        "description": "Build core backend services including authentication, vendor management, and payment processing",
        "start_date": "2025-03-15",
        "end_date": "2025-04-15",
        "duration_days": 31,
        "dependencies": ["T003"],
        "priority": "critical",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Backend Developer 1", "Backend Developer 2", "DevOps Engineer"],
        "resources": [],
        "tags": ["backend", "infrastructure"],
        "estimated_effort_hours": 240
      },
      {
        "id": "T007",
        "name": "Frontend Marketplace Development",
        "description": "Develop responsive web interface for customer marketplace with search and filtering",
        "start_date": "2025-04-01",
        "end_date": "2025-05-01",
        "duration_days": 30,
        "dependencies": ["T005", "T006"],
        "priority": "high",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Frontend Developer 1", "Frontend Developer 2"],
        "resources": [],
        "tags": ["frontend", "marketplace"],
        "estimated_effort_hours": 200
      },
      {
        "id": "T008",
        "name": "Vendor Portal Development",
        "description": "Build comprehensive vendor portal for product and order management",
        "start_date": "2025-04-15",
        "end_date": "2025-05-15",
        "duration_days": 30,
        "dependencies": ["T006"],
        "priority": "high",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Frontend Developer 3", "Backend Developer 1"],
        "resources": [],
        "tags": ["vendor", "portal"],
        "estimated_effort_hours": 180
      },
      {
        "id": "T009",
        "name": "Payment Integration & Security",
        "description": "Integrate Stripe payment processing with fraud detection and security measures",
        "start_date": "2025-05-01",
        "end_date": "2025-05-15",
        "duration_days": 14,
        "dependencies": ["T006"],
        "priority": "critical",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["Payment Specialist", "Security Engineer"],
        "resources": [],
        "tags": ["payment", "security"],
        "estimated_effort_hours": 100
      },
      {
        "id": "T010",
        "name": "Quality Assurance & Testing",
        "description": "Comprehensive testing including unit, integration, and user acceptance testing",
        "start_date": "2025-05-15",
        "end_date": "2025-06-01",
        "duration_days": 17,
        "dependencies": ["T007", "T008", "T009"],
        "priority": "high",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["QA Engineer 1", "QA Engineer 2"],
        "resources": [],
        "tags": ["testing", "qa"],
        "estimated_effort_hours": 120
      },
      {
        "id": "T011",
        "name": "Production Deployment & Launch",
        "description": "Deploy to production environment and execute go-to-market strategy",
        "start_date": "2025-06-01",
        "end_date": "2025-06-30",
        "duration_days": 29,
        "dependencies": ["T010"],
        "priority": "critical",
        "status": "not_started",
        "progress_percentage": 0,
        "assigned_to": ["DevOps Engineer", "Marketing Manager", "Project Manager"],
        "resources": [],
        "tags": ["deployment", "launch"],
        "estimated_effort_hours": 150
      }
    ],
    "milestones": [
      {
        "id": "M001",
        "name": "Technical Architecture Approved",
        "description": "Complete technical architecture design approved by stakeholders",
        "due_date": "2025-02-01",
        "success_criteria": ["Architecture document approved", "Technology stack finalized", "Development team aligned"]
      },
      {
        "id": "M002",
        "name": "Design System Completed",
        "description": "Complete design system and brand identity ready for implementation",
        "due_date": "2025-03-15",
        "success_criteria": ["Brand guidelines finalized", "Component library created", "Design system documentation complete"]
      },
      {
        "id": "M003",
        "name": "Backend Core Services Ready",
        "description": "All core backend services operational and tested",
        "due_date": "2025-04-15",
        "success_criteria": ["Authentication system working", "Payment processing integrated", "Vendor management APIs complete"]
      },
      {
        "id": "M004",
        "name": "Full Platform Functionality",
        "description": "Complete platform ready for comprehensive testing",
        "due_date": "2025-05-15",
        "success_criteria": ["Marketplace functional", "Vendor portal complete", "Payment flow working", "Search and filtering operational"]
      },
      {
        "id": "M005",
        "name": "Public Launch Ready",
        "description": "Platform tested, approved, and ready for public launch",
        "due_date": "2025-06-30",
        "success_criteria": ["All testing completed", "Performance benchmarks met", "Initial vendors onboarded", "Marketing campaign launched"]
      }
    ],
    "phases": [
      "Discovery & Planning",
      "Design & Prototyping",
      "Core Development",
      "Testing & Quality Assurance",
      "Launch & Deployment"
    ],
    "budget_estimate": 180000.0,
    "risk_factors": [
      "Payment processing integration complexities",
      "Vendor acquisition slower than expected",
      "Competition from established platforms like Etsy",
      "Scalability challenges during peak traffic periods",
      "Multi-vendor data management complexity",
      "Regulatory compliance for international transactions"
    ],
    "success_metrics": [
      "100+ vendors onboarded within first month",
      "1,000+ customer registrations in launch week",
      "Platform uptime > 99.9%",
      "Average page load time < 2 seconds",
      "Payment success rate > 99%",
      "Customer satisfaction score > 4.5/5"
    ],
    "metadata": {
      "created_by": "SwissAI API",
      "creation_date": "2025-09-26",
      "version": "1.0"
    }
  },
  "metadata": {
    "processing_time": "< 12 seconds",
    "model_used": "swiss-ai/apertus-8b-instruct",
    "confidence_score": 0.92,
    "tasks_generated": 11,
    "milestones_generated": 5,
    "api_version": "1.0.0",
    "timestamp": "2025-09-26T16:40:00"
  }
};

const licenseKey = "====BEGIN LICENSE KEY====\nmETos+ErUJZyUsmGUgQlkgRXbC3qZEYa5628cDcSGS49XEcHbxlSa1SfOIYBjilJtAwqmKxGmf1rh+j8TklFAAsrvvAs0D3iGmCJ88PqNk9KVZAXw9HwBKv695WgRMw1D+K1SS9gE4SLI/mg88I/Qze6UPHsj2ip1xa+IRNanaX72tuinxAxg54utxiXM2lKeL6UdkuvsNfMJMiakVvOh+zJ8JmImsUMbIb+SCZhZzgeokm5b7Au62rhBIhJAVBbiyop2ZpOk7l4YEZIv4YMELpQ9hFThhAkpwhC6hi2euGWowKamDq0RLC/eEnoELzif4hNuib/Epf6hx5KOg3Fbg==||U2FsdGVkX18GQzmFDaLCsrFAoK/HL09cV3wYQ+DtAWRyJe70WlszYc4siRnq6HgHPXVOmhMdB3DNDLG/Q6UD5XEVJsnwGMU+5kooM1TFrww=\nlmCFtX6rYtv407DvU331WjBMWfbTzcY7Qy9grgKUG7bw4gJOfKPnH0/ohL8OZRgON1U89aiGH0klou3B2Au+4cXF4ZP0DJDiKYwKgFZWnQbw2C+ulaz0mHQ9iANyrgHpSJ7FqgNohXc5Lm54rkpkX+oiKIboQhsCLQURAwd7Yx/m2FGyzgrjGTvWDAQS3JIOsqDiNGSPeGdP6kMnB9ykcFdYTC6+3c50FgTovTE8kILgIgo59zyCmvfhmXK+KuPf5C4EicOTfsQcqaJmiR1/AX06gma4vSkM+eq8KuD1NQTDODyq0nT+g/4DBg+3y43vzQaqYfO9xNVc/2iKm88/vQ==\n====END LICENSE KEY====";

let gstc: GSTCResult;
const gstcEl = ref<HTMLDivElement | null>(null);

// helper functions
function generateRowsFromData(): { [key: string]: Row } {
  const rows: { [key: string]: Row } = {};
  ganttData.gantt_plan.tasks.forEach(task => {
    const id = GSTC.api.GSTCID(task.id);
    rows[id] = {
      id,
      label: task.name,
    };
  });
  return rows;
}

function generateItemsFromData(): { [key: string]: Item } {
  const items: { [key: string]: Item } = {};
  ganttData.gantt_plan.tasks.forEach(task => {
    const id = GSTC.api.GSTCID(task.id);
    items[id] = {
      id,
      label: task.name,
      rowId: id,
      time: {
        start: GSTC.api.date(task.start_date).startOf('day').valueOf(),
        end: GSTC.api.date(task.end_date).endOf('day').valueOf(),
      },
      dependencies: task.dependencies.map(depId => GSTC.api.GSTCID(depId)),
    };
  });
  return items;
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
            width: 200,
            data: 'label',
            header: {
              content: 'Task',
            },
          },
        },
      },
      rows: generateRowsFromData(),
    },
    chart: {
      items: generateItemsFromData(),
    },
  };

  const state = GSTC.api.stateFromConfig(config);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (globalThis as any).state = state;

  gstc = GSTC({
    element: gstcEl.value as HTMLElement,
    state,
  });
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
