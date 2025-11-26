//
//  DocumentUploadProgressView.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import SwiftUI

/// View for displaying document upload progress
struct DocumentUploadProgressView: View {
    @ObservedObject var viewModel: DocumentUploadViewModel
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            
            // Progress indicator
            progressIndicatorView
            
            // Status message
            statusMessageView
            
            // Error handling
            if viewModel.uploadStatus == .error {
                errorView
            }
            
            Spacer()
            
            // Action buttons
            actionButtonsView
        }
        .padding()
        .navigationTitle("Uploading Document")
        .navigationBarTitleDisplayMode(.inline)
        .onChange(of: viewModel.uploadStatus) { newStatus in
            if newStatus == .success {
                // Auto-dismiss after a short delay
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                    dismiss()
                }
            }
        }
    }
    
    // MARK: - Progress Indicator
    
    private var progressIndicatorView: some View {
        VStack(spacing: 16) {
            if viewModel.uploadStatus == .uploading {
                // Circular progress indicator
                ZStack {
                    Circle()
                        .stroke(Color(.systemGray5), lineWidth: 8)
                        .frame(width: 120, height: 120)
                    
                    Circle()
                        .trim(from: 0, to: viewModel.uploadProgress)
                        .stroke(Color.blue, style: StrokeStyle(lineWidth: 8, lineCap: .round))
                        .frame(width: 120, height: 120)
                        .rotationEffect(.degrees(-90))
                        .animation(.linear, value: viewModel.uploadProgress)
                    
                    Text("\(Int(viewModel.uploadProgress * 100))%")
                        .font(.title2)
                        .fontWeight(.semibold)
                }
            } else if viewModel.uploadStatus == .success {
                // Success indicator
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.green)
            } else if viewModel.uploadStatus == .error {
                // Error indicator
                Image(systemName: "xmark.circle.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.red)
            } else {
                // Idle state
                Image(systemName: "doc.text.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.blue)
            }
        }
    }
    
    // MARK: - Status Message
    
    private var statusMessageView: some View {
        VStack(spacing: 8) {
            Text(statusTitle)
                .font(.title2)
                .fontWeight(.semibold)
            
            Text(statusMessage)
                .font(.body)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
    }
    
    private var statusTitle: String {
        switch viewModel.uploadStatus {
        case .idle:
            return "Ready to Upload"
        case .uploading:
            return "Uploading..."
        case .success:
            return "Upload Complete"
        case .error:
            return "Upload Failed"
        }
    }
    
    private var statusMessage: String {
        switch viewModel.uploadStatus {
        case .idle:
            return "Tap upload to begin"
        case .uploading:
            return "Please wait while we upload your document"
        case .success:
            return "Your document has been successfully uploaded and is being processed"
        case .error:
            return viewModel.errorMessage ?? "An error occurred during upload"
        }
    }
    
    // MARK: - Error View
    
    private var errorView: some View {
        VStack(spacing: 12) {
            if let errorMessage = viewModel.errorMessage {
                Text(errorMessage)
                    .font(.subheadline)
                    .foregroundColor(.red)
                    .multilineTextAlignment(.center)
                    .padding()
                    .background(Color.red.opacity(0.1))
                    .cornerRadius(12)
            }
            
            Button(action: {
                Task {
                    await viewModel.uploadDocument()
                }
            }) {
                HStack {
                    Image(systemName: "arrow.clockwise")
                    Text("Retry Upload")
                }
                .font(.body)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .cornerRadius(12)
            }
        }
    }
    
    // MARK: - Action Buttons
    
    private var actionButtonsView: some View {
        VStack(spacing: 12) {
            if viewModel.uploadStatus == .success {
                Button(action: {
                    viewModel.reset()
                    dismiss()
                }) {
                    Text("Done")
                        .font(.body)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(12)
                }
            } else if viewModel.uploadStatus == .error {
                Button(action: {
                    dismiss()
                }) {
                    Text("Cancel")
                        .font(.body)
                        .foregroundColor(.blue)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                }
            }
        }
    }
}

// MARK: - Preview

struct DocumentUploadProgressView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            DocumentUploadProgressView(viewModel: DocumentUploadViewModel())
        }
    }
}

