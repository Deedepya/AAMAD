//
//  ContentView.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import SwiftUI

struct ContentView: View {
    @StateObject private var documentUploadViewModel = DocumentUploadViewModel()
    @State private var showDocumentCapture = false
    @State private var showDocumentReview = false
    @State private var showUploadProgress = false
    
    var body: some View {
        NavigationStack {
            TabView {
                // Home Tab
                homeView
                    .tabItem {
                        Label("Home", systemImage: "house.fill")
                    }
                
                // Documents Tab
                documentsView
                    .tabItem {
                        Label("Documents", systemImage: "doc.fill")
                    }
                
                // Profile Tab (Stub)
                profileView
                    .tabItem {
                        Label("Profile", systemImage: "person.fill")
                    }
            }
        }
        .sheet(isPresented: $showDocumentCapture) {
            DocumentCaptureView(viewModel: documentUploadViewModel)
                .onChange(of: documentUploadViewModel.capturedImage) { image in
                    if image != nil {
                        showDocumentCapture = false
                        showDocumentReview = true
                    }
                }
        }
        .sheet(isPresented: $showDocumentReview) {
            NavigationStack {
                DocumentReviewView(viewModel: documentUploadViewModel)
                    .onChange(of: documentUploadViewModel.uploadStatus) { status in
                        if status == .uploading {
                            showDocumentReview = false
                            showUploadProgress = true
                        }
                    }
            }
        }
        .sheet(isPresented: $showUploadProgress) {
            NavigationStack {
                DocumentUploadProgressView(viewModel: documentUploadViewModel)
            }
        }
    }
    
    // MARK: - Home View
    
    private var homeView: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Welcome section
                welcomeSection
                
                // Quick actions
                quickActionsSection
                
                // Progress summary (placeholder)
                progressSummarySection
            }
            .padding()
        }
        .navigationTitle("Onboarding")
    }
    
    private var welcomeSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Welcome!")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Complete your onboarding tasks to get started")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
    
    private var quickActionsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Quick Actions")
                .font(.headline)
            
            Button(action: {
                showDocumentCapture = true
            }) {
                HStack {
                    Image(systemName: "camera.fill")
                        .font(.title2)
                    VStack(alignment: .leading) {
                        Text("Upload Document")
                            .font(.body)
                            .fontWeight(.semibold)
                        Text("I-9, W-4, ID, etc.")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    Spacer()
                    Image(systemName: "chevron.right")
                        .foregroundColor(.secondary)
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(12)
            }
            .buttonStyle(PlainButtonStyle())
        }
    }
    
    private var progressSummarySection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Progress")
                .font(.headline)
            
            VStack(spacing: 8) {
                HStack {
                    Text("Overall Progress")
                        .font(.subheadline)
                    Spacer()
                    Text("0%")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                }
                
                ProgressView(value: 0.0)
                    .progressViewStyle(LinearProgressViewStyle())
                
                Text("0 of 0 tasks completed")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)
        }
    }
    
    // MARK: - Documents View
    
    private var documentsView: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 16) {
                    if documentUploadViewModel.uploadedDocument == nil {
                        emptyDocumentsView
                    } else {
                        documentListView
                    }
                }
                .padding()
            }
            .navigationTitle("Documents")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showDocumentCapture = true
                    }) {
                        Image(systemName: "plus")
                    }
                }
            }
        }
    }
    
    private var emptyDocumentsView: some View {
        VStack(spacing: 16) {
            Image(systemName: "doc.text.fill")
                .font(.system(size: 60))
                .foregroundColor(.secondary)
            
            Text("No Documents")
                .font(.headline)
            
            Text("Upload your first document to get started")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            Button(action: {
                showDocumentCapture = true
            }) {
                Text("Upload Document")
                    .font(.body)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(12)
            }
        }
        .padding()
    }
    
    private var documentListView: some View {
        VStack(spacing: 12) {
            if let document = documentUploadViewModel.uploadedDocument {
                DocumentRowView(document: document)
            }
        }
    }
    
    // MARK: - Profile View (Stub)
    
    private var profileView: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Image(systemName: "person.circle.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.secondary)
                
                Text("Profile")
                    .font(.title2)
                    .fontWeight(.semibold)
                
                Text("Profile management coming in Phase 2")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding()
            .navigationTitle("Profile")
        }
    }
}

// MARK: - Document Row View

struct DocumentRowView: View {
    let document: Document
    
    var body: some View {
        HStack {
            Image(systemName: iconForDocumentType(document.documentType))
                .font(.title2)
                .foregroundColor(.blue)
                .frame(width: 44, height: 44)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(document.documentType.rawValue)
                    .font(.body)
                    .fontWeight(.medium)
                
                Text(document.status.rawValue.capitalized)
                    .font(.caption)
                    .foregroundColor(colorForStatus(document.status))
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    private func iconForDocumentType(_ type: DocumentType) -> String {
        switch type {
        case .i9, .w4:
            return "doc.text.fill"
        case .driversLicense:
            return "creditcard.fill"
        case .passport:
            return "book.fill"
        case .socialSecurityCard:
            return "person.text.rectangle.fill"
        }
    }
    
    private func colorForStatus(_ status: DocumentStatus) -> Color {
        switch status {
        case .verified:
            return .green
        case .processing:
            return .blue
        case .rejected, .error:
            return .red
        case .pending, .uploading:
            return .orange
        }
    }
}

// MARK: - Preview

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
