//
//  DocumentService.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import Foundation
import UIKit
import Combine

/// Protocol for document service to enable testing
protocol DocumentServiceProtocol {
    func uploadDocument(
        _ image: UIImage,
        documentType: DocumentType,
        progressHandler: @escaping (Double) -> Void
    ) async throws -> Document
}

/// Document service errors
enum DocumentServiceError: LocalizedError {
    case uploadFailed(String)
    case invalidImage
    case fileSizeExceeded
    case networkError(String)
    
    var errorDescription: String? {
        switch self {
        case .uploadFailed(let message):
            return "Upload failed: \(message)"
        case .invalidImage:
            return "Invalid image format"
        case .fileSizeExceeded:
            return "File size exceeds 10MB limit"
        case .networkError(let message):
            return "Network error: \(message)"
        }
    }
}

/// Document service for handling document uploads and processing
class DocumentService: DocumentServiceProtocol {
    
    private let baseURL = "https://api.onboarding.example.com/v1" // Mock API URL
    private let maxFileSizeMB: Double = 10.0
    private let minResolution = CGSize(width: 800, height: 600)
    
    /// Uploads a document image to the backend
    func uploadDocument(
        _ image: UIImage,
        documentType: DocumentType,
        progressHandler: @escaping (Double) -> Void
    ) async throws -> Document {
        // Validate image
        guard validateImageResolution(image) else {
            throw DocumentServiceError.invalidImage
        }
        
        // Compress image if needed
        let imageData = try compressImage(image, maxSizeMB: maxFileSizeMB)
        
        // Validate file size
        guard validateFileSize(imageData, maxSizeMB: maxFileSizeMB) else {
            throw DocumentServiceError.fileSizeExceeded
        }
        
        // Extract metadata
        let metadata = extractImageMetadata(image)
        
        // Simulate upload progress (mock implementation)
        progressHandler(0.1)
        try await Task.sleep(nanoseconds: 200_000_000) // 0.2 seconds
        
        progressHandler(0.5)
        try await Task.sleep(nanoseconds: 200_000_000)
        
        progressHandler(0.8)
        try await Task.sleep(nanoseconds: 200_000_000)
        
        progressHandler(1.0)
        
        // Mock API response - in real implementation, this would be an actual network call
        // For MVP, we return a mock document
        return Document(
            id: UUID(),
            userId: UUID(), // Would come from authentication
            documentType: documentType,
            status: .verified,
            fileName: "\(documentType.rawValue.replacingOccurrences(of: " ", with: "_")).jpg",
            fileSize: imageData.count,
            createdAt: Date(),
            resolution: metadata
        )
    }
    
    /// Compresses an image to meet size requirements
    func compressImage(_ image: UIImage, maxSizeMB: Double) throws -> Data {
        let maxSizeBytes = Int(maxSizeMB * 1024 * 1024)
        var compressionQuality: CGFloat = 0.8
        var imageData = image.jpegData(compressionQuality: compressionQuality)!
        
        // Reduce quality until we meet size requirements
        while imageData.count > maxSizeBytes && compressionQuality > 0.1 {
            compressionQuality -= 0.1
            if let data = image.jpegData(compressionQuality: compressionQuality) {
                imageData = data
            } else {
                break
            }
        }
        
        // If still too large, resize the image
        if imageData.count > maxSizeBytes {
            let scaleFactor = sqrt(Double(maxSizeBytes) / Double(imageData.count))
            let newSize = CGSize(
                width: image.size.width * scaleFactor,
                height: image.size.height * scaleFactor
            )
            
            let renderer = UIGraphicsImageRenderer(size: newSize)
            let resizedImage = renderer.image { _ in
                image.draw(in: CGRect(origin: .zero, size: newSize))
            }
            
            if let resizedData = resizedImage.jpegData(compressionQuality: 0.7) {
                imageData = resizedData
            }
        }
        
        return imageData
    }
    
    /// Validates image resolution meets minimum requirements
    func validateImageResolution(_ image: UIImage) -> Bool {
        let resolution = image.size
        return resolution.width >= minResolution.width &&
               resolution.height >= minResolution.height
    }
    
    /// Validates file size is within limits
    func validateFileSize(_ data: Data, maxSizeMB: Double) -> Bool {
        let maxSizeBytes = Int(maxSizeMB * 1024 * 1024)
        return data.count <= maxSizeBytes
    }
    
    /// Extracts metadata from an image
    func extractImageMetadata(_ image: UIImage) -> CGSize {
        return image.size
    }
    
    /// Converts image to JPEG format
    func convertToJPEG(_ image: UIImage, quality: CGFloat = 0.8) throws -> Data {
        guard let jpegData = image.jpegData(compressionQuality: quality) else {
            throw DocumentServiceError.invalidImage
        }
        return jpegData
    }
    
    /// Detects image format from data
    func detectImageFormat(_ data: Data) -> ImageFormat? {
        guard data.count >= 4 else { return nil }
        
        var bytes = [UInt8](repeating: 0, count: 4)
        data.copyBytes(to: &bytes, count: 4)
        
        // JPEG: FF D8 FF
        if bytes[0] == 0xFF && bytes[1] == 0xD8 && bytes[2] == 0xFF {
            return .jpeg
        }
        
        // PNG: 89 50 4E 47
        if bytes[0] == 0x89 && bytes[1] == 0x50 && bytes[2] == 0x4E && bytes[3] == 0x47 {
            return .png
        }
        
        return nil
    }
}

/// Image format enumeration
enum ImageFormat {
    case jpeg
    case png
}

