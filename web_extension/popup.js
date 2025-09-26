// Popup script for managing extension UI and data
document.addEventListener('DOMContentLoaded', async () => {
  // Clear any badge when popup is opened
  try {
    await browser.browserAction.setBadgeText({ text: "" });
  } catch (error) {
    console.log('Could not clear badge:', error);
  }
  
  await loadLastSelectedText();
  await loadRecentSelections();
  await loadCultureSettings();
  await loadLanguageSettings();
  setupEventListeners();
});

async function loadLastSelectedText() {
  try {
    const data = await browser.storage.local.get(['lastSelectedText', 'lastSelectedUrl', 'lastSelectedTime']);
    
    const textElement = document.getElementById('lastSelectedText');
    const urlElement = document.getElementById('lastSelectedUrl');
    const timeElement = document.getElementById('lastSelectedTime');
    
    if (data.lastSelectedText) {
      textElement.textContent = data.lastSelectedText;
      textElement.classList.remove('empty');
      
      // Only update URL element if it exists
      if (data.lastSelectedUrl && urlElement) {
        urlElement.textContent = `From: ${new URL(data.lastSelectedUrl).hostname}`;
      }
      
      // Only update time element if it exists
      if (data.lastSelectedTime && timeElement) {
        const time = new Date(data.lastSelectedTime);
        timeElement.textContent = `Selected: ${time.toLocaleDateString()} at ${time.toLocaleTimeString()}`;
      }
    } else {
      textElement.value = '';
      textElement.classList.add('empty');
    }
  } catch (error) {
    console.error('Error loading last selected text:', error);
  }
}

async function loadRecentSelections() {
  try {
    const data = await browser.storage.local.get('processedTexts');
    const recentSelections = data.processedTexts || [];
    const container = document.getElementById('recentSelections');
    
    // Only proceed if the container element exists
    if (!container) {
      console.log('Recent selections container not found - skipping');
      return;
    }
    
    if (recentSelections.length === 0) {
      container.innerHTML = '<div class="loading">No recent selections</div>';
      return;
    }
    
    // Sort by timestamp (most recent first) and limit to last 5
    const sortedSelections = recentSelections
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .slice(0, 5);
    
    container.innerHTML = sortedSelections.map(selection => {
      const time = new Date(selection.timestamp);
      const hostname = selection.sourceUrl ? new URL(selection.sourceUrl).hostname : 'Unknown';
      
      return `
        <div class="recent-item">
          <div class="recent-item-text">${escapeHtml(selection.text.substring(0, 100))}${selection.text.length > 100 ? '...' : ''}</div>
          <div class="recent-item-meta">
            From: ${hostname} • ${time.toLocaleDateString()} ${time.toLocaleTimeString()}
          </div>
        </div>
      `;
    }).join('');
    
  } catch (error) {
    console.error('Error loading recent selections:', error);
    const container = document.getElementById('recentSelections');
    if (container) {
      container.innerHTML = '<div class="loading">Error loading selections</div>';
    }
  }
}

async function loadCultureSettings() {
  try {
    const data = await browser.storage.local.get('selectedCulture');
    const cultureSelect = document.getElementById('cultureSelect');
    
    if (data.selectedCulture) {
      cultureSelect.value = data.selectedCulture;
    } else {
      // Default to American if no culture is saved
      cultureSelect.value = 'us';
      await browser.storage.local.set({ selectedCulture: 'us' });
    }
  } catch (error) {
    console.error('Error loading culture settings:', error);
  }
}

async function loadLanguageSettings() {
  try {
    const data = await browser.storage.local.get('selectedLanguage');
    const languageSelect = document.getElementById('languageSelect');
    
    if (data.selectedLanguage) {
      languageSelect.value = data.selectedLanguage;
    } else {
      // Default to English if no language is saved
      languageSelect.value = 'en';
      await browser.storage.local.set({ selectedLanguage: 'en' });
    }
  } catch (error) {
    console.error('Error loading language settings:', error);
  }
}

function setupEventListeners() {
  // Culture dropdown change handler
  document.getElementById('cultureSelect').addEventListener('change', async (event) => {
    try {
      const selectedCulture = event.target.value;
      await browser.storage.local.set({ selectedCulture });
      
      // Show visual feedback
      const dropdown = event.target;
      const originalStyle = dropdown.style.borderColor;
      dropdown.style.borderColor = '#4F46E5';
      dropdown.style.boxShadow = '0 0 0 2px rgba(79, 70, 229, 0.2)';
      
      setTimeout(() => {
        dropdown.style.borderColor = originalStyle;
        dropdown.style.boxShadow = '';
      }, 1000);
      
    } catch (error) {
      console.error('Error saving culture setting:', error);
    }
  });

  // Language dropdown change handler
  document.getElementById('languageSelect').addEventListener('change', async (event) => {
    try {
      const selectedLanguage = event.target.value;
      await browser.storage.local.set({ selectedLanguage });
      
      // Show visual feedback
      const dropdown = event.target;
      const originalStyle = dropdown.style.borderColor;
      dropdown.style.borderColor = '#4F46E5';
      dropdown.style.boxShadow = '0 0 0 2px rgba(79, 70, 229, 0.2)';
      
      setTimeout(() => {
        dropdown.style.borderColor = originalStyle;
        dropdown.style.boxShadow = '';
      }, 1000);
      
    } catch (error) {
      console.error('Error saving language setting:', error);
    }
  });

  // Align text button
  document.getElementById('alignText').addEventListener('click', async () => {
    await alignSelectedText();
  });
}

async function alignSelectedText() {
  try {
    // Get the last selected text
    const data = await browser.storage.local.get(['lastSelectedText', 'selectedCulture', 'selectedLanguage']);
    const text = data.lastSelectedText;
    const culture = data.selectedCulture || 'us';
    const language = data.selectedLanguage || 'en';

    if (!text || text.trim() === '') {
      alert('No text selected. Please select some text first.');
      return;
    }

    // Get button reference and show loading state
    const button = document.getElementById('alignText');
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="loading-spinner"></span> Aligning...';

    // Make API call to cultural_align_text endpoint
    const response = await fetch('http://localhost:8000/cultural_align_text/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        target_culture: culture,
        language: language
      })
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();

    // Update the "Recommended version" section with the aligned text
    const recommendedSection = document.getElementById('currentSelection');
    recommendedSection.textContent = result.better_version;
    recommendedSection.classList.remove('empty');

    // Show success feedback
    button.textContent = 'Success!';
    button.style.background = '#10B981';
    
    setTimeout(() => {
      button.textContent = originalText;
      button.style.background = '#4F46E5';
      button.disabled = false;
    }, 2000);

  } catch (error) {
    console.error('Error aligning text:', error);
    
    // Show error feedback
    const button = document.getElementById('alignText');
    button.textContent = 'Error!';
    button.style.background = '#EF4444';
    
    setTimeout(() => {
      button.textContent = 'Align Text';
      button.style.background = '#4F46E5';
      button.disabled = false;
    }, 3000);

    // Show error message to user
    alert(`Error aligning text: ${error.message}`);
  }
}


function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Listen for storage changes to update UI in real-time
browser.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local') {
    if (changes.lastSelectedText || changes.lastSelectedUrl || changes.lastSelectedTime) {
      loadLastSelectedText();
      // Highlight the last selected text section when it updates
      setTimeout(() => {
        const textElement = document.getElementById('lastSelectedText');
        if (textElement && !textElement.classList.contains('empty')) {
          textElement.style.animation = 'highlight 2s ease-out';
          setTimeout(() => {
            textElement.style.animation = '';
          }, 2000);
        }
      }, 100);
    }
    if (changes.processedTexts) {
      loadRecentSelections();
    }
  }
});