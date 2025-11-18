//
//  ContentView.swift
//  OnboardingApp
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            Text("Progress Dashboard")
                .tabItem {
                    Label("Home", systemImage: "house")
                }
            
            Text("Document Upload")
                .tabItem {
                    Label("Documents", systemImage: "doc.text")
                }
            
            Text("Tasks")
                .tabItem {
                    Label("Tasks", systemImage: "checklist")
                }
            
            Text("Profile")
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
    }
}

#Preview {
    ContentView()
}

