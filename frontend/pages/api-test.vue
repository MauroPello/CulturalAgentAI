// Simple test page to verify API integration
<template>
  <div class="container mx-auto p-8">
    <h1 class="text-3xl font-bold mb-8">API Integration Test</h1>
    
    <div class="grid gap-6">
      <!-- Health Check Test -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-semibold">Health Check</h2>
        </template>
        
        <div class="space-y-4">
          <UButton 
            @click="testHealthCheck"
            :loading="healthLoading"
            color="primary"
          >
            Test Health Check
          </UButton>
          
          <div v-if="healthResult" class="p-4 bg-gray-50 rounded">
            <pre>{{ JSON.stringify(healthResult, null, 2) }}</pre>
          </div>
          
          <UAlert 
            v-if="healthError" 
            color="red" 
            :title="healthError"
          />
        </div>
      </UCard>

      <!-- Ask AI Test -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-semibold">Ask AI</h2>
        </template>
        
        <div class="space-y-4">
          <UInput 
            v-model="testQuery" 
            placeholder="Enter a test question"
            size="lg"
          />
          
          <UButton 
            @click="testAsk"
            :loading="askLoading"
            :disabled="!testQuery.trim()"
            color="primary"
          >
            Ask AI
          </UButton>
          
          <div v-if="askResult" class="p-4 bg-gray-50 rounded">
            <h3 class="font-semibold mb-2">Response:</h3>
            <p class="mb-4">{{ askResult.answer }}</p>
            <details>
              <summary class="cursor-pointer font-medium">Full Response Data</summary>
              <pre class="mt-2 text-xs">{{ JSON.stringify(askResult, null, 2) }}</pre>
            </details>
          </div>
          
          <UAlert 
            v-if="askError" 
            color="red" 
            :title="askError"
          />
        </div>
      </UCard>

      <!-- File List Test -->
      <UCard>
        <template #header>
          <h2 class="text-xl font-semibold">Get Files</h2>
        </template>
        
        <div class="space-y-4">
          <UButton 
            @click="testGetFiles"
            :loading="filesLoading"
            color="primary"
          >
            Get Uploaded Files
          </UButton>
          
          <div v-if="filesResult" class="p-4 bg-gray-50 rounded">
            <h3 class="font-semibold mb-2">Files ({{ filesResult.total_files }}):</h3>
            <div v-if="filesResult.files.length === 0" class="text-gray-500">
              No files uploaded yet
            </div>
            <ul v-else class="space-y-2">
              <li 
                v-for="file in filesResult.files" 
                :key="file.filename"
                class="flex justify-between items-center p-2 bg-white rounded border"
              >
                <span>{{ file.filename }}</span>
                <span class="text-sm text-gray-500">{{ formatFileSize(file.file_size) }}</span>
              </li>
            </ul>
          </div>
          
          <UAlert 
            v-if="filesError" 
            color="red" 
            :title="filesError"
          />
        </div>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
const testQuery = ref('What is artificial intelligence?')

// Health check
const healthLoading = ref(false)
const healthResult = ref(null)
const healthError = ref('')

const testHealthCheck = async () => {
  healthLoading.value = true
  healthError.value = ''
  healthResult.value = null
  
  try {
    const { api } = useApi()
    healthResult.value = await api.healthCheck()
  } catch (error) {
    healthError.value = error instanceof Error ? error.message : 'Unknown error'
  } finally {
    healthLoading.value = false
  }
}

// Ask AI
const askLoading = ref(false)
const askResult = ref(null)
const askError = ref('')

const testAsk = async () => {
  askLoading.value = true
  askError.value = ''
  askResult.value = null
  
  try {
    const { ask } = useApiCall()
    askResult.value = await ask(testQuery.value)
  } catch (error) {
    askError.value = error instanceof Error ? error.message : 'Unknown error'
  } finally {
    askLoading.value = false
  }
}

// Get files
const filesLoading = ref(false)
const filesResult = ref(null)
const filesError = ref('')

const testGetFiles = async () => {
  filesLoading.value = true
  filesError.value = ''
  filesResult.value = null
  
  try {
    const { getFiles } = useApiCall()
    filesResult.value = await getFiles()
  } catch (error) {
    filesError.value = error instanceof Error ? error.message : 'Unknown error'
  } finally {
    filesLoading.value = false
  }
}

// Helper function
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}
</script>