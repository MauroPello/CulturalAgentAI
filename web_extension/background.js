// Background script for handling extension events
console.log('Cultural Agent Extension background script loaded');

// Create context menu when extension starts
browser.runtime.onInstalled.addListener(() => {
  browser.contextMenus.create({
    id: "send-to-cultural-agent",
    title: "Send to Cultural Agent",
    contexts: ["selection"]
  });
});

// Handle context menu clicks
browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "send-to-cultural-agent" && info.selectionText) {
    handleSelectedText(info.selectionText, tab);
  }
});

// Handle messages from content script
browser.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "sendSelectedText") {
    handleSelectedText(request.text, sender.tab);
    sendResponse({ success: true });
  }
});

// Main method to handle selected text
async function handleSelectedText(text, tab) {
  try {
    console.log('Selected text:', text);
    console.log('From tab:', tab.url);
    
    // Store the selected text in storage for popup to access
    await browser.storage.local.set({
      lastSelectedText: text,
      lastSelectedUrl: tab.url,
      lastSelectedTime: new Date().toISOString()
    });
    
    // Here you can add your custom logic to process the selected text
    // For example, send it to your Cultural Agent API
    await processTextWithCulturalAgent(text, tab.url);
    
    // Notify user of success and prompt to view results
    browser.tabs.sendMessage(tab.id, {
      action: "showSuccessNotification",
      message: "Text sent to Cultural Agent successfully!",
      showPopupPrompt: true
    });
    
    // Add a badge to the extension icon to draw attention
    browser.browserAction.setBadgeText({ text: "●" });
    browser.browserAction.setBadgeBackgroundColor({ color: "#10B981" });
    
    // Remove the badge after a few seconds
    setTimeout(() => {
      browser.browserAction.setBadgeText({ text: "" });
    }, 5000);
    
  } catch (error) {
    console.error('Error handling selected text:', error);
    browser.tabs.sendMessage(tab.id, {
      action: "showNotification",
      message: "Error: Failed to send text to Cultural Agent",
      type: "error"
    });
  }
}

// Method to process text with Cultural Agent (customize this for your needs)
async function processTextWithCulturalAgent(text, sourceUrl) {
  // Get the selected culture and language from storage
  const data = await browser.storage.local.get(['selectedCulture', 'selectedLanguage']);
  const selectedCulture = data.selectedCulture || 'us';
  const selectedLanguage = data.selectedLanguage || 'en';
  
  // This is where you would integrate with your Cultural Agent backend
  // For now, we'll just log the text and simulate processing
  
  console.log('Processing text with Cultural Agent:');
  console.log('Text:', text);
  console.log('Source URL:', sourceUrl);
  console.log('Target Culture:', selectedCulture);
  console.log('Target Language:', selectedLanguage);
  
  // Example: You could make an API call to your backend here
  // const response = await fetch('http://localhost:8000/api/process-text', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify({
  //     text: text,
  //     sourceUrl: sourceUrl,
  //     targetCulture: selectedCulture,
  //     targetLanguage: selectedLanguage,
  //     timestamp: new Date().toISOString()
  //   })
  // });
  
  // For demonstration, we'll just store it locally
  const existingData = await browser.storage.local.get('processedTexts') || {};
  const processedTexts = existingData.processedTexts || [];
  
  processedTexts.push({
    text: text,
    sourceUrl: sourceUrl,
    targetCulture: selectedCulture,
    targetLanguage: selectedLanguage,
    timestamp: new Date().toISOString(),
    id: Date.now().toString()
  });
  
  await browser.storage.local.set({ processedTexts: processedTexts });
  
  return { success: true, processed: true };
}