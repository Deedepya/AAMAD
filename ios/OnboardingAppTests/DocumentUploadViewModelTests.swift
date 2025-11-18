//
//  DocumentUploadViewModelTests.swift
//  OnboardingAppTests
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import XCTest
import UIKit
import Combine
@testable import OnboardingApp

final class DocumentUploadViewModelTests: XCTestCase {
    
    var viewModel: DocumentUploadViewModel!
    var cancellables: Set<AnyCancellable>!
    
    override func setUp() {
        super.setUp()
        cancellables = Set<AnyCancellable>()
        viewModel = DocumentUploadViewModel()
    }
    
    override func tearDown() {
        cancellables = nil
        viewModel = nil
        super.tearDown()
    }
    
    func testInitialState() {
        // Then
        XCTAssertNil(viewModel.capturedImage, "Initial captured image should be nil")
        XCTAssertEqual(viewModel.documentType, .i9, "Initial document type should be I-9")
        XCTAssertEqual(viewModel.uploadProgress, 0.0, "Initial upload progress should be 0")
        XCTAssertEqual(viewModel.uploadStatus, .idle, "Initial upload status should be idle")
        XCTAssertNil(viewModel.errorMessage, "Initial error message should be nil")
    }
    
    func testSetCapturedImage() {
        // Given
        let image = UIImage(systemName: "doc.text")!
        
        // When
        viewModel.capturedImage = image
        
        // Then
        XCTAssertNotNil(viewModel.capturedImage, "Captured image should be set")
    }
    
    func testSetDocumentType() {
        // Given
        let newType = DocumentType.w4
        
        // When
        viewModel.documentType = newType
        
        // Then
        XCTAssertEqual(viewModel.documentType, newType, "Document type should be updated")
    }
    
    func testValidateDocumentWithValidImage() {
        // Given
        let validImage = createTestImage(width: 800, height: 600)
        viewModel.capturedImage = validImage
        viewModel.documentType = .i9
        
        // When
        let isValid = viewModel.validateDocument()
        
        // Then
        XCTAssertTrue(isValid, "Valid document should pass validation")
        XCTAssertNil(viewModel.errorMessage, "Valid document should have no error")
    }
    
    func testValidateDocumentWithInvalidImage() {
        // Given
        let invalidImage = createTestImage(width: 50, height: 50) // Too small
        viewModel.capturedImage = invalidImage
        viewModel.documentType = .i9
        
        // When
        let isValid = viewModel.validateDocument()
        
        // Then
        XCTAssertFalse(isValid, "Invalid document should fail validation")
        XCTAssertNotNil(viewModel.errorMessage, "Invalid document should have error message")
    }
    
    func testValidateDocumentWithNilImage() {
        // Given
        viewModel.capturedImage = nil
        viewModel.documentType = .i9
        
        // When
        let isValid = viewModel.validateDocument()
        
        // Then
        XCTAssertFalse(isValid, "Nil image should fail validation")
        XCTAssertNotNil(viewModel.errorMessage, "Nil image should have error message")
    }
    
    func testUploadDocumentUpdatesProgress() {
        // Given
        let image = createTestImage(width: 800, height: 600)
        viewModel.capturedImage = image
        viewModel.documentType = .i9
        
        let progressExpectation = expectation(description: "Upload progress should update")
        var progressValues: [Double] = []
        
        viewModel.$uploadProgress
            .dropFirst() // Skip initial 0.0
            .sink { progress in
                progressValues.append(progress)
                if progress >= 1.0 {
                    progressExpectation.fulfill()
                }
            }
            .store(in: &cancellables)
        
        // When
        viewModel.uploadDocument()
        
        // Then
        waitForExpectations(timeout: 3.0) { _ in
            XCTAssertFalse(progressValues.isEmpty, "Progress values should be updated")
            XCTAssertEqual(self.viewModel.uploadStatus, .completed, "Upload status should be completed")
        }
    }
    
    func testUploadDocumentUpdatesStatus() {
        // Given
        let image = createTestImage(width: 800, height: 600)
        viewModel.capturedImage = image
        viewModel.documentType = .i9
        
        let statusExpectation = expectation(description: "Upload status should update")
        
        viewModel.$uploadStatus
            .dropFirst() // Skip initial .idle
            .sink { status in
                if status == .completed || status == .failed {
                    statusExpectation.fulfill()
                }
            }
            .store(in: &cancellables)
        
        // When
        viewModel.uploadDocument()
        
        // Then
        waitForExpectations(timeout: 3.0) { _ in
            XCTAssertTrue(self.viewModel.uploadStatus == .completed || self.viewModel.uploadStatus == .failed)
        }
    }
    
    func testRetryUploadResetsState() {
        // Given
        let image = createTestImage(width: 800, height: 600)
        viewModel.capturedImage = image
        viewModel.documentType = .i9
        viewModel.uploadStatus = .failed
        viewModel.errorMessage = "Test error"
        
        // When
        viewModel.retryUpload()
        
        // Then
        XCTAssertEqual(viewModel.uploadStatus, .idle, "Retry should reset status to idle")
        XCTAssertNil(viewModel.errorMessage, "Retry should clear error message")
        XCTAssertEqual(viewModel.uploadProgress, 0.0, "Retry should reset progress")
    }
    
    func testRetryUploadWithValidDocument() {
        // Given
        let image = createTestImage(width: 800, height: 600)
        viewModel.capturedImage = image
        viewModel.documentType = .i9
        
        let completionExpectation = expectation(description: "Retry upload should complete")
        
        viewModel.$uploadStatus
            .dropFirst()
            .sink { status in
                if status == .completed {
                    completionExpectation.fulfill()
                }
            }
            .store(in: &cancellables)
        
        // When
        viewModel.retryUpload()
        
        // Then
        waitForExpectations(timeout: 3.0) { _ in
            XCTAssertEqual(self.viewModel.uploadStatus, .completed, "Retry upload should complete successfully")
        }
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

