<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";

// This is a simplified version of the fetch function from [id].vue
async function fetchPreviousChats() {
  return new Promise<{id: number, title: string}[]>((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, title: "Asian Market Strategy" },
        { id: 2, title: "European Expansion" },
      ]);
    }, 100);
  });
}

const router = useRouter();

onMounted(async () => {
  const chats = await fetchPreviousChats();
  if (chats && chats.length > 0 && chats[0]) {
    router.push(`/ai-chat/${chats[0].id}`);
  } else {
    // Handle case with no chats, maybe redirect to a 'new-plan' page
    // or create a new chat automatically. For now, just log it.
    console.log("No chats found to redirect to.");
  }
});
</script>

<template>
  <div class="flex h-full items-center justify-center">
    <p>Loading chats...</p>
  </div>
</template>
