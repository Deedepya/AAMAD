//
//  DocumentProcessorTests.swift
//  OnboardingiOSAppTests
//
//  Created by @frontend.eng
//

import XCTest
@testable import OnboardingiOSApp

final class DocumentProcessorTests: XCTestCase {
    
    var processor: DocumentProcessor!
    
    override func setUpWithError() throws {
        try super.setUpWithError()
        processor = DocumentProcessor()
    }
    
    override func tearDownWithError() throws {
        processor = nil
        try super.tearDownWithError()
    }
    
    func testProcessDocumentImage() async throws {
        let image = createTestImage()
        let result = try await processor.processDocumentImage(image, documentType: .i9)
        
        XCTAssertNotNil(result)
        XCTAssertEqual(result.documentType, .i9)
        XCTAssertNotNil(result.processedImageData)
    }
    
    func testCompressDocument() throws {
        let image = createLargeTestImage()
        let imageData = image.jpegData(compressionQuality: 1.0)!
        
        let compressedData = try processor.compressDocument(imageData, maxSizeMB: 5.0)
        
        XCTAssertNotNil(compressedData)
        let sizeInMB = Double(compressedData.count) / (1024 * 1024)
        XCTAssertLessThanOrEqual(sizeInMB, 5.0)
    }
    
    func testValidateDocumentRequirements() throws {
        let validImage = createTestImage(size: CGSize(width: 1920, height: 1080))
        let imageData = validImage.jpegData(compressionQuality: 0.8)!
        
        let validation = processor.validateDocumentRequirements(
            imageData: imageData,
            resolution: CGSize(width: 1920, height: 1080),
            documentType: .i9
        )
        
        XCTAssertTrue(validation.isValid)
        XCTAssertNil(validation.error)
    }
    
    func testValidateDocumentRequirementsFailsForLowResolution() throws {
        let invalidImage = createTestImage(size: CGSize(width: 100, height: 100))
        let imageData = invalidImage.jpegData(compressionQuality: 0.8)!
        
        let validation = processor.validateDocumentRequirements(
            imageData: imageData,
            resolution: CGSize(width: 100, height: 100),
            documentType: .i9
        )
        
        XCTAssertFalse(validation.isValid)
        XCTAssertNotNil(validation.error)
    }
    
    func testValidateDocumentRequirementsFailsForLargeFile() throws {
        let image = createTestImage()
        // Create a data blob that exceeds the limit
        var largeData = image.jpegData(compressionQuality: 1.0)!
        // Pad to exceed 10MB
        largeData.append(Data(count: 11 * 1024 * 1024))
        
        let validation = processor.validateDocumentRequirements(
            imageData: largeData,
            resolution: CGSize(width: 1920, height: 1080),
            documentType: .i9
        )
        
        XCTAssertFalse(validation.isValid)
        XCTAssertNotNil(validation.error)
    }
    
    // MARK: - Helper Methods
    
    private func createTestImage(size: CGSize = CGSize(width: 1920, height: 1080)) -> UIImage {
        let renderer = UIGraphicsImageRenderer(size: size)
        return renderer.image { context in
            UIColor.blue.setFill()
            context.fill(CGRect(origin: .zero, size: size))
        }
    }
    
    private func createLargeTestImage() -> UIImage {
        return createTestImage(size: CGSize(width: 4000, height: 3000))
    }
}

