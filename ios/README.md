# iOS Application - Automated Employee Onboarding Workflow

## Overview
Native iOS application for new hires to complete onboarding tasks, upload documents, and track progress.

## Technology Stack
- **Framework:** SwiftUI
- **Minimum iOS:** iOS 16+
- **Language:** Swift 5.9+
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

1. **Open Project:**
   - Open `OnboardingApp.xcodeproj` in Xcode (to be created by @frontend.eng)

2. **Install Dependencies:**
   - Dependencies will be managed via Swift Package Manager or CocoaPods
   - See implementation phase for specific dependencies

3. **Configure API Endpoint:**
   - Set API base URL in `APIService.swift`
   - Configure authentication tokens

4. **Build and Run:**
   - Select target device/simulator
   - Build and run (Cmd+R)

## Key Features (MVP)
- Document upload with camera capture
- Real-time progress tracking
- Task completion interface
- Push notifications

## Reference
- SAD: `project-context/1.define/sad.md` Section 6 (Frontend Architecture)

