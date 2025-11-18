# iOS Application - Automated Employee Onboarding Workflow

## Overview
Native iOS application for new hires to complete onboarding tasks, upload documents, and track progress.

## Technology Stack
- **Framework:** SwiftUI
- **Minimum iOS:** iOS 16+
- **Language:** Swift 5.7+ (compatible with Xcode 14.3)
- **Architecture:** MVVM with Combine

## Project Structure
```
OnboardingApp/
├── App/
│   ├── OnboardingApp.swift    # App entry point
│   └── ContentView.swift      # Root view
├── Models/                    # Data models
├── ViewModels/                # ViewModels (MVVM)
├── Views/
│   ├── DocumentUpload/        # Document upload views
│   ├── Progress/              # Progress tracking views
│   └── Common/                # Shared UI components
├── Services/                  # API and business logic
└── Utilities/                 # Helper utilities
```

## Setup Instructions

### Option 1: Using XcodeGen (Recommended)

1. **Install XcodeGen:**
   ```bash
   brew install xcodegen
   ```

2. **Generate Xcode Project:**
   ```bash
   cd ios
   xcodegen generate
   ```

3. **Open Project:**
   - Open `OnboardingApp.xcodeproj` in Xcode

### Option 2: Manual Xcode Project Creation

1. **Create New Project in Xcode:**
   - Open Xcode
   - File > New > Project
   - Choose iOS > App
   - Name: `OnboardingApp`
   - Interface: SwiftUI
   - Language: Swift
   - Minimum iOS: 16.0

2. **Add Existing Files:**
   - Delete the default ContentView.swift and OnboardingApp.swift
   - Right-click on project > Add Files to "OnboardingApp"
   - Select all folders: `App`, `Models`, `ViewModels`, `Services`, `Views`, `Utilities`
   - Ensure "Copy items if needed" is unchecked
   - Ensure "Create groups" is selected

3. **Add Test Target:**
   - File > New > Target
   - Choose iOS > Unit Testing Bundle
   - Name: `OnboardingAppTests`
   - Add existing test files from `OnboardingAppTests` folder

4. **Configure Info.plist:**
   - Replace the default Info.plist with the one in the project root
   - Or add camera/photo library usage descriptions manually

5. **Build and Run:**
   - Select target device/simulator
   - Build and run (Cmd+R)

### Running Tests

1. **Run All Tests:**
   - Cmd+U to run all tests
   - Or Product > Test

2. **Run Specific Test:**
   - Click the diamond icon next to test method
   - Or right-click > Run

### Test Coverage

The project includes comprehensive tests for:
- Document model and types
- DocumentService (image processing, validation)
- DocumentUploadViewModel (state management, upload flow)

All tests follow TDD principles and should pass with the current implementation.

## Key Features (MVP)
- Document upload with camera capture
- Real-time progress tracking
- Task completion interface
- Push notifications

## Reference
- SAD: `project-context/1.define/sad.md` Section 6 (Frontend Architecture)

