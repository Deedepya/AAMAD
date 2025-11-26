//
//  DocumentReviewView.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import SwiftUI

/// View for reviewing captured document before upload
struct DocumentReviewView: View {
    @Binding var capturedImage: UIImage?
    @Binding var selectedDocumentType: DocumentType?
    var onRetake: () -> Void
    var onUpload: () -> Void
    
    @Environment(\.dismiss) var dismiss
    @State private var scale: CGFloat = 1.0
    @State private var lastScale: CGFloat = 1.0
    @State private var offset: CGSize = .zero
    @State private var lastOffset: CGSize = .zero
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            ZStack {
                Color(.systemBackground)
                    .ignoresSafeArea()
                
                VStack(spacing: 20) {
                    // Document preview with zoom
                    documentPreviewView
                    
                    // Document type confirmation
                    documentTypeConfirmationView
                    
                    // Image metadata
                    imageMetadataView
                    
                    // Action buttons
                    actionButtonsView
                }
                .padding()
            }
            .navigationTitle("Review Document")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
    
    // MARK: - Document Preview
    
    private var documentPreviewView: some View {
        ScrollView([.horizontal, .vertical]) {
            if let image = capturedImage {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .scaleEffect(scale)
                    .offset(offset)
                    .frame(maxWidth: .infinity, maxHeight: 400)
                    .gesture(
                        MagnificationGesture()
                            .onChanged { value in
                                let delta = value / lastScale
                                lastScale = value
                                scale = min(max(scale * delta, 1.0), 4.0)
                            }
                            .onEnded { _ in
                                lastScale = 1.0
                            }
                    )
                    .gesture(
                        DragGesture()
                            .onChanged { value in
                                offset = CGSize(
                                    width: lastOffset.width + value.translation.width,
                                    height: lastOffset.height + value.translation.height
                                )
                            }
                            .onEnded { _ in
                                lastOffset = offset
                            }
                    )
            } else {
                Text("No image captured")
                    .foregroundColor(.secondary)
                    .frame(height: 400)
            }
        }
        .frame(height: 400)
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    // MARK: - Document Type Confirmation
    
    private var documentTypeConfirmationView: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Document Type")
                .font(.caption)
                .foregroundColor(.secondary)
            
            if let documentType = selectedDocumentType {
                HStack {
                    Image(systemName: iconForDocumentType(documentType))
                        .foregroundColor(.blue)
                    Text(documentType.rawValue)
                        .font(.body)
                        .fontWeight(.medium)
                    Spacer()
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(12)
            }
        }
    }
    
    // MARK: - Image Metadata
    
    private var imageMetadataView: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Image Details")
                .font(.caption)
                .foregroundColor(.secondary)
            
            if let image = capturedImage {
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Label("Resolution", systemImage: "photo")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Text("\(Int(image.size.width)) × \(Int(image.size.height))")
                            .font(.subheadline)
                            .fontWeight(.medium)
                    }
                    
                    Spacer()
                    
                    VStack(alignment: .trailing, spacing: 4) {
                        Label("Size", systemImage: "doc")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Text(formatFileSize(estimateFileSize(image)))
                            .font(.subheadline)
                            .fontWeight(.medium)
                    }
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(12)
            }
        }
    }
    
    // MARK: - Action Buttons
    
    private var actionButtonsView: some View {
        VStack(spacing: 12) {
            Button(action: {
                isLoading = true
                onUpload()
            }) {
                HStack {
                    if isLoading {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    } else {
                        Image(systemName: "arrow.up.circle.fill")
                    }
                    Text("Upload Document")
                }
                .font(.body)
                .fontWeight(.semibold)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .cornerRadius(12)
            }
            .disabled(isLoading || capturedImage == nil || selectedDocumentType == nil)
            
            Button(action: {
                onRetake()
                dismiss()
            }) {
                HStack {
                    Image(systemName: "camera.fill")
                    Text("Retake")
                }
                .font(.body)
                .foregroundColor(.blue)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(12)
            }
        }
    }
    
    // MARK: - Helper Methods
    
    private func iconForDocumentType(_ type: DocumentType) -> String {
        switch type {
        case .i9:
            return "doc.text.fill"
        case .w4:
            return "doc.text.fill"
        case .driversLicense:
            return "creditcard.fill"
        case .passport:
            return "book.fill"
        case .socialSecurityCard:
            return "person.text.rectangle.fill"
        }
    }
    
    private func estimateFileSize(_ image: UIImage) -> Int {
        // Rough estimate: width * height * 4 bytes (RGBA)
        return Int(image.size.width * image.size.height * 4)
    }
    
    private func formatFileSize(_ bytes: Int) -> String {
        let formatter = ByteCountFormatter()
        formatter.allowedUnits = [.useKB, .useMB]
        formatter.countStyle = .file
        return formatter.string(fromByteCount: Int64(bytes))
    }
}

// MARK: - Preview

struct DocumentReviewView_Previews: PreviewProvider {
    static var previews: some View {
        DocumentReviewView(
            capturedImage: .constant(UIImage(systemName: "doc.text.fill")),
            selectedDocumentType: .constant(.i9),
            onRetake: {},
            onUpload: {}
        )
    }
}
