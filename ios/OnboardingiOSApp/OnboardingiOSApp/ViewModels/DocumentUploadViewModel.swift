//
//  DocumentUploadViewModel.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import Foundation
import UIKit
import Combine

/// Upload status enumeration
enum UploadStatus {
    case idle
    case uploading
    case success
    case error
}

/// Document upload view model following MVVM pattern
@MainActor
class DocumentUploadViewModel: ObservableObject {
    
    // MARK: - Published Properties
    
    @Published var selectedDocumentType: DocumentType?
    @Published var capturedImage: UIImage?
    @Published var uploadStatus: UploadStatus = .idle
    @Published var uploadProgress: Double = 0.0
    @Published var errorMessage: String?
    @Published var uploadedDocument: Document?
    
    // MARK: - Private Properties
    
    private let documentService: DocumentServiceProtocol
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - Initialization
    
    init(documentService: DocumentServiceProtocol = DocumentService()) {
        self.documentService = documentService
    }
    
    // MARK: - Public Methods
    
    /// Selects a document type (nil to clear selection)
    func selectDocumentType(_ type: DocumentType?) {
        selectedDocumentType = type
        errorMessage = nil
    }
    
    /// Captures an image from the camera
    func captureImage(_ image: UIImage) {
        capturedImage = image
        errorMessage = nil
    }
    
    /// Retakes the image (clears current capture)
    func retakeImage() {
        capturedImage = nil
        errorMessage = nil
    }
    
    /// Uploads the captured document
    func uploadDocument() async {
        guard let image = capturedImage,
              let documentType = selectedDocumentType else {
            await MainActor.run {
                errorMessage = "Please select a document type and capture an image"
            }
            return
        }
        
        // Validate image
        guard validateImage(image) else {
            await MainActor.run {
                errorMessage = "Image resolution is too low. Please capture a higher quality image."
                uploadStatus = .error
            }
            return
        }
        
        // Validate file size
        guard validateFileSize(image) else {
            await MainActor.run {
                errorMessage = "Image file size is too large. Please try again."
                uploadStatus = .error
            }
            return
        }
        
        await MainActor.run {
            uploadStatus = .uploading
            uploadProgress = 0.0
            errorMessage = nil
        }
        
        do {
            let document = try await documentService.uploadDocument(
                image,
                documentType: documentType
            ) { [weak self] progress in
                Task { @MainActor in
                    self?.uploadProgress = progress
                }
            }
            
            await MainActor.run {
                uploadedDocument = document
                uploadStatus = .success
                uploadProgress = 1.0
            }
        } catch {
            await MainActor.run {
                errorMessage = error.localizedDescription
                uploadStatus = .error
                uploadProgress = 0.0
            }
        }
    }
    
    /// Validates image resolution
    func validateImage(_ image: UIImage) -> Bool {
        let minResolution = CGSize(width: 800, height: 600)
        return image.size.width >= minResolution.width &&
               image.size.height >= minResolution.height
    }
    
    /// Validates file size (approximate)
    func validateFileSize(_ image: UIImage) -> Bool {
        // Estimate file size from image dimensions
        // This is an approximation; actual validation happens in the service
        let estimatedSize = Int(image.size.width * image.size.height * 4) // RGBA bytes
        let maxSize = 10 * 1024 * 1024 // 10MB
        return estimatedSize <= maxSize
    }
    
    /// Resets the view model state
    func reset() {
        selectedDocumentType = nil
        capturedImage = nil
        uploadStatus = .idle
        uploadProgress = 0.0
        errorMessage = nil
        uploadedDocument = nil
    }
}

