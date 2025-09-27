import { ref, onMounted } from "vue";

export interface Document {
  id: number;
  name: string;
  size: string;
  upload_date: string;
  status: "processing" | "completed";
  file_id: string;
}

interface ApiFile {
  filename: string;
  file_size: number;
  upload_time: number;
  file_id: string;
}

const documents = ref<Document[]>([]);
const isLoadingDocuments = ref(false);

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const formatDate = (timestamp: number): string => {
  return new Date(timestamp * 1000).toLocaleDateString();
};

const fetchDocuments = async () => {
  isLoadingDocuments.value = true;
  try {
    const response = await fetch("http://localhost:8000/uploaded-files");
    if (response.ok) {
      const data = await response.json();
      documents.value = data.files.map((file: ApiFile, index: number) => ({
        id: index + 1,
        name: file.filename,
        size: formatFileSize(file.file_size),
        upload_date: formatDate(file.upload_time),
        status: "completed" as const,
        file_id: file.file_id
      }));
    } else {
      console.error("Failed to fetch documents:", response.statusText);
      documents.value = [];
    }
  } catch (error) {
    console.error("Error fetching documents:", error);
    documents.value = [];
  } finally {
    isLoadingDocuments.value = false;
  }
};

export function useDocuments() {
  onMounted(() => {
    if (documents.value.length === 0) {
      fetchDocuments();
    }
  });

  return {
    documents,
    isLoadingDocuments,
    fetchDocuments,
  };
}
