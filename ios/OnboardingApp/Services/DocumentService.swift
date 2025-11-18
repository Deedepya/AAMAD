//
//  DocumentService.swift
//  OnboardingApp
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import UIKit
import Foundation

/// Result of image validation
struct ImageValidationResult {
    let isValid: Bool
    let error: String?
    
    init(isValid: Bool, error: String? = nil) {
        self.isValid = isValid
        self.error = error
    }
}

/// Service for handling document processing operations
class DocumentService {
    
    // Minimum resolution requirements (per SAD requirements)
    private let minimumWidth: Int = 200
    private let minimumHeight: Int = 200
    
    /// Compresses an image to meet maximum size requirements
    /// - Parameters:
    ///   - image: The image to compress
    ///   - maxSize: Maximum file size in bytes (default: 10MB per SAD)
    /// - Returns: Compressed image
    func compressImage(_ image: UIImage, maxSize: Int = 10 * 1024 * 1024) -> UIImage {
        guard let imageData = image.jpegData(compressionQuality: 1.0) else {
            return image
        }
        
        // If image is already within size limit, return as is
        if imageData.count <= maxSize {
            return image
        }
        
        // Calculate target compression quality
        let ratio = Double(maxSize) / Double(imageData.count)
        var compressionQuality: CGFloat = CGFloat(ratio * 0.9) // Use 90% of calculated ratio for safety
        
        // Ensure compression quality is within valid range
        compressionQuality = max(0.1, min(1.0, compressionQuality))
        
        // Try to compress
        var compressedData = image.jpegData(compressionQuality: compressionQuality)
        var attempts = 0
        let maxAttempts = 5
        
        // If still too large, reduce quality further
        while let data = compressedData, data.count > maxSize && attempts < maxAttempts {
            compressionQuality *= 0.8
            compressedData = image.jpegData(compressionQuality: compressionQuality)
            attempts += 1
        }
        
        // If still too large, resize the image
        if let data = compressedData, data.count > maxSize {
            let scale = sqrt(Double(maxSize) / Double(data.count))
            let newSize = CGSize(
                width: image.size.width * scale,
                height: image.size.height * scale
            )
            return resizeImage(image, to: newSize)
        }
        
        return compressedData.flatMap { UIImage(data: $0) } ?? image
    }
    
    /// Validates an image meets quality requirements
    /// - Parameter image: The image to validate
    /// - Returns: Validation result with success status and optional error message
    func validateImage(_ image: UIImage?) -> ImageValidationResult {
        guard let image = image else {
            return ImageValidationResult(
                isValid: false,
                error: "No image provided"
            )
        }
        
        let width = Int(image.size.width * image.scale)
        let height = Int(image.size.height * image.scale)
        
        if width < minimumWidth || height < minimumHeight {
            return ImageValidationResult(
                isValid: false,
                error: "Image resolution too low. Minimum size: \(minimumWidth)x\(minimumHeight) pixels"
            )
        }
        
        return ImageValidationResult(isValid: true)
    }
    
    /// Extracts metadata from an image
    /// - Parameter image: The image to extract metadata from
    /// - Returns: Document metadata
    func extractMetadata(_ image: UIImage) -> DocumentMetadata {
        let width = Int(image.size.width * image.scale)
        let height = Int(image.size.height * image.scale)
        
        // Get file size
        let imageData = image.jpegData(compressionQuality: 0.8) ?? Data()
        let fileSize = imageData.count
        
        // Determine format
        let format = imageData.isEmpty ? "Unknown" : "JPEG"
        
        return DocumentMetadata(
            fileSize: fileSize,
            width: width,
            height: height,
            format: format
        )
    }
    
    /// Validates file size is within limit
    /// - Parameters:
    ///   - image: The image to validate
    ///   - maxSize: Maximum file size in bytes (default: 10MB per SAD)
    /// - Returns: True if file size is within limit
    func validateFileSize(_ image: UIImage, maxSize: Int = 10 * 1024 * 1024) -> Bool {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            return false
        }
        return imageData.count <= maxSize
    }
    
    // MARK: - Private Helpers
    
    /// Resizes an image to a new size
    private func resizeImage(_ image: UIImage, to size: CGSize) -> UIImage {
        UIGraphicsBeginImageContextWithOptions(size, false, image.scale)
        defer { UIGraphicsEndImageContext() }
        
        image.draw(in: CGRect(origin: .zero, size: size))
        return UIGraphicsGetImageFromCurrentImageContext() ?? image
    }
}

