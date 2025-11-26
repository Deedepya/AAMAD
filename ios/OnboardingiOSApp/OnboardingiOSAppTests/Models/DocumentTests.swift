//
//  DocumentTests.swift
//  OnboardingiOSAppTests
//
//  Created by @frontend.eng
//

import XCTest
@testable import OnboardingiOSApp

final class DocumentTests: XCTestCase {
    
    func testDocumentInitialization() throws {
        let document = Document(
            id: UUID(),
            userId: UUID(),
            documentType: .i9,
            status: .pending,
            fileName: "test.pdf",
            fileSize: 1024 * 1024, // 1MB
            createdAt: Date()
        )
        
        XCTAssertEqual(document.documentType, .i9)
        XCTAssertEqual(document.status, .pending)
        XCTAssertEqual(document.fileSize, 1024 * 1024)
    }
    
    func testDocumentTypeEnum() throws {
        XCTAssertEqual(DocumentType.i9.rawValue, "I-9")
        XCTAssertEqual(DocumentType.w4.rawValue, "W-4")
        XCTAssertEqual(DocumentType.driversLicense.rawValue, "Driver's License")
        XCTAssertEqual(DocumentType.passport.rawValue, "Passport")
        XCTAssertEqual(DocumentType.socialSecurityCard.rawValue, "Social Security Card")
    }
    
    func testDocumentStatusEnum() throws {
        XCTAssertEqual(DocumentStatus.pending.rawValue, "pending")
        XCTAssertEqual(DocumentStatus.uploading.rawValue, "uploading")
        XCTAssertEqual(DocumentStatus.processing.rawValue, "processing")
        XCTAssertEqual(DocumentStatus.verified.rawValue, "verified")
        XCTAssertEqual(DocumentStatus.rejected.rawValue, "rejected")
        XCTAssertEqual(DocumentStatus.error.rawValue, "error")
    }
    
    func testDocumentFileSizeValidation() throws {
        let validDocument = Document(
            id: UUID(),
            userId: UUID(),
            documentType: .i9,
            status: .pending,
            fileName: "test.pdf",
            fileSize: 5 * 1024 * 1024, // 5MB (under 10MB limit)
            createdAt: Date()
        )
        
        XCTAssertTrue(validDocument.isFileSizeValid)
        
        let invalidDocument = Document(
            id: UUID(),
            userId: UUID(),
            documentType: .i9,
            status: .pending,
            fileName: "test.pdf",
            fileSize: 15 * 1024 * 1024, // 15MB (over 10MB limit)
            createdAt: Date()
        )
        
        XCTAssertFalse(invalidDocument.isFileSizeValid)
    }
    
    func testDocumentMetadata() throws {
        let document = Document(
            id: UUID(),
            userId: UUID(),
            documentType: .w4,
            status: .processing,
            fileName: "w4-form.pdf",
            fileSize: 2 * 1024 * 1024,
            createdAt: Date(),
            resolution: CGSize(width: 1920, height: 1080)
        )
        
        XCTAssertNotNil(document.resolution)
        XCTAssertEqual(document.resolution?.width, 1920)
        XCTAssertEqual(document.resolution?.height, 1080)
    }
}

