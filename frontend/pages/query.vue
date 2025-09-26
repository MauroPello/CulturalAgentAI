<template>
  <div class="query-container">
    <h1>Query Your Documents</h1>
    <p>Ask a question about the documents you've uploaded. The system will retrieve relevant information and prepare a prompt for the LLM.</p>
    
    <div class="input-group">
      <input
        v-model="query"
        type="text"
        placeholder="e.g., What was our revenue last quarter?"
        @keyup.enter="submitQuery"
        :disabled="isLoading"
      />
      <button @click="submitQuery" :disabled="isLoading">
        {{ isLoading ? 'Searching...' : 'Ask' }}
      </button>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-if="result" class="results-container">
      <hr />
      
      <div class="retrieved-chunks">
        <h3>Retrieved Chunks (Context)</h3>
        <p v-if="result.retrieved_chunks.length === 0">No relevant chunks found.</p>
        <ul>
          <li v-for="(chunk, index) in result.retrieved_chunks" :key="index">
            <p>"{{ chunk }}"</p>
          </li>
        </ul>
      </div>

      <div class="prepared-prompt">
        <h3>Prepared Prompt for LLM</h3>
        <pre>{{ result.prepared_prompt }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      result: null,
      isLoading: false,
      error: null,
    };
  },
  methods: {
    async submitQuery() {
      if (!this.query.trim()) {
        this.error = 'Please enter a query.';
        return;
      }

      this.isLoading = true;
      this.result = null;
      this.error = null;

      try {
        const response = await fetch('http://127.0.0.1:8000/query/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: this.query,
            n_results: 3 // Requesting top 3 chunks
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'An error occurred while fetching data.');
        }

        this.result = await response.json();

      } catch (err) {
        this.error = err.message;
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.query-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
}

p {
  color: #666;
  line-height: 1.5;
}

.input-group {
  display: flex;
  margin-top: 1.5rem;
  gap: 10px;
}

input {
  flex-grow: 1;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  color: #d9534f;
  text-align: center;
}

.results-container {
  margin-top: 2rem;
}

hr {
  border: 0;
  border-top: 1px solid #eee;
  margin: 2rem 0;
}

h3 {
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 5px;
  margin-bottom: 1rem;
}

.retrieved-chunks ul {
  list-style-type: none;
  padding: 0;
}

.retrieved-chunks li {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.prepared-prompt pre {
  background-color: #e9ecef;
  padding: 1rem;
  border-radius: 4px;
  white-space: pre-wrap; /* Allows text to wrap */
  word-wrap: break-word;
  font-family: monospace;
  color: #495057;
}
</style>