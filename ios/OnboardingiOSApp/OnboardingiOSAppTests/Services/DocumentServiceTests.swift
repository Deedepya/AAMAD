//
//  DocumentServiceTests.swift
//  OnboardingiOSAppTests
//
//  Created by @frontend.eng
//

import XCTest
@testable import OnboardingiOSApp

final class DocumentServiceTests: XCTestCase {
    
    var service: DocumentService!
    
    override func setUpWithError() throws {
        try super.setUpWithError()
        service = DocumentService()
    }
    
    override func tearDownWithError() throws {
        service = nil
        try super.tearDownWithError()
    }
    
    func testCompressImage() throws {
        let largeImage = createLargeTestImage()
        let compressedData = try service.compressImage(largeImage, maxSizeMB: 5.0)
        
        XCTAssertNotNil(compressedData)
        let sizeInMB = Double(compressedData.count) / (1024 * 1024)
        XCTAssertLessThanOrEqual(sizeInMB, 5.0)
    }
    
    func testCompressImageMaintainsQuality() throws {
        let originalImage = createTestImage()
        let compressedData = try service.compressImage(originalImage, maxSizeMB: 10.0)
        
        XCTAssertNotNil(compressedData)
        let decompressedImage = UIImage(data: compressedData)
        XCTAssertNotNil(decompressedImage)
    }
    
    func testValidateImageResolution() throws {
        let validImage = createTestImage(size: CGSize(width: 1920, height: 1080))
        XCTAssertTrue(service.validateImageResolution(validImage))
        
        let invalidImage = createTestImage(size: CGSize(width: 100, height: 100))
        XCTAssertFalse(service.validateImageResolution(invalidImage))
    }
    
    func testValidateFileSize() throws {
        let smallImage = createTestImage(size: CGSize(width: 1000, height: 1000))
        let imageData = smallImage.jpegData(compressionQuality: 0.8)!
        XCTAssertTrue(service.validateFileSize(imageData, maxSizeMB: 10.0))
        
        // Create a large data blob to test size limit
        let largeData = Data(count: 15 * 1024 * 1024) // 15MB
        XCTAssertFalse(service.validateFileSize(largeData, maxSizeMB: 10.0))
    }
    
    func testExtractImageMetadata() throws {
        let image = createTestImage(size: CGSize(width: 1920, height: 1080))
        let metadata = service.extractImageMetadata(image)
        
        XCTAssertNotNil(metadata)
        XCTAssertEqual(metadata.width, 1920)
        XCTAssertEqual(metadata.height, 1080)
    }
    
    func testFormatConversion() throws {
        let image = createTestImage()
        let jpegData = try service.convertToJPEG(image, quality: 0.8)
        
        XCTAssertNotNil(jpegData)
        // Verify it's actually JPEG format
        let imageFormat = service.detectImageFormat(jpegData)
        XCTAssertEqual(imageFormat, .jpeg)
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

