// swift-tools-version: 5.7
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "OnboardingApp",
    platforms: [
        .iOS(.v16)
    ],
    products: [
        .library(
            name: "OnboardingApp",
            targets: ["OnboardingApp"]
        ),
    ],
    dependencies: [
        // Add dependencies here if needed
    ],
    targets: [
        .target(
            name: "OnboardingApp",
            dependencies: [],
            path: "OnboardingApp",
            sources: [
                "App",
                "Models",
                "ViewModels",
                "Views",
                "Services",
                "Utilities"
            ]
        ),
        .testTarget(
            name: "OnboardingAppTests",
            dependencies: ["OnboardingApp"],
            path: "OnboardingAppTests"
        ),
    ]
)

