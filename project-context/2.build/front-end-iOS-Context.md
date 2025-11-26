# iOS Frontend Development Plan

## Overview
This document outlines the development plan for the iOS native application component of the Automated Employee Onboarding Workflow system. This plan is based on the Product Requirements Document (PRD), System Architecture Document (SAD), and Setup documentation.

**Reference Documents:**
- PRD: `project-context/1.define/prd.md`
- SAD: `project-context/1.define/sad.md`
- Setup: `project-context/2.build/setup.md`
- Frontend Engineer Persona: `.cursor/agents/frontend-eng.md`
- Frontend design and architechture: `project-context/2.build/front-end-design-guide.md`

## Table of Contents
- [Overview](#overview)
- [1. Development Objectives](#1-development-objectives)
  - [1.1 Primary Goals](#11-primary-goals)
  - [1.2 Success Criteria](#12-success-criteria)
- [2. Technology Stack & Architecture](#2-technology-stack--architecture)
  - [2.1 Technology Stack](#21-technology-stack)
  - [2.2 Application Structure](#22-application-structure)
    - [Directory Organization (per SAD Section 6.2)](#directory-organization-per-sad-section-62)
    - [Feature-wise flow and connections](#feature-wise-flow-and-connections)
    - [Modular Folder Structure (High Level)](#modular-folder-structure-high-level)
    - [Folder structure (iOS Level)](#folder-structure)
- [3. Component Development Plan](#3-component-development-plan)


---

## 1. Development Objectives

### 1.1 Primary Goals
1. **Document Upload Experience:** Enable new hires to capture, review, and upload onboarding documents (I-9, W-4, ID, Passport)
2. **Task List Management:** Provide a clear, interactive onboarding task list with statuses and next actions
3. **User Profile Overview:** Offer a simple user profile view showing key information (name, role, contact details)

### 1.2 Success Criteria
- **User Experience:** 90%+ satisfaction, <2 hours onboarding completion time (per PRD Section 1)
- **Performance:** <100ms screen transitions, <2s API response time (per SAD Section 12.1)
- **Accessibility:** WCAG 2.1 AA compliance (per PRD Section 5)
- **Code Quality:** MVVM architecture, 70%+ test coverage target (per SAD Section 12.4)

**Out of Scope (Per MVP):**
- Backend API integration (deferred to @integration.eng)
- Functional backend connections (UI only, mock data)
- Android application (Phase 2)
- Web-based admin dashboard (Phase 2)
- Offline mode (Phase 2)

---

## 2. Technology Stack & Architecture

### 2.1 Technology Stack

**Framework & Language:**
- **SwiftUI** for declarative UI development (per SAD Section 6.1)
- **Swift 5.9+** for modern language features
- **iOS 16+** minimum deployment target
- **Combine** for reactive data flow
- **Async/Await** for asynchronous operations (including future network calls)

**Dependencies:**
- **Alamofire** or native `URLSession` for API communication (to be decided)
- **SwiftUI NavigationStack** for navigation
- **KeychainSwift** or native Keychain for secure storage
- **Camera/CameraUI** for document capture

### 2.2 Application Structure

#### Directory Organization (per SAD Section 6.2)

##### Feature-wise flow and connections
- Main app composition (`OnboardingApp` + `ContentView`) defines the root navigation container with a tab-based layout (e.g., Home/Progress, Documents, Tasks, Profile)
- **Document Upload Experience**
  - User selects the **Documents** tab/entry point from the main app shell
  - Navigation stack presents the document upload screens in order (document type selection → capture → review → upload progress)
  - Each screen passes the necessary document information forward to the next step in the flow
- **Task List Management**
  - From `ContentView`, user selects the **Tasks** tab/entry point
  - Tasks screen shows a list of onboarding tasks with status indicators and basic actions (e.g., view details)
  - Navigating into a task detail screen shows more information and possible next steps
- **User Profile Overview**
  - From `ContentView`, user selects the **Profile** tab/entry point
  - Profile screen displays key user information (name, role, contact details) and placeholders for future settings

#### Modular Folder Structure (High Level)

Modular layout:

```
ios/OnboardingApp/
├── App/                       # App composition / coordinator
│   ├── OnboardingApp.swift
│   └── ContentView.swift
│
├── Features/                  # Feature modules
│   ├── DocumentUpload/        # Everything for document upload in one place
│   │   ├── Views/
│   │   ├── Models/
│   │   ├── Services/
│   │   └── Utilities/
│   ├── TaskList/              # Everything for task list in one place
│   │   ├── Views/
│   │   ├── Models/
│   │   └── Services/
│   └── Profile/               # Everything for profile in one place
│       ├── Views/
│       └── Models/
│
└── Shared/                    # Cross-feature code
    ├── Components/            # Reusable UI components
    ├── Services/              # Shared services (API, Keychain, etc.)
    └── Utilities/             # Shared helpers (network, image processing, constants)
```

#### Folder structure (iOS Level)

```
ios/OnboardingApp/
├── App/                              # App composition / coordinator
│   ├── OnboardingApp.swift          # App entry point
│   └── ContentView.swift             # Root view with TabView
│
├── Features/                         # Feature modules
│   ├── DocumentUpload/               # Document upload feature module
│   │   ├── Views/
│   │   │   ├── DocumentCaptureView.swift
│   │   │   ├── DocumentReviewView.swift
│   │   │   └── DocumentUploadProgressView.swift
│   │   ├── Models/
│   │   │   └── Document.swift
│   │   ├── Services/
│   │   │   └── DocumentService.swift
│   │   └── Utilities/
│   │       └── DocumentProcessor.swift
│   │
│   ├── TaskList/                     # Task list feature module
│   │   ├── Views/
│   │   │   ├── TaskListView.swift
│   │   │   └── TaskDetailView.swift
│   │   ├── Models/
│   │   │   └── OnboardingTask.swift
│   │   └── Services/
│   │       └── TaskService.swift
│   │
│   └── Profile/                      # User profile feature module
│       ├── Views/
│       │   └── ProfileView.swift
│       └── Models/
│           └── User.swift
│
└── Shared/                           # Cross-feature code
    ├── Components/                   # Reusable UI components
    │   ├── LoadingView.swift
    │   ├── ErrorView.swift
    │   ├── StatusBadge.swift
    │   └── EmptyStateView.swift
    ├── Services/                     # Shared services
    │   ├── APIService.swift
    │   ├── KeychainService.swift
    │   └── NotificationService.swift
    └── Utilities/                    # Shared utilities
        ├── KeychainManager.swift
        ├── NetworkManager.swift
        ├── ImageProcessor.swift
        └── Constants.swift
```

---

## 3. Component Development Plan

### 3.1 Features/DocumentUpload Module

#### 3.1.1 Views

**DocumentCaptureView.swift**
- **Purpose:** Native iOS camera interface for document capture
- **Features:**
  - Camera permission handling
  - Document type selection (I-9, W-4, ID, Passport)
  - Real-time camera preview
  - Capture button with haptic feedback
  - Flash toggle
  - Image quality validation (minimum resolution, file size)
- **UI Requirements:**
  - Full-screen camera interface
  - Overlay guides for document alignment
  - Clear instructions for document positioning
- **State Management:** Manages document capture state
- **Dependencies:** `AVFoundation` for camera, `UIKit` for camera UI

**DocumentReviewView.swift**
- **Purpose:** Preview captured document before upload
- **Features:**
  - Document image preview with zoom capability
  - Document type confirmation
  - Retake option
  - Upload confirmation button
  - Image metadata display (size, resolution)
- **UI Requirements:**
  - Scrollable image view
  - Action buttons (Retake, Upload, Cancel)
  - Loading state during upload preparation
- **State Management:** Receives document from `DocumentCaptureView`, manages document state

**DocumentUploadProgressView.swift**
- **Purpose:** Display upload progress and status
- **Features:**
  - Progress bar with percentage
  - Upload status messages
  - Success/error state handling
  - Auto-navigation on completion
- **UI Requirements:**
  - Circular or linear progress indicator
  - Status text updates
  - Error retry button

#### 3.1.2 Models

**Document.swift**
- **Purpose:** Document data model
- **Properties:**
  - Document ID, type, status
  - File metadata (size, resolution, format)
  - Upload timestamp and status

#### 3.1.3 Services

**DocumentService.swift**
- **Purpose:** Document handling and processing
- **Features:**
  - Image compression
  - Image format conversion
  - Document metadata extraction
  - File size validation
- **Methods:**
  - `compressImage(_:maxSize:)`
  - `validateImage(_:)`
  - `extractMetadata(_:)`

#### 3.1.4 Utilities

**DocumentProcessor.swift**
- **Purpose:** Document processing utilities
- **Features:**
  - Image quality validation
  - Document type validation
  - Format conversion utilities

### 3.2 Features/TaskList Module

#### 3.2.1 Views

**ProgressDashboardView.swift**
- **Purpose:** Main dashboard showing overall onboarding progress
- **Features:**
  - Overall progress percentage
  - Task completion count (e.g., "3 of 5 tasks completed")
  - Compliance status summary
  - Next action recommendations
  - Pull-to-refresh for status updates
- **UI Requirements:**
  - Large progress circle or bar
  - Task summary cards
  - Status badges (color-coded)
  - Navigation to task list
- **State Management:** `ProgressTrackingViewModel` with Combine publishers

**TaskListView.swift**
- **Purpose:** Detailed list of all onboarding tasks
- **Features:**
  - Task name and description
  - Status badges (pending, in-progress, completed, error)
  - Due date display
  - Task action buttons (Start, Complete, View Details)
  - Filtering by status
  - Sorting by due date or priority
- **UI Requirements:**
  - SwiftUI `List` with custom row views
  - Swipe actions for quick actions
  - Empty state when no tasks
- **State Management:** Manages task list state

**TaskDetailView.swift**
- **Purpose:** Detailed view of a single task
- **Features:**
  - Task information display
  - Task actions (complete, start, view related documents)
  - Related task navigation

#### 3.2.2 Models

**OnboardingTask.swift**
- **Purpose:** Task data model
- **Properties:**
  - Task ID, name, description
  - Status, due date, priority
  - Related documents and dependencies

#### 3.2.3 Services

**TaskService.swift**
- **Purpose:** Task management service
- **Features:**
  - Task fetching and updates
  - Task status management
  - Task filtering and sorting logic

### 3.3 Features/Profile Module

#### 3.3.1 Views

**ProfileView.swift**
- **Purpose:** User profile display (stub for MVP)
- **Features:**
  - User name and email display
  - Profile picture placeholder
  - Settings button (non-functional)
- **Note:** Full profile management deferred to Phase 2

#### 3.3.2 Models

**User.swift**
- **Purpose:** User profile data model
- **Properties:**
  - User ID, name, email, role
  - Contact details
  - Profile picture URL

### 3.4 Shared Components

#### 3.4.1 Shared/Components

**LoadingView.swift**
- **Purpose:** Reusable loading indicator
- **Features:**
  - Spinner animation
  - Optional loading message
  - Full-screen or inline variants

**ErrorView.swift**
- **Purpose:** Error display with retry option
- **Features:**
  - Error message display
  - Retry button
  - Dismiss option
  - Error icon

**StatusBadge.swift**
- **Purpose:** Color-coded status indicator
- **Features:**
  - Status text (Pending, In Progress, Completed, Error)
  - Color coding (gray, blue, green, red)
  - Icon support

**EmptyStateView.swift**
- **Purpose:** Placeholder for empty states
- **Features:**
  - Icon or illustration
  - Message text
  - Optional action button

#### 3.4.2 Shared/Services

**APIService.swift**
- **Purpose:** API client with mock implementations
- **Implementation:**
  - Define API endpoint structure
  - Create request/response models
  - Implement mock responses with delay simulation
  - Error simulation for testing
- **Methods (Mock):**
  - `uploadDocument(_:completion:)` - Returns success after 2-second delay
  - `fetchOnboardingStatus(userId:completion:)` - Returns mock status data
  - `fetchTasks(userId:completion:)` - Returns mock task list
  - `completeTask(taskId:completion:)` - Returns success after 1-second delay
- **Note:** Real API integration deferred to @integration.eng

**KeychainService.swift**
- **Purpose:** Secure storage for authentication tokens
- **Features:**
  - Token storage/retrieval
  - Token deletion
  - Secure key management
- **Implementation:**
  - Use iOS Keychain APIs
  - Encrypt sensitive data
  - Handle keychain errors gracefully

**NotificationService.swift**
- **Purpose:** Push notification handling
- **Features:**
  - APNs registration (stub)
  - Notification permission request
  - Local notification scheduling (for testing)
- **Note:** Full APNs integration deferred to @integration.eng

#### 3.4.3 Shared/Utilities

**KeychainManager.swift**
- **Purpose:** Keychain wrapper for secure storage
- **Features:**
  - Generic save/load/delete methods
  - Error handling
  - Key management

**NetworkManager.swift**
- **Purpose:** Network configuration and utilities
- **Features:**
  - Base URL configuration
  - Request timeout settings
  - Network reachability (optional)
  - SSL pinning configuration (stub)

**ImageProcessor.swift**
- **Purpose:** Image processing utilities
- **Features:**
  - Image resizing
  - Image compression
  - Format conversion
  - Quality optimization

**Constants.swift**
- **Purpose:** App-wide constants
- **Contents:**
  - API endpoints (placeholder URLs)
  - UI constants (colors, spacing, fonts)
  - Document type definitions
  - Task status definitions

---

