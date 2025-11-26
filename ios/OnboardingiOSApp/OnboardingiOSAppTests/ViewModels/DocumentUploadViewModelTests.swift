//
//  DocumentUploadViewModelTests.swift
//  OnboardingiOSAppTests
//
//  Created by @frontend.eng
//

import XCTest
import Combine
@testable import OnboardingiOSApp

final class DocumentUploadViewModelTests: XCTestCase {
    
    var viewModel: DocumentUploadViewModel!
    var mockService: MockDocumentService!
    var cancellables: Set<AnyCancellable>!
    
    override func setUpWithError() throws {
        try super.setUpWithError()
        mockService = MockDocumentService()
        viewModel = DocumentUploadViewModel(documentService: mockService)
        cancellables = Set<AnyCancellable>()
    }
    
    override func tearDownWithError() throws {
        viewModel = nil
        mockService = nil
        cancellables = nil
        try super.tearDownWithError()
    }
    
    func testInitialState() throws {
        XCTAssertEqual(viewModel.selectedDocumentType, nil)
        XCTAssertEqual(viewModel.uploadStatus, .idle)
        XCTAssertNil(viewModel.capturedImage)
        XCTAssertNil(viewModel.errorMessage)
    }
    
    func testSelectDocumentType() throws {
        viewModel.selectDocumentType(.i9)
        XCTAssertEqual(viewModel.selectedDocumentType, .i9)
    }
    
    func testCaptureImage() throws {
        let testImage = createTestImage()
        viewModel.captureImage(testImage)
        
        XCTAssertNotNil(viewModel.capturedImage)
        XCTAssertEqual(viewModel.capturedImage, testImage)
    }
    
    func testRetakeImage() throws {
        let testImage = createTestImage()
        viewModel.captureImage(testImage)
        viewModel.retakeImage()
        
        XCTAssertNil(viewModel.capturedImage)
    }
    
    func testUploadDocumentSuccess() async throws {
        let testImage = createTestImage()
        viewModel.selectDocumentType(.i9)
        viewModel.captureImage(testImage)
        
        mockService.shouldSucceed = true
        
        let expectation = XCTestExpectation(description: "Upload completes")
        
        viewModel.$uploadStatus
            .dropFirst()
            .sink { status in
                if status == .success {
                    expectation.fulfill()
                }
            }
            .store(in: &cancellables)
        
        await viewModel.uploadDocument()
        
        await fulfillment(of: [expectation], timeout: 3.0)
        XCTAssertEqual(viewModel.uploadStatus, .success)
        XCTAssertNil(viewModel.errorMessage)
    }
    
    func testUploadDocumentFailure() async throws {
        let testImage = createTestImage()
        viewModel.selectDocumentType(.i9)
        viewModel.captureImage(testImage)
        
        mockService.shouldSucceed = false
        mockService.errorMessage = "Upload failed"
        
        let expectation = XCTestExpectation(description: "Upload fails")
        
        viewModel.$uploadStatus
            .dropFirst()
            .sink { status in
                if status == .error {
                    expectation.fulfill()
                }
            }
            .store(in: &cancellables)
        
        await viewModel.uploadDocument()
        
        await fulfillment(of: [expectation], timeout: 3.0)
        XCTAssertEqual(viewModel.uploadStatus, .error)
        XCTAssertNotNil(viewModel.errorMessage)
    }
    
    func testUploadProgressUpdates() async throws {
        let testImage = createTestImage()
        viewModel.selectDocumentType(.w4)
        viewModel.captureImage(testImage)
        
        mockService.shouldSucceed = true
        mockService.shouldReportProgress = true
        
        let progressExpectation = XCTestExpectation(description: "Progress updates")
        progressExpectation.expectedFulfillmentCount = 3
        
        viewModel.$uploadProgress
            .dropFirst()
            .sink { progress in
                if progress > 0 {
                    progressExpectation.fulfill()
                }
            }
            .store(in: &cancellables)
        
        await viewModel.uploadDocument()
        
        await fulfillment(of: [progressExpectation], timeout: 3.0)
        XCTAssertGreaterThan(viewModel.uploadProgress, 0)
    }
    
    func testImageValidation() throws {
        let validImage = createTestImage(size: CGSize(width: 1920, height: 1080))
        XCTAssertTrue(viewModel.validateImage(validImage))
        
        let invalidImage = createTestImage(size: CGSize(width: 100, height: 100))
        XCTAssertFalse(viewModel.validateImage(invalidImage))
    }
    
    func testFileSizeValidation() throws {
        let smallImage = createTestImage(size: CGSize(width: 1000, height: 1000))
        XCTAssertTrue(viewModel.validateFileSize(smallImage))
        
        // Note: Actual file size validation would require real image data
        // This is a placeholder for the validation logic
    }
    
    // MARK: - Helper Methods
    
    private func createTestImage(size: CGSize = CGSize(width: 1920, height: 1080)) -> UIImage {
        let renderer = UIGraphicsImageRenderer(size: size)
        return renderer.image { context in
            UIColor.blue.setFill()
            context.fill(CGRect(origin: .zero, size: size))
        }
    }
}

// MARK: - Mock Document Service

class MockDocumentService: DocumentServiceProtocol {
    var shouldSucceed = true
    var shouldReportProgress = false
    var errorMessage: String?
    
    func uploadDocument(_ image: UIImage, documentType: DocumentType, progressHandler: @escaping (Double) -> Void) async throws -> Document {
        if shouldReportProgress {
            progressHandler(0.25)
            try await Task.sleep(nanoseconds: 100_000_000)
            progressHandler(0.50)
            try await Task.sleep(nanoseconds: 100_000_000)
            progressHandler(0.75)
            try await Task.sleep(nanoseconds: 100_000_000)
            progressHandler(1.0)
        }
        
        if shouldSucceed {
            return Document(
                id: UUID(),
                userId: UUID(),
                documentType: documentType,
                status: .verified,
                fileName: "uploaded.pdf",
                fileSize: 1024 * 1024,
                createdAt: Date()
            )
        } else {
            throw DocumentServiceError.uploadFailed(errorMessage ?? "Unknown error")
        }
    }
}

