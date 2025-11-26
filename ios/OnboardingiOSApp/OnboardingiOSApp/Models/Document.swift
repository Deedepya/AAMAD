//
//  Document.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import Foundation
import UIKit

/// Document type enumeration
enum DocumentType: String, Codable, CaseIterable {
    case i9 = "I-9"
    case w4 = "W-4"
    case driversLicense = "Driver's License"
    case passport = "Passport"
    case socialSecurityCard = "Social Security Card"
}

/// Document status enumeration
enum DocumentStatus: String, Codable {
    case pending = "pending"
    case uploading = "uploading"
    case processing = "processing"
    case verified = "verified"
    case rejected = "rejected"
    case error = "error"
}

/// Document model representing an uploaded document
struct Document: Identifiable {
    let id: UUID
    let userId: UUID
    let documentType: DocumentType
    var status: DocumentStatus
    let fileName: String
    let fileSize: Int // Size in bytes
    let createdAt: Date
    var updatedAt: Date?
    var resolution: CGSize?
    var extractedData: [String: Any]?
    
    /// Maximum file size limit in bytes (10MB per SAD)
    static let maxFileSizeBytes = 10 * 1024 * 1024
    
    /// Minimum resolution requirements (per features list)
    static let minResolution = CGSize(width: 800, height: 600)
    
    init(
        id: UUID = UUID(),
        userId: UUID,
        documentType: DocumentType,
        status: DocumentStatus,
        fileName: String,
        fileSize: Int,
        createdAt: Date = Date(),
        updatedAt: Date? = nil,
        resolution: CGSize? = nil,
        extractedData: [String: Any]? = nil
    ) {
        self.id = id
        self.userId = userId
        self.documentType = documentType
        self.status = status
        self.fileName = fileName
        self.fileSize = fileSize
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.resolution = resolution
        self.extractedData = extractedData
    }
    
    /// Validates if file size is within the 10MB limit
    var isFileSizeValid: Bool {
        return fileSize <= Document.maxFileSizeBytes
    }
    
    /// Validates if resolution meets minimum requirements
    var isResolutionValid: Bool {
        guard let resolution = resolution else { return false }
        return resolution.width >= Document.minResolution.width &&
               resolution.height >= Document.minResolution.height
    }
}

// MARK: - Codable Conformance

extension Document: Codable {
    enum CodingKeys: String, CodingKey {
        case id
        case userId
        case documentType
        case status
        case fileName
        case fileSize
        case createdAt
        case updatedAt
        case resolution
        case extractedData
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(UUID.self, forKey: .id)
        userId = try container.decode(UUID.self, forKey: .userId)
        documentType = try container.decode(DocumentType.self, forKey: .documentType)
        status = try container.decode(DocumentStatus.self, forKey: .status)
        fileName = try container.decode(String.self, forKey: .fileName)
        fileSize = try container.decode(Int.self, forKey: .fileSize)
        createdAt = try container.decode(Date.self, forKey: .createdAt)
        updatedAt = try container.decodeIfPresent(Date.self, forKey: .updatedAt)
        resolution = try container.decodeIfPresent(CGSize.self, forKey: .resolution)
        
        // Handle extractedData by decoding as JSON string and converting to [String: Any]
        if let jsonString = try? container.decodeIfPresent(String.self, forKey: .extractedData),
           let jsonData = jsonString.data(using: .utf8),
           let jsonObject = try? JSONSerialization.jsonObject(with: jsonData) as? [String: Any] {
            extractedData = jsonObject
        } else {
            extractedData = nil
        }
    }
    
    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(id, forKey: .id)
        try container.encode(userId, forKey: .userId)
        try container.encode(documentType, forKey: .documentType)
        try container.encode(status, forKey: .status)
        try container.encode(fileName, forKey: .fileName)
        try container.encode(fileSize, forKey: .fileSize)
        try container.encode(createdAt, forKey: .createdAt)
        try container.encodeIfPresent(updatedAt, forKey: .updatedAt)
        try container.encodeIfPresent(resolution, forKey: .resolution)
        
        // Convert extractedData [String: Any] to JSON string for encoding
        if let data = extractedData {
            let jsonData = try JSONSerialization.data(withJSONObject: data, options: [])
            if let jsonString = String(data: jsonData, encoding: .utf8) {
                try container.encodeIfPresent(jsonString, forKey: .extractedData)
            }
        }
    }
}

// MARK: - Codable Extensions for CGSize

extension CGSize: Codable {
    enum CodingKeys: String, CodingKey {
        case width, height
    }
    
    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(width, forKey: .width)
        try container.encode(height, forKey: .height)
    }
    
    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let width = try container.decode(CGFloat.self, forKey: .width)
        let height = try container.decode(CGFloat.self, forKey: .height)
        self.init(width: width, height: height)
    }
}

