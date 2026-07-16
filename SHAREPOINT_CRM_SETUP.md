# SharePoint Excel CRM Integration Setup

This guide explains how to configure the door builder to save project data to your SharePoint Online Excel CRM.

## Overview

When a user clicks "Generate Internal Quote", the system will:
1. Generate the PDF quote (internal use)
2. Save project and customer information to your SharePoint Excel CRM

The CRM will be populated with these fields:
- **Due Date** - Quote validity date (30 days from creation)
- **Next Action** - Default: "Follow up on quote"
- **Status** - Default: "Quote Generated"
- **Project Name** - From customer input or auto-generated from door specs
- **Project Value** - The calculated estimate
- **Project Stage** - Default: "Quote"
- **First Name** - Customer's first name
- **Last Name** - Customer's last name
- **Job Title** - Customer's job title
- **Phone** - Customer's phone number
- **Email address** - Customer's email
- **Organization** - Customer's company/organization

---

## Step 1: Create Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Enter:
   - Name: `Door Builder CRM Integration`
   - Supported account types: **Accounts in this organizational directory only**
   - Redirect URI: Leave blank (not needed for app-only auth)
5. Click **Register**
6. Note down the **Application (client) ID** and **Directory (tenant) ID**

## Step 2: Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Enter a description (e.g., "Door Builder Secret")
4. Select expiration (recommend 24 months)
5. Click **Add**
6. **IMPORTANT**: Copy the secret value immediately (it won't be shown again)

## Step 3: Grant API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission** → **Microsoft Graph** → **Application permissions**
3. Add these permissions:
   - `Files.ReadWrite.All` (for OneDrive/SharePoint file access)
   - `Sites.ReadWrite.All` (for SharePoint site access)
4. Click **Grant admin consent for [Your Organization]**

## Step 4: Get SharePoint File Information

You need to find the Drive ID and file path for your Excel CRM file.

### Option A: Using Graph Explorer

1. Go to [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
2. Sign in with your Microsoft account
3. To find your OneDrive drive ID:
   ```
   GET https://graph.microsoft.com/v1.0/me/drive
   ```
   Look for the `id` field in the response.

4. To find the file path, navigate to your Excel file in SharePoint/OneDrive and note the path.

### Option B: From your SharePoint URL

Your SharePoint URL:
```
https://specflow-my.sharepoint.com/:x:/r/personal/matt_specflow_tech/_layouts/15/doc2.aspx?sourcedoc=%7B5D0DA19E-9375-4A32-8AA8-92004367EF48%7D&file=Excel%20CRM%20Preferred%20Option.xlsx
```

From this:
- Site: `specflow-my.sharepoint.com`
- User folder: `personal/matt_specflow_tech`
- File name: `Excel CRM Preferred Option.xlsx`

To get the drive ID via API:
```
GET https://graph.microsoft.com/v1.0/sites/specflow-my.sharepoint.com:/personal/matt_specflow_tech
```

Then:
```
GET https://graph.microsoft.com/v1.0/sites/{site-id}/drive
```

## Step 5: Configure Environment Variables

Create a `.env` file in the project root (or set these as system environment variables):

```bash
# Azure AD Authentication
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here

# SharePoint Excel File Location
SHAREPOINT_DRIVE_ID=your-drive-id-here
SHAREPOINT_FILE_PATH=/Excel CRM Preferred Option.xlsx
SHAREPOINT_TABLE_NAME=Table1
SHAREPOINT_WORKSHEET_NAME=Sheet1
```

### For Windows (PowerShell):
```powershell
$env:AZURE_TENANT_ID = "your-tenant-id-here"
$env:AZURE_CLIENT_ID = "your-client-id-here"
$env:AZURE_CLIENT_SECRET = "your-client-secret-here"
$env:SHAREPOINT_DRIVE_ID = "your-drive-id-here"
$env:SHAREPOINT_FILE_PATH = "/Excel CRM Preferred Option.xlsx"
$env:SHAREPOINT_TABLE_NAME = "Table1"
$env:SHAREPOINT_WORKSHEET_NAME = "Sheet1"
```

### For Windows (CMD):
```cmd
set AZURE_TENANT_ID=your-tenant-id-here
set AZURE_CLIENT_ID=your-client-id-here
set AZURE_CLIENT_SECRET=your-client-secret-here
set SHAREPOINT_DRIVE_ID=your-drive-id-here
set SHAREPOINT_FILE_PATH=/Excel CRM Preferred Option.xlsx
set SHAREPOINT_TABLE_NAME=Table1
set SHAREPOINT_WORKSHEET_NAME=Sheet1
```

## Step 6: Prepare Your Excel File

Your SharePoint Excel CRM file must have these headers in the first row:

| Column | Header |
|--------|--------|
| A | Due Date |
| B | Next Action |
| C | Status |
| D | Project Name |
| E | Project Value |
| F | Project Stage |
| G | First Name |
| H | Last Name |
| I | Job Title |
| J | Phone |
| K | Email address |
| L | Organization |

### Creating an Excel Table (Recommended)

For best results, format your data as an Excel Table:
1. Open your Excel file in SharePoint/Excel Online
2. Select the header row and any existing data
3. Go to **Insert** → **Table**
4. Make sure "My table has headers" is checked
5. The table will be named "Table1" by default (you can rename it)

---

## Fallback: Local Excel

If the SharePoint integration is not configured (no `AZURE_CLIENT_ID` set), the system will automatically fall back to saving data to a local `crm_projects.xlsx` file in the project directory.

---

## Troubleshooting

### "Failed to get access token"
- Verify your tenant ID, client ID, and client secret are correct
- Check that admin consent was granted for the API permissions

### "Failed to append to Excel"
- Verify the drive ID and file path are correct
- Make sure the Excel file exists and is accessible
- Check that the table name matches (default: "Table1")

### "Azure AD credentials not configured"
- The environment variables are not set
- Restart your server after setting environment variables

---

## Security Notes

1. **Never commit secrets**: Don't add `.env` files or secrets to git
2. **Rotate secrets**: Create new client secrets before they expire
3. **Least privilege**: Only grant the minimum required permissions
4. **Monitor access**: Review Azure AD sign-in logs periodically
