//
//  Document.swift
//  OnboardingApp
//
//  Created by Frontend Engineer
//  Copyright © 2024 AAMAD. All rights reserved.
//

import UIKit
import Foundation

/// Represents a document type for onboarding
enum DocumentType: String, CaseIterable, Codable {
    case i9 = "I-9"
    case w4 = "W-4"
    case driversLicense = "Driver's License"
    case passport = "Passport"
    case socialSecurityCard = "Social Security Card"
}

/// Represents the status of a document
enum DocumentStatus: String, Codable {
    case pending
    case uploading
    case uploaded
    case verified
    case failed
}

/// Metadata about a document
struct DocumentMetadata: Codable, Equatable {
    let fileSize: Int // Size in bytes
    let width: Int
    let height: Int
    let format: String
    
    init(fileSize: Int, width: Int, height: Int, format: String) {
        self.fileSize = fileSize
        self.width = width
        self.height = height
        self.format = format
    }
}

/// Represents a document in the onboarding process
struct Document: Identifiable, Equatable {
    let id: String
    let type: DocumentType
    let image: UIImage
    let metadata: DocumentMetadata
    var status: DocumentStatus
    var uploadedAt: Date?
    
    init(id: String = UUID().uuidString,
         type: DocumentType,
         image: UIImage,
         metadata: DocumentMetadata,
         status: DocumentStatus = .pending,
         uploadedAt: Date? = nil) {
        self.id = id
        self.type = type
        self.image = image
        self.metadata = metadata
        self.status = status
        self.uploadedAt = uploadedAt
    }
    
    // Equatable conformance (UIImage doesn't conform to Equatable, so we compare IDs)
    static func == (lhs: Document, rhs: Document) -> Bool {
        return lhs.id == rhs.id
    }
}

