# Xcode Manual Setup Guide

## Step-by-Step Instructions

### Step 1: Create New Xcode Project

1. **Open Xcode**
2. **File > New > Project** (or `Cmd+Shift+N`)
3. **Select Template:**
   - Choose **iOS** tab
   - Select **App**
   - Click **Next**

4. **Configure Project:**
   - **Product Name:** `OnboardingApp`
   - **Team:** Select your team (or leave None)
   - **Organization Identifier:** `com.aamad` (or your own)
   - **Bundle Identifier:** Will auto-fill as `com.aamad.OnboardingApp`
   - **Interface:** **SwiftUI**
   - **Language:** **Swift**
   - **Storage:** Choose "None" (we'll use our own structure)
   - **Include Tests:** ✅ **Check this box**
   - Click **Next**

5. **Choose Location:**
   - Navigate to: `/Users/dedeepyareddysalla/Documents/Developer/AgenticAI/AAMAD/ios/`
   - **IMPORTANT:** Uncheck "Create Git repository" (we already have one)
   - Click **Create**

### Step 2: Remove Default Files

1. In Xcode project navigator, **delete** these files:
   - `ContentView.swift` (we have our own)
   - `OnboardingAppApp.swift` (we have `OnboardingApp.swift`)

2. **Right-click on each file > Move to Trash**

### Step 3: Add Existing Source Files

1. **Right-click on `OnboardingApp` folder** in project navigator
2. **Select "Add Files to 'OnboardingApp'..."**
3. **Navigate to:** `ios/OnboardingApp/`
4. **Select these folders:**
   - `App`
   - `Models`
   - `ViewModels`
   - `Services`
   - `Views` (even if empty for now)
   - `Utilities` (even if empty for now)

5. **IMPORTANT Settings:**
   - ✅ **Copy items if needed:** **UNCHECKED** (files are already in place)
   - ✅ **Create groups:** **CHECKED**
   - ✅ **Add to targets:** **OnboardingApp** should be checked
   - Click **Add**

### Step 4: Add Test Files

1. **Right-click on `OnboardingAppTests` folder** in project navigator
2. **Select "Add Files to 'OnboardingApp'..."**
3. **Navigate to:** `ios/OnboardingAppTests/`
4. **Select all test files:**
   - `DocumentModelTests.swift`
   - `DocumentServiceTests.swift`
   - `DocumentUploadViewModelTests.swift`
   - `OnboardingAppTests.swift`

5. **Settings:**
   - ✅ **Copy items if needed:** **UNCHECKED**
   - ✅ **Create groups:** **CHECKED**
   - ✅ **Add to targets:** **OnboardingAppTests** should be checked
   - Click **Add**

### Step 5: Configure Project Settings

1. **Select `OnboardingApp` project** in navigator (top blue icon)
2. **Select `OnboardingApp` target** (under TARGETS)
3. **General Tab:**
   - **Minimum Deployments:** iOS 16.0
   - **Supported Destinations:** iPhone, iPad

4. **Build Settings Tab:**
   - Search for "Swift Language Version"
   - Set to **Swift 5.7** (compatible with Xcode 14.3)

5. **Info Tab:**
   - **Replace Info.plist** with the one from `ios/Info.plist`
   - Or manually add these keys:
     - `NSCameraUsageDescription`: "We need access to your camera to capture documents for onboarding."
     - `NSPhotoLibraryUsageDescription`: "We need access to your photo library to select documents for onboarding."

### Step 6: Configure Test Target

1. **Select `OnboardingAppTests` target**
2. **General Tab:**
   - **Minimum Deployments:** iOS 16.0
3. **Build Settings Tab:**
   - **Swift Language Version:** Swift 5.7 (compatible with Xcode 14.3)

### Step 7: Build and Test

1. **Select a Simulator** (e.g., iPhone 15)
2. **Build:** `Cmd+B`
3. **Run Tests:** `Cmd+U`

### Step 8: Verify Tests Pass

1. **Open Test Navigator:** `Cmd+6`
2. **You should see:**
   - DocumentModelTests (5 tests)
   - DocumentServiceTests (7 tests)
   - DocumentUploadViewModelTests (8 tests)
3. **Run all tests:** `Cmd+U`
4. **All 20 tests should pass** ✅

## Troubleshooting

### Issue: "Cannot find 'Document' in scope"
**Solution:** 
- Check that files are added to the correct target
- Select file > File Inspector > Target Membership > Ensure "OnboardingApp" is checked

### Issue: Tests not found
**Solution:**
- Ensure test files are added to "OnboardingAppTests" target
- Clean build folder: `Cmd+Shift+K`
- Build again: `Cmd+B`

### Issue: Import errors
**Solution:**
- Ensure `@testable import OnboardingApp` is in test files
- Check that source files are in the main target

## Quick Verification Checklist

- [ ] Project created with SwiftUI
- [ ] Default files removed
- [ ] Source files added (App, Models, ViewModels, Services)
- [ ] Test files added to test target
- [ ] iOS 16.0 minimum deployment
- [ ] Swift 5.7 language version (Xcode 14.3 compatible)
- [ ] Info.plist configured with camera permissions
- [ ] Project builds successfully (`Cmd+B`)
- [ ] All tests pass (`Cmd+U`)

## Next Steps

Once setup is complete:
1. Run tests to verify everything works
2. Build the app to check for compilation errors
3. Start implementing UI views (DocumentCaptureView, etc.)

