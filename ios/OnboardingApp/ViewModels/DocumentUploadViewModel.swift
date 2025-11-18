//
//  DocumentUploadViewModel.swift
//  OnboardingApp
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import UIKit
import Combine
import Foundation

/// Upload status for document upload process
enum UploadStatus {
    case idle
    case uploading
    case completed
    case failed
}

/// ViewModel for managing document upload state and operations
@MainActor
class DocumentUploadViewModel: ObservableObject {
    
    // MARK: - Published Properties
    
    @Published var capturedImage: UIImage?
    @Published var documentType: DocumentType = .i9
    @Published var uploadProgress: Double = 0.0
    @Published var uploadStatus: UploadStatus = .idle
    @Published var errorMessage: String?
    
    // MARK: - Private Properties
    
    private let documentService = DocumentService()
    private var uploadTask: Task<Void, Never>?
    
    // MARK: - Public Methods
    
    /// Validates the current document
    /// - Returns: True if document is valid, false otherwise
    func validateDocument() -> Bool {
        errorMessage = nil
        
        guard let image = capturedImage else {
            errorMessage = "Please capture an image first"
            return false
        }
        
        let validationResult = documentService.validateImage(image)
        
        if !validationResult.isValid {
            errorMessage = validationResult.error ?? "Document validation failed"
            return false
        }
        
        return true
    }
    
    /// Uploads the current document (mock implementation)
    func uploadDocument() {
        guard validateDocument() else {
            uploadStatus = .failed
            return
        }
        
        uploadStatus = .uploading
        uploadProgress = 0.0
        errorMessage = nil
        
        // Cancel any existing upload task
        uploadTask?.cancel()
        
        // Create new upload task
        uploadTask = Task {
            await performUpload()
        }
    }
    
    /// Retries the upload after a failure
    func retryUpload() {
        uploadStatus = .idle
        uploadProgress = 0.0
        errorMessage = nil
        
        uploadDocument()
    }
    
    // MARK: - Private Methods
    
    /// Performs the actual upload simulation
    private func performUpload() async {
        // Simulate upload progress
        let steps = 10
        let delay: UInt64 = 200_000_000 // 0.2 seconds per step (2 seconds total)
        
        for step in 1...steps {
            // Check if task was cancelled
            if Task.isCancelled {
                uploadStatus = .failed
                errorMessage = "Upload cancelled"
                return
            }
            
            await MainActor.run {
                uploadProgress = Double(step) / Double(steps)
            }
            
            // Simulate network delay
            try? await Task.sleep(nanoseconds: delay)
        }
        
        // Simulate success (in real implementation, this would be API call)
        await MainActor.run {
            uploadProgress = 1.0
            uploadStatus = .completed
        }
    }
}

