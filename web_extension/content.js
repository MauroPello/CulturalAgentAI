// Content script for handling text selection and UI interactions
console.log('Cultural Agent Extension content script loaded');

// Use chrome API with fallback to browser API for cross-browser compatibility
const api = typeof browser !== 'undefined' ? browser : chrome;

let isExtensionActive = false;
let selectedText = '';

// Create notification element
function createNotification() {
  const notification = document.createElement('div');
  notification.id = 'cultural-agent-notification';
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #10B981;
    color: white;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    z-index: 10001;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    display: none;
    max-width: 300px;
    word-wrap: break-word;
  `;
  
  document.body.appendChild(notification);
  return notification;
}

// Initialize elements
const notification = createNotification();

// Handle text selection for keyboard shortcut
document.addEventListener('mouseup', (e) => {
  setTimeout(() => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text.length > 0) {
      selectedText = text;
    }
  }, 10);
});

function sendSelectedText() {
  if (selectedText.length === 0) return;
  
  // Send message to background script
  api.runtime.sendMessage({
    action: "sendSelectedText",
    text: selectedText
  }).then(response => {
    console.log('Text sent successfully:', response);
    clearSelection();
  }).catch(error => {
    console.error('Error sending text:', error);
    showNotification('Error: Failed to send text', 'error');
  });
}

function clearSelection() {
  window.getSelection().removeAllRanges();
  selectedText = '';
}

function showNotification(message, type = 'success') {
  notification.textContent = message;
  notification.style.background = type === 'error' ? '#EF4444' : '#10B981';
  notification.style.display = 'block';
  
  setTimeout(() => {
    notification.style.display = 'none';
  }, 3000);
}

function showSuccessNotification(message, showPopupPrompt = false) {
  if (showPopupPrompt) {
    // Create an enhanced notification with popup prompt
    notification.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px;">
        <div style="flex: 1;">
          <div style="font-weight: 600; margin-bottom: 4px;">✅ ${message}</div>
          <div style="font-size: 12px; opacity: 0.9;">Click the extension icon to view details</div>
        </div>
        <div style="font-size: 24px; cursor: pointer; opacity: 0.8; hover: opacity: 1;" onclick="this.style.transform='scale(1.2)'; setTimeout(() => this.style.transform='scale(1)', 150);">
          🤖
        </div>
      </div>
    `;
    notification.style.background = '#10B981';
    notification.style.cursor = 'pointer';
    notification.style.maxWidth = '400px';
    notification.style.display = 'block';
    
    // Add click handler to notification
    notification.onclick = () => {
      // Visual feedback
      notification.style.transform = 'scale(0.95)';
      setTimeout(() => {
        notification.style.transform = 'scale(1)';
        notification.style.display = 'none';
      }, 150);
      
      // Send message to inform user to click extension icon
      showNotification('Click the Cultural Agent extension icon in your toolbar!', 'success');
    };
    
    // Auto-hide after longer duration for enhanced notification
    setTimeout(() => {
      notification.style.display = 'none';
      notification.onclick = null;
      notification.style.cursor = 'default';
    }, 8000);
  } else {
    showNotification(message, 'success');
  }
}

// Listen for messages from background script
api.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "showNotification") {
    showNotification(request.message, request.type);
  } else if (request.action === "showSuccessNotification") {
    showSuccessNotification(request.message, request.showPopupPrompt);
  }
});

// Keyboard shortcut (Ctrl/Cmd + Shift + C)
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text.length > 0) {
      selectedText = text;
      sendSelectedText();
    }
  }
});