# GPT4All Setup Guide

## 🚀 Quick Start

### 1. Install GPT4All
- Download GPT4All from: https://gpt4all.io/
- Install and launch the application

### 2. Enable API Server
1. Open GPT4All application
2. Go to **Settings** (gear icon)
3. Click on **API Server** tab
4. Enable **"Start API Server"**
5. Set **Port** to `4891`
6. Click **"Start Server"**

### 3. Verify Connection
The Valheim Modlist Builder will automatically detect if the server is running.

## 🔧 Troubleshooting

### Server Not Starting
- **Check if port 4891 is in use:**
  ```bash
  netstat -an | findstr :4891
  ```
- **Try a different port** (e.g., 4890, 4892)
- **Restart GPT4All** application

### Connection Refused
- **Firewall issues:** Allow GPT4All through Windows Firewall
- **Antivirus blocking:** Add GPT4All to antivirus exceptions
- **Port conflicts:** Change port in GPT4All settings

### API Not Responding
- **Check server status** in GPT4All settings
- **Restart the API server** in GPT4All
- **Verify model is loaded** in GPT4All

## 📋 Manual Test

Test the API manually:
```bash
curl -X GET http://localhost:4891/v1/models
```

Expected response:
```json
{
  "data": [
    {
      "id": "Phi-3 Mini Instruct",
      "object": "model"
    }
  ]
}
```

## 🎯 Features Without GPT4All

The Valheim Modlist Builder works perfectly without GPT4All:
- ✅ Mod categorization and management
- ✅ Zip file analysis
- ✅ Auto-categorization based on keywords
- ✅ Export functionality
- ❌ AI-enhanced summaries
- ❌ AI category suggestions

## 🔄 Alternative Ports

If port 4891 doesn't work, you can modify the application to use a different port:

1. Edit `valheim_modlist_builder.py`
2. Change line: `self.base_url = "http://localhost:4891/v1"`
3. Replace `4891` with your preferred port

## 📞 Support

If you continue having issues:
1. Check GPT4All logs in the application
2. Try restarting both GPT4All and the Valheim Modlist Builder
3. Ensure no other applications are using the same port 