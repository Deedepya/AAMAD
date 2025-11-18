//
//  DocumentModelTests.swift
//  OnboardingAppTests
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import XCTest
import UIKit
@testable import OnboardingApp

final class DocumentModelTests: XCTestCase {
    
    func testDocumentInitialization() {
        // Given
        let documentType = DocumentType.i9
        let image = UIImage(systemName: "doc.text")!
        let metadata = DocumentMetadata(
            fileSize: 1024,
            width: 100,
            height: 100,
            format: "PNG"
        )
        
        // When
        let document = Document(
            id: "test-id",
            type: documentType,
            image: image,
            metadata: metadata,
            status: .pending,
            uploadedAt: nil
        )
        
        // Then
        XCTAssertEqual(document.id, "test-id")
        XCTAssertEqual(document.type, documentType)
        XCTAssertNotNil(document.image)
        XCTAssertEqual(document.metadata.fileSize, 1024)
        XCTAssertEqual(document.status, .pending)
        XCTAssertNil(document.uploadedAt)
    }
    
    func testDocumentTypeEnum() {
        // Test all document types exist
        XCTAssertNotNil(DocumentType.i9)
        XCTAssertNotNil(DocumentType.w4)
        XCTAssertNotNil(DocumentType.driversLicense)
        XCTAssertNotNil(DocumentType.passport)
        XCTAssertNotNil(DocumentType.socialSecurityCard)
    }
    
    func testDocumentStatusEnum() {
        // Test all status types exist
        XCTAssertNotNil(DocumentStatus.pending)
        XCTAssertNotNil(DocumentStatus.uploading)
        XCTAssertNotNil(DocumentStatus.uploaded)
        XCTAssertNotNil(DocumentStatus.verified)
        XCTAssertNotNil(DocumentStatus.failed)
    }
    
    func testDocumentMetadataInitialization() {
        // Given
        let metadata = DocumentMetadata(
            fileSize: 2048,
            width: 200,
            height: 300,
            format: "JPEG"
        )
        
        // Then
        XCTAssertEqual(metadata.fileSize, 2048)
        XCTAssertEqual(metadata.width, 200)
        XCTAssertEqual(metadata.height, 300)
        XCTAssertEqual(metadata.format, "JPEG")
    }
    
    func testDocumentEquality() {
        // Given
        let image = UIImage(systemName: "doc.text")!
        let metadata = DocumentMetadata(fileSize: 1024, width: 100, height: 100, format: "PNG")
        
        let document1 = Document(
            id: "same-id",
            type: .i9,
            image: image,
            metadata: metadata,
            status: .pending,
            uploadedAt: nil
        )
        
        let document2 = Document(
            id: "same-id",
            type: .i9,
            image: image,
            metadata: metadata,
            status: .pending,
            uploadedAt: nil
        )
        
        // Then
        XCTAssertEqual(document1.id, document2.id)
    }
}

