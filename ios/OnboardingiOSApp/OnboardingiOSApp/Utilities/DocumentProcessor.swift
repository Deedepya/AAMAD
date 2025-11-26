//
//  DocumentProcessor.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import Foundation
import UIKit

/// Document processing result
struct DocumentProcessingResult {
    let documentType: DocumentType
    let processedImageData: Data
    let metadata: ImageMetadata
    let validationStatus: DocumentValidationStatus
}

/// Image metadata
struct ImageMetadata {
    let width: CGFloat
    let height: CGFloat
    let fileSize: Int
}

/// Document validation status
struct DocumentValidationStatus {
    let isValid: Bool
    let error: String?
}

/// Document processor for handling document processing operations
class DocumentProcessor {
    
    private let maxFileSizeMB: Double = 10.0
    private let minResolution = CGSize(width: 800, height: 600)
    
    /// Processes a document image
    func processDocumentImage(
        _ image: UIImage,
        documentType: DocumentType
    ) async throws -> DocumentProcessingResult {
        // Convert to JPEG
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            throw DocumentServiceError.invalidImage
        }
        
        // Extract metadata
        let metadata = ImageMetadata(
            width: image.size.width,
            height: image.size.height,
            fileSize: imageData.count
        )
        
        // Validate requirements
        let validation = validateDocumentRequirements(
            imageData: imageData,
            resolution: image.size,
            documentType: documentType
        )
        
        // Compress if needed
        let processedData = try compressDocument(imageData, maxSizeMB: maxFileSizeMB)
        
        return DocumentProcessingResult(
            documentType: documentType,
            processedImageData: processedData,
            metadata: metadata,
            validationStatus: validation
        )
    }
    
    /// Compresses document data to meet size requirements
    func compressDocument(_ data: Data, maxSizeMB: Double) throws -> Data {
        let maxSizeBytes = Int(maxSizeMB * 1024 * 1024)
        
        guard data.count > maxSizeBytes else {
            return data
        }
        
        // Decompress and recompress with lower quality
        guard let image = UIImage(data: data) else {
            throw DocumentServiceError.invalidImage
        }
        
        var compressionQuality: CGFloat = 0.7
        var compressedData = image.jpegData(compressionQuality: compressionQuality)!
        
        while compressedData.count > maxSizeBytes && compressionQuality > 0.1 {
            compressionQuality -= 0.1
            if let data = image.jpegData(compressionQuality: compressionQuality) {
                compressedData = data
            } else {
                break
            }
        }
        
        return compressedData
    }
    
    /// Validates document requirements
    func validateDocumentRequirements(
        imageData: Data,
        resolution: CGSize,
        documentType: DocumentType
    ) -> DocumentValidationStatus {
        // Check resolution
        if resolution.width < minResolution.width || resolution.height < minResolution.height {
            return DocumentValidationStatus(
                isValid: false,
                error: "Image resolution must be at least \(Int(minResolution.width))x\(Int(minResolution.height)) pixels"
            )
        }
        
        // Check file size
        let sizeInMB = Double(imageData.count) / (1024 * 1024)
        if sizeInMB > maxFileSizeMB {
            return DocumentValidationStatus(
                isValid: false,
                error: "File size (\(String(format: "%.2f", sizeInMB))MB) exceeds \(maxFileSizeMB)MB limit"
            )
        }
        
        return DocumentValidationStatus(isValid: true, error: nil)
    }
}

