# Cultural Agent Text Selector - Firefox Extension

A Firefox web extension that allows users to select text on any webpage and send it to the Cultural Agent AI system for processing.

## Features

- **Text Selection**: Select any text on a webpage
- **Multiple Activation Methods**:
  - Floating button that appears after text selection
  - Right-click context menu
  - Keyboard shortcut (Ctrl+Shift+C)
- **Visual Feedback**: Success/error notifications
- **History Tracking**: View recently selected texts
- **Clean UI**: Modern popup interface

## Installation

### Development Installation

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox" in the left sidebar
3. Click "Load Temporary Add-on"
4. Navigate to the `web_extension` folder and select `manifest.json`

### Production Installation

1. Package the extension:
   ```bash
   cd web_extension
   zip -r cultural-agent-extension.zip . -x "*.DS_Store" "node_modules/*"
   ```
2. Submit to Firefox Add-ons store or install manually

## Usage

1. **Install the extension** following the instructions above
2. **Navigate to any webpage**
3. **Select text** you want to send to Cultural Agent
4. **Choose one of these methods**:
   - Click the blue floating "🤖 Send to Cultural Agent" button
   - Right-click and select "Send to Cultural Agent" from context menu
   - Use keyboard shortcut `Ctrl+Shift+C` (or `Cmd+Shift+C` on Mac)
5. **View your selections** by clicking the extension icon in the toolbar

## Customization

### Integrating with Your Backend

Edit the `processTextWithCulturalAgent` function in `background.js` to integrate with your Cultural Agent API:

```javascript
async function processTextWithCulturalAgent(text, sourceUrl) {
  // Replace this with your actual API endpoint
  const response = await fetch('http://localhost:8000/api/process-text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      sourceUrl: sourceUrl,
      timestamp: new Date().toISOString()
    })
  });
  
  return await response.json();
}
```

### Styling

- Modify `content.css` to change the floating button appearance
- Edit `popup.css` to customize the popup interface
- Update colors, fonts, and animations as needed

## File Structure

```
web_extension/
├── manifest.json          # Extension configuration
├── background.js          # Background script (handles logic)
├── content.js            # Content script (handles UI on pages)
├── content.css           # Styles for content script elements
├── popup.html            # Popup interface HTML
├── popup.css             # Popup interface styles
├── popup.js              # Popup interface logic
├── icons/                # Extension icons
└── README.md             # This file
```

## Permissions

The extension requests these permissions:
- `activeTab`: Access to the current active tab
- `contextMenus`: Create right-click context menu items
- `storage`: Store selected text history locally

## Browser Compatibility

- **Firefox**: Manifest V2 (tested on Firefox 90+)
- **Chrome/Edge**: Would need conversion to Manifest V3

## Development

### Making Changes

1. Edit the relevant files
2. Go to `about:debugging` in Firefox
3. Click "Reload" next to your extension
4. Test your changes

### Debugging

- Use Firefox Developer Tools
- Check the browser console for errors
- Use `console.log()` statements in the scripts

## Security Notes

- The extension only accesses text that users explicitly select
- No automatic data collection or transmission
- All data stored locally in browser storage
- No external network requests by default (customize as needed)

## License

This extension is part of the Cultural Agent AI project.