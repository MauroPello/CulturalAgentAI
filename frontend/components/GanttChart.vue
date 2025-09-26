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
import 'gantt-schedule-timeline-calendar/dist/style.css';

const licenseKey = "====BEGIN LICENSE KEY====\nmETos+ErUJZyUsmGUgQlkgRXbC3qZEYa5628cDcSGS49XEcHbxlSa1SfOIYBjilJtAwqmKxGmf1rh+j8TklFAAsrvvAs0D3iGmCJ88PqNk9KVZAXw9HwBKv695WgRMw1D+K1SS9gE4SLI/mg88I/Qze6UPHsj2ip1xa+IRNanaX72tuinxAxg54utxiXM2lKeL6UdkuvsNfMJMiakVvOh+zJ8JmImsUMbIb+SCZhZzgeokm5b7Au62rhBIhJAVBbiyop2ZpOk7l4YEZIv4YMELpQ9hFThhAkpwhC6hi2euGWowKamDq0RLC/eEnoELzif4hNuib/Epf6hx5KOg3Fbg==||U2FsdGVkX18GQzmFDaLCsrFAoK/HL09cV3wYQ+DtAWRyJe70WlszYc4siRnq6HgHPXVOmhMdB3DNDLG/Q6UD5XEVJsnwGMU+5kooM1TFrww=\nlmCFtX6rYtv407DvU331WjBMWfbTzcY7Qy9grgKUG7bw4gJOfKPnH0/ohL8OZRgON1U89aiGH0klou3B2Au+4cXF4ZP0DJDiKYwKgFZWnQbw2C+ulaz0mHQ9iANyrgHpSJ7FqgNohXc5Lm54rkpkX+oiKIboQhsCLQURAwd7Yx/m2FGyzgrjGTvWDAQS3JIOsqDiNGSPeGdP6kMnB9ykcFdYTC6+3c50FgTovTE8kILgIgo59zyCmvfhmXK+KuPf5C4EicOTfsQcqaJmiR1/AX06gma4vSkM+eq8KuD1NQTDODyq0nT+g/4DBg+3y43vzQaqYfO9xNVc/2iKm88/vQ==\n====END LICENSE KEY====";

let gstc: GSTCResult;
const gstcEl = ref<HTMLDivElement | null>(null);

// helper functions
function generateRows(): { [key: string]: Row } {
  const rows: { [key: string]: Row } = {};
  for (let i = 0; i < 100; i++) {
    const id = GSTC.api.GSTCID(i.toString());
    rows[id] = {
      id,
      label: `Row ${i}`,
    };
  }
  return rows;
}

function generateItems(): { [key: string]: Item } {
  const items: { [key: string]: Item } = {};
  let start = GSTC.api.date().startOf('day').subtract(6, 'day');
  for (let i = 0; i < 100; i++) {
    const id = GSTC.api.GSTCID(i.toString());
    const rowId = GSTC.api.GSTCID(Math.floor(Math.random() * 100).toString());
    start = start.add(1, 'day');
    items[id] = {
      id,
      label: `Item ${i}`,
      rowId,
      time: {
        start: start.valueOf(),
        end: start.add(1, 'day').endOf('day').valueOf(),
      },
    };
  }
  return items;
}

onMounted(() => {
  const config = {
    licenseKey,
    plugins: [TimelinePointer(), Selection(), ItemResizing(), ItemMovement()],
    list: {
      columns: {
        data: {
          [GSTC.api.GSTCID('id')]: {
            id: GSTC.api.GSTCID('id'),
            width: 60,
            data: ({ row }: { row: Row }) => GSTC.api.sourceID(row.id),
            header: {
              content: 'ID',
            },
          },
          [GSTC.api.GSTCID('label')]: {
            id: GSTC.api.GSTCID('label'),
            width: 200,
            data: 'label',
            header: {
              content: 'Label',
            },
          },
        },
      },
      rows: generateRows(),
    },
    chart: {
      items: generateItems(),
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
