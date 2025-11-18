//
//  DocumentServiceTests.swift
//  OnboardingAppTests
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import XCTest
import UIKit
@testable import OnboardingApp

final class DocumentServiceTests: XCTestCase {
    
    var documentService: DocumentService!
    
    override func setUp() {
        super.setUp()
        documentService = DocumentService()
    }
    
    override func tearDown() {
        documentService = nil
        super.tearDown()
    }
    
    func testCompressImageReducesFileSize() {
        // Given - Create a large test image
        let largeImage = createTestImage(width: 2000, height: 2000)
        let originalData = largeImage.jpegData(compressionQuality: 1.0)!
        let originalSize = originalData.count
        
        // When
        let compressedImage = documentService.compressImage(largeImage, maxSize: 1024 * 500) // 500KB max
        
        // Then
        let compressedData = compressedImage.jpegData(compressionQuality: 0.8)!
        let compressedSize = compressedData.count
        XCTAssertLessThan(compressedSize, originalSize, "Compressed image should be smaller than original")
    }
    
    func testCompressImageRespectsMaxSize() {
        // Given
        let largeImage = createTestImage(width: 3000, height: 3000)
        let maxSize = 1024 * 100 // 100KB max
        
        // When
        let compressedImage = documentService.compressImage(largeImage, maxSize: maxSize)
        
        // Then
        let compressedData = compressedImage.jpegData(compressionQuality: 0.8)!
        XCTAssertLessThanOrEqual(compressedData.count, maxSize, "Compressed image should respect max size")
    }
    
    func testValidateImageWithValidImage() {
        // Given
        let validImage = createTestImage(width: 800, height: 600)
        
        // When
        let result = documentService.validateImage(validImage)
        
        // Then
        XCTAssertTrue(result.isValid, "Valid image should pass validation")
        XCTAssertNil(result.error, "Valid image should have no error")
    }
    
    func testValidateImageWithTooSmallImage() {
        // Given - Image below minimum resolution
        let smallImage = createTestImage(width: 100, height: 100)
        
        // When
        let result = documentService.validateImage(smallImage)
        
        // Then
        XCTAssertFalse(result.isValid, "Image below minimum resolution should fail validation")
        XCTAssertNotNil(result.error, "Invalid image should have error message")
    }
    
    func testValidateImageWithNilImage() {
        // Given
        let nilImage: UIImage? = nil
        
        // When
        let result = documentService.validateImage(nilImage)
        
        // Then
        XCTAssertFalse(result.isValid, "Nil image should fail validation")
        XCTAssertNotNil(result.error, "Nil image should have error message")
    }
    
    func testExtractMetadata() {
        // Given
        let image = createTestImage(width: 1200, height: 800)
        
        // When
        let metadata = documentService.extractMetadata(image)
        
        // Then
        XCTAssertEqual(metadata.width, 1200, "Metadata should contain correct width")
        XCTAssertEqual(metadata.height, 800, "Metadata should contain correct height")
        XCTAssertNotNil(metadata.format, "Metadata should contain format")
        XCTAssertGreaterThan(metadata.fileSize, 0, "Metadata should contain file size")
    }
    
    func testFileSizeValidationWithinLimit() {
        // Given
        let image = createTestImage(width: 1000, height: 1000)
        let maxSize = 10 * 1024 * 1024 // 10MB limit per SAD
        
        // When
        let isValid = documentService.validateFileSize(image, maxSize: maxSize)
        
        // Then
        XCTAssertTrue(isValid, "Image within size limit should pass validation")
    }
    
    // MARK: - Helper Methods
    
    private func createTestImage(width: Int, height: Int) -> UIImage {
        let size = CGSize(width: width, height: height)
        UIGraphicsBeginImageContextWithOptions(size, false, 1.0)
        UIColor.blue.setFill()
        UIRectFill(CGRect(origin: .zero, size: size))
        let image = UIGraphicsGetImageFromCurrentImageContext()!
        UIGraphicsEndImageContext()
        return image
    }
}

