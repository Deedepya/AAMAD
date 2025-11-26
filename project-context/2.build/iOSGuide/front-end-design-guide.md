# Front-End Design Guide

## Plain English Explanation: Making "Feature-wise flow and connections" Modular

**Current state:** The section describes three features (Document Upload, Task List, Profile) and how they connect to the main app, but it's not organized as independent modules.

**Modular design approach:**

### 1. **Each module defines its own flow**
Each feature module should document:
- **Entry point** (how you get into this feature)
- **Internal flow** (what screens/steps happen inside)
- **Exit points** (how you leave and what data you pass back)
- **Dependencies** (what it needs from outside, like shared models or services)

### 1.1. **Think of each feature as a self-contained box**
Each feature (Document Upload, Task List, Profile) should be:
- **Independent** — works on its own without relying on other features
- **Reusable** — can be swapped or updated without breaking others
- **Self-contained** — has its own views, logic, and data handling

### 1.2. **Define clear boundaries between modules**
- Each feature module has a **public interface** (what other parts can use)
- Each feature module has **private internals** (implementation details hidden from others)
- Modules communicate through **well-defined contracts** (like passing data objects, not direct dependencies)

### 1.3. **Organize by feature, not by file type**
Instead of grouping all Views together, all ViewModels together, etc., organize like this:

```
Features/
├── DocumentUpload/          # Everything for document upload in one place
│   ├── Views/
│   ├── Models/
│   ├── Services/
│   └── Utilities/
├── TaskList/                # Everything for task list in one place
│   ├── Views/
│   ├── Models/
│   └── Services/
└── Profile/                 # Everything for profile in one place
    ├── Views/
    └── Models/
```

### 2. **Shared components live separately**
Common pieces used by multiple features (like loading spinners, error views) go in a **Shared** or **Common** folder that all features can access.

### 3. **The main app is just a coordinator**
The main app (`OnboardingApp` + `ContentView`) is responsible for:

- **Composition & bootstrapping:** Setting up the root view hierarchy, global environment, and initial dependencies when the app launches.
- **Navigation coordination:** Deciding which feature or screen to show (e.g., Documents, Tasks, Profile) and managing transitions between them based on user actions and app state.
- **Delegating feature logic:** Pushing all business logic, data handling, and UI details down into feature modules so the main app focuses on wiring things together.
- **App-wide responsibilities:** Owning cross-cutting concerns like app lifecycle hooks, global state (e.g., auth/session), and passing shared services (network, storage, analytics) into features.

**In summary:** Modular design means each feature is a self-contained unit that can be developed, tested, and maintained independently, with the main app acting as a coordinator that composes features, manages navigation, and provides shared services.

