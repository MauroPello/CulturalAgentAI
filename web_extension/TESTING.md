# Testing Guide for Cultural Agent Firefox Extension

## 🚀 Quick Start Testing

### Step 1: Install the Extension in Firefox

1. **Open Firefox** (make sure you have Firefox installed)
2. **Navigate to** `about:debugging` in the address bar
3. **Click "This Firefox"** in the left sidebar
4. **Click "Load Temporary Add-on..."** button
5. **Navigate to** `/home/mattia/Documents/GitHub/CulturalAgentAI/web_extension/`
6. **Select** `manifest.json` file
7. **Click "Open"**

✅ You should see "Cultural Agent Text Selector" appear in the loaded extensions list.

### Step 2: Verify Installation

1. **Look for the extension icon** in your Firefox toolbar (🤖 robot icon)
2. **Click the extension icon** to open the popup
3. **Verify the popup opens** with the Cultural Agent interface

### Step 3: Test Text Selection Features

#### Method 1: Floating Button Test
1. **Go to any website** (e.g., Wikipedia, news site, GitHub)
2. **Select some text** on the page
3. **Look for the blue floating button** "🤖 Send to Cultural Agent"
4. **Click the button**
5. **Verify:**
   - Success notification appears
   - Extension icon gets a green badge (●)
   - Notification suggests clicking the extension icon

#### Method 2: Context Menu Test
1. **Go to any website**
2. **Select some text**
3. **Right-click** on the selected text
4. **Look for "Send to Cultural Agent"** in the context menu
5. **Click it**
6. **Verify same results** as Method 1

#### Method 3: Keyboard Shortcut Test
1. **Go to any website**
2. **Select some text**
3. **Press `Ctrl+Shift+C`** (or `Cmd+Shift+C` on Mac)
4. **Verify same results** as Method 1

### Step 4: Test Popup Functionality

1. **After sending text**, click the extension icon
2. **Verify the popup shows:**
   - Your selected text in "Last Selected Text" section
   - Source URL where text came from
   - Timestamp of selection
   - Text highlighting animation
3. **Send more text** from different websites
4. **Check "Recent Selections"** section updates
5. **Test "Clear History"** button works

## 🛠️ Development Testing

### Enable Extension Console Logging

1. **Go to** `about:debugging`
2. **Find your extension** in the list
3. **Click "Inspect"** next to your extension
4. **Open the Console tab**
5. **Watch for log messages** when you use the extension

### Test Error Handling

1. **Modify the background.js** to simulate API errors
2. **Send text** and verify error notifications work
3. **Check console** for error logs

### Test Different Websites

Try the extension on various types of websites:
- News sites (CNN, BBC)
- Documentation sites (MDN, GitHub)
- Social media (Reddit, Twitter)
- E-commerce sites
- Wikipedia articles

## 🔧 Troubleshooting

### Extension Not Loading?
```bash
# Check manifest.json syntax
cd /home/mattia/Documents/GitHub/CulturalAgentAI/web_extension
cat manifest.json | python -m json.tool
```

### Icons Not Showing?
```bash
# Verify icon files exist
ls -la icons/
```

### Popup Not Opening?
1. Check browser console for errors
2. Verify popup.html loads correctly
3. Check if popup.js has syntax errors

### Text Selection Not Working?
1. Check content script injection
2. Verify permissions in manifest.json
3. Look for JavaScript errors in page console

## 📝 Test Scenarios

### Basic Functionality Tests
- [ ] Extension loads without errors
- [ ] Popup opens and displays correctly
- [ ] Text selection detection works
- [ ] Floating button appears on selection
- [ ] Context menu item appears
- [ ] Keyboard shortcut works
- [ ] Notifications display properly
- [ ] Badge appears on extension icon
- [ ] History tracking works
- [ ] Clear history function works

### Edge Cases
- [ ] Very long text selection (1000+ characters)
- [ ] Empty text selection
- [ ] Special characters (emojis, unicode)
- [ ] Multiple rapid selections
- [ ] Selections from iframes
- [ ] Selections from password fields
- [ ] Selections on dynamic content (AJAX loaded)

### Browser Compatibility
- [ ] Firefox Desktop (latest)
- [ ] Firefox ESR
- [ ] Different screen resolutions
- [ ] With other extensions installed

## 🔄 Reload Extension for Changes

When you make code changes:

1. **Go to** `about:debugging`
2. **Find your extension**
3. **Click "Reload"** button
4. **Test your changes**

Or use the build script:
```bash
cd /home/mattia/Documents/GitHub/CulturalAgentAI/web_extension
./build.sh
# Then reload in Firefox
```

## 🐛 Common Issues and Solutions

### Issue: "Content script not injecting"
**Solution:** Check manifest.json permissions and content_scripts configuration

### Issue: "Popup shows 'Loading...' forever"
**Solution:** Check popup.js for async function errors

### Issue: "Context menu not appearing"
**Solution:** Verify contextMenus permission and background script

### Issue: "Icons not displaying"
**Solution:** Regenerate icons or check file paths

```bash
# Regenerate icons if needed
cd /home/mattia/Documents/GitHub/CulturalAgentAI/web_extension/icons
convert icon.svg -resize 16x16 icon-16.png
convert icon.svg -resize 32x32 icon-32.png
convert icon.svg -resize 48x48 icon-48.png
convert icon.svg -resize 128x128 icon-128.png
```

## 📊 Testing Checklist

Print this checklist and check off each item:

- [ ] Extension installs successfully
- [ ] Extension icon visible in toolbar
- [ ] Popup opens when clicking icon
- [ ] Text selection triggers floating button
- [ ] Floating button sends text successfully
- [ ] Right-click context menu works
- [ ] Keyboard shortcut (Ctrl+Shift+C) works
- [ ] Success notifications appear
- [ ] Extension icon badge appears after sending text
- [ ] Badge disappears when popup is opened
- [ ] Last selected text shows in popup
- [ ] Recent selections list updates
- [ ] Clear history button works
- [ ] Text highlighting animation works in popup
- [ ] Extension works on multiple websites
- [ ] No console errors in browser dev tools
- [ ] Extension console shows expected log messages

## 🎯 Next Steps After Testing

Once basic testing is complete:

1. **Integrate with your backend API** by modifying the `processTextWithCulturalAgent()` function
2. **Add authentication** if needed
3. **Customize styling** to match your brand
4. **Add more features** like text categorization or processing options
5. **Package for distribution** using the provided build script